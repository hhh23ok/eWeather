# notifications/telegram_bot.py
import asyncio
from asgiref.sync import sync_to_async
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from django.db import IntegrityError
from notifications.models import BotUser
from notifications.services import check_extremal_conditions
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from forecast.services import generate_daily_forecast_tg


user_data = {}


# Wrapping the ORM call to make it async-friendly
@sync_to_async
def update_or_create_user(user_id, chat_id, username, date_joined):
    from .models import BotUser
    user, created = BotUser.objects.update_or_create(
        user_id=user_id,
        chat_id=chat_id,
        username=username,
        defaults={'date_joined': date_joined, 'is_active': True}
    )
    return user, created


# /start handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    user_data[user_id] = {
        'chat_id': chat_id,
        'username': username
    }

    try:
        # Call the wrapped sync ORM method asynchronously
        user, created = await update_or_create_user(user_id, chat_id, username, update.message.date)

        if created:
            print(f"New user added: {user.username if user.username else user.user_id}")
        else:
            print(f"User updated: {user.username if user.username else user.user_id}")

        # Sending the welcome message with markdown formatting
        welcome_message = (
            f"Welcome, *{username}*!\n\n"
            "If you'd like to get the weather forecast, use the command: `/weather`\n"
            "Simply type it in the chat to receive the latest weather updates."
        )

        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    except IntegrityError:
        print(f"Error: User with user_id={user_id}, chat_id={chat_id}, username={username} already exists.")
        await update.message.reply_text("This user is already registered.")


# Weather command to display location options
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Get user from the database
    user = await sync_to_async(BotUser.objects.get)(user_id=user_id)

    # Get user's saved locations
    user_locations = await sync_to_async(list)(user.locations.values_list('city', flat=True))

    if not user_locations:
        await update.message.reply_text("You don't have any saved locations, please add them in your profile.")
        return

    # Create location buttons
    keyboard = [[InlineKeyboardButton(location, callback_data=location)] for location in user_locations]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a location to get the forecast:", reply_markup=reply_markup)


# Callback to handle location selection and prompt for forecast days
async def location_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    location = query.data

    # Store selected location in context for later use
    context.user_data['location'] = location

    await query.answer()  # Acknowledge the callback
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)

    # Prompt the user to select the number of forecast days (3, 5, or 7)
    keyboard = [
        [InlineKeyboardButton("3 days", callback_data="3")],
        [InlineKeyboardButton("5 days", callback_data="5")],
        [InlineKeyboardButton("7 days", callback_data="7")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select the number of days for the weather forecast:", reply_markup=reply_markup)


# Callback to handle the number of forecast days selection and generate forecast
async def days_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    days = int(query.data)

    # Get the selected location from user data
    location = context.user_data.get('location')

    # Acknowledge the callback and show typing action
    await query.answer()
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)

    # Fetch combined weather forecast data for the selected number of days
    weather_data = await generate_daily_forecast_tg(location)

    # Generate the weather forecast for the selected days
    forecast_message = f"*Weather forecast for {location} ({days} days):*\n"

    # Get the forecast for the specified number of days
    for i in range(min(days, len(weather_data))):
        forecast_day = weather_data[i]  # forecast_day is now a dictionary
        forecast_message += (
            f"\n*{forecast_day['date']}*\n"  # Print actual date instead of "Day 1"
            f"🌡️ Min Temp: {forecast_day['min_temperature']} - Max Temp: {forecast_day['max_temperature']}\n"
            f"☀️ UV Index: {forecast_day['uv_index']}\n"
            f"🌬️ Wind Gust: {forecast_day['wind_gust']}\n"
            f"🌧️ Precipitation Chance: {forecast_day['precip_prob']}\n"  # Add precipitation chance
            f"Condition: {forecast_day['condition']}\n\n"
        )

    await query.edit_message_text(forecast_message, parse_mode=ParseMode.MARKDOWN)

    # Check and report dangerous conditions
    extremal_conditions = check_extremal_conditions(weather_data)
    if extremal_conditions:
        await query.message.reply_text("\n".join(extremal_conditions), parse_mode=ParseMode.MARKDOWN)
    else:
        await query.message.reply_text("✅ Weather conditions are safe!", parse_mode=ParseMode.MARKDOWN)


# Run bot
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CallbackQueryHandler(location_callback, pattern="^[A-Za-z ]+$"))  # Regex pattern to match location
    application.add_handler(CallbackQueryHandler(days_selection_callback, pattern="^[3,5,7]$"))  # Handle 3, 5, or 7 days

    print("Telegram bot started...")
    try:
        loop.run_until_complete(application.run_polling())
    except Exception as e:
        print(f"Error starting the bot: {e}")