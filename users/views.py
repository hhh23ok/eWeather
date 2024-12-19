# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from forecast.models import Location
from notifications.models import BotUser
from users.forms import TelegramUsernameForm


@login_required
def account(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    bot_link = "https://t.me/eWeatherNotificationBot"

    # Check if the user is already a BotUser
    bot_user = BotUser.objects.filter(email=request.user.email).first()

    # Handle form submission if the user is not a BotUser
    if not bot_user:
        if request.method == "POST":
            form = TelegramUsernameForm(request.POST)
            if form.is_valid():
                # Create a new BotUser with the provided Telegram username
                BotUser.objects.create(
                    email=request.user.email,
                    username=form.cleaned_data['username'],
                    user_id=request.user.id,  # Use the Django user ID or a unique value
                    chat_id=0  # Placeholder chat ID, adjust as needed
                )
                return redirect('account')  # Reload the page after creation
        else:
            form = TelegramUsernameForm()
    else:
        form = None  # No form needed if the user is already a BotUser

    user_info = {
        "username": request.user.username,
        "email": request.user.email,
    }

    saved_locations = bot_user.locations.all() if bot_user else []

    return render(request,
                  'users/account.html',
                  {'bot_link': bot_link,
                   'user_info': user_info,
                   'saved_locations': saved_locations,
                   'form': form,
                   'is_bot_user': bool(bot_user)})


@login_required
def location_delete(request, id):
    if request.method == "POST":
        location = get_object_or_404(Location, id=id)
        location.delete()
        return redirect('users:account')
