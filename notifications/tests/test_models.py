from django.test import TestCase
from notifications.models import BotUser
from forecast.models import Location
from django.db.utils import IntegrityError


class BotUserModelTest(TestCase):
    def setUp(self):
        """
        Creating test data for Location and BotUser models.
        """
        self.location1 = Location.objects.create(city="Kyiv")
        self.location2 = Location.objects.create(city="Lviv")

        self.bot_user = BotUser.objects.create(
            user_id=1,
            chat_id=12345,
            username="test_user",
            email="test@example.com"
        )
        self.bot_user.locations.add(self.location1)

    def test_botuser_creation(self):
        """Test for creating a BotUser object"""
        self.assertEqual(self.bot_user.user_id, 1)
        self.assertEqual(self.bot_user.chat_id, 12345)
        self.assertEqual(self.bot_user.username, "test_user")
        self.assertEqual(self.bot_user.email, "test@example.com")
        self.assertTrue(self.bot_user.is_active)
        self.assertEqual(self.bot_user.locations.count(), 1)

    def test_str_method(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.bot_user), "test_user")

        # If username is empty
        bot_user_no_username = BotUser.objects.create(user_id=2, chat_id=54321)
        self.assertEqual(str(bot_user_no_username), "Bot User 2")

    def test_unique_constraint(self):
        """Test the uniqueness constraint for BotUser"""
        with self.assertRaises(IntegrityError):
            BotUser.objects.create(
                user_id=1,  # Repeat user_id
                chat_id=12345,  # Repeat chat_id
                username="test_user"  # Repeat username
            )

    def test_many_to_many_relationship(self):
        """Test ManyToManyField relationship between BotUser and Location"""
        self.bot_user.locations.add(self.location2)
        self.assertEqual(self.bot_user.locations.count(), 2)
        self.assertIn(self.location1, self.bot_user.locations.all())
        self.assertIn(self.location2, self.bot_user.locations.all())
