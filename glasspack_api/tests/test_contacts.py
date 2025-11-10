from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UsersMessagesAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="user", password="user_password")
        
    def test_only_authorized_users_can_create_messages(self):
        data = {
            "full_name": "user",
            "email": "example@gmail.com",
            "comment": "some comment"
        }

        #unauthorized user
        response = self.client.post(path=reverse("contacts"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.post(path=reverse("contacts"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        