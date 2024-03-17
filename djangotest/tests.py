from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import App, Subscription

# Create your tests here.
class AuthenticationTestCase(APITestCase):
    def test_register(self):
        data = {
            "email": "admin@admin.com",
            "username": "admin",
            "password": "123456",
            "is_staff": True,
            "is_superuser": True
        }
        response = self.client.post(reverse('auth_register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', '123456')
        data = {
            "username": "admin",
            "password": "123456"
        }
        response = self.client.post(reverse('auth_login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AppsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test')
        self.client.force_login(user=self.user)
        self.token = Token.objects.create(user=self.user)

        self.new_app = App.objects.create(
            name='UnitTest', description='UnitTest', user=self.user)
        self.create_payload = {
            "name": "UnitTest",
            "description": "UnitTest"
        }
        self.update_payload = {
            "name": "UnitTest2",
            "description": "UnitTest2"
        }

    def test_get_apps(self):
        response = self.client.get(reverse('get_all_apps'), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_app(self):
        response = self.client.post(reverse('create_new_app'), data=self.create_payload, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_app(self):
        response = self.client.post(reverse('update_app', kwargs={'pk': self.new_app.pk}), data=self.update_payload, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_app(self):
        response = self.client.delete(reverse('delete_app', kwargs={'pk': self.new_app.pk}), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

class SubscriptionsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test')
        self.client.force_login(user=self.user)
        self.token = Token.objects.create(user=self.user)

        self.new_app = App.objects.create(
            name='UnitTest', description='UnitTest', user=self.user)
        
        self.new_subs = Subscription.objects.create(
            app=self.new_app, plan=1, subscribed=True)

        self.update_payload = {
            "app": self.new_app.pk,
            "plan": 1,
            "subscribed": True
        }

    def test_get_subs(self):
        response = self.client.get(reverse('get_all_subscriptions'), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sub(self):
        response = self.client.post(reverse('update_subscription'), data=self.update_payload, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)