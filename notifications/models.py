# notifications/models.py
from django.db import models
from forecast.models import Location


class BotUser(models.Model):
    user_id = models.IntegerField('User ID', primary_key=True)
    chat_id = models.IntegerField('Chat ID')
    username = models.CharField('Username', max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    is_active = models.BooleanField('Active', default=True)
    email = models.EmailField('Email Address', blank=True, null=True)
    locations = models.ManyToManyField(Location, related_name='users')

    # Unique constraint for combination of chat_id, user_id, and username
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chat_id', 'user_id', 'username'],
                                    name='unique_chat_user')
        ]

    def __str__(self):
        return self.username if self.username else f"Bot User {self.user_id}"

