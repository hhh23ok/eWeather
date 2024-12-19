from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from forecast.models import Location
from notifications.models import BotUser


class LocationDeleteViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client = Client()

        # Create a Location instance
        self.location = Location.objects.create(city='Test Location')

        # Create a BotUser and associate it with the location
        self.bot_user = BotUser.objects.create(user_id=1, chat_id=12345, email=self.user.email, username='test_bot_user')
        self.bot_user.locations.add(self.location)

        # URL for deleting the location
        self.location_delete_url = reverse('users:location_delete', args=[self.location.id])

    def test_location_delete_redirect_if_not_logged_in(self):
        response = self.client.post(self.location_delete_url)
        self.assertRedirects(response, f"{reverse('account_login')}?next={self.location_delete_url}")

    def test_location_delete_successful(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.location_delete_url)

        # Check that the location is deleted
        self.assertFalse(Location.objects.filter(id=self.location.id).exists())

        # Check that the user is redirected to the account page
        self.assertRedirects(response, reverse('users:account'))

    def test_location_delete_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        invalid_delete_url = reverse('users:location_delete', args=[999])

        response = self.client.post(invalid_delete_url)
        self.assertEqual(response.status_code, 404)
