# notifications/apps.py
from django.apps import AppConfig
import threading
import os


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    def ready(self):

        # Уникаємо запуску бота під час міграцій або серверних перезавантажень
        if os.environ.get("RUN_MAIN", None) != "true":
            return
        from . import telegram_bot
        # Запускаємо бота у окремому потоці
        bot_thread = threading.Thread(target=telegram_bot.run_bot, daemon=True)
        bot_thread.start()
