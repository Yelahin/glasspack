from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UsersAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username="admin", password="admin_password")
        get_user_model().objects.create_user(username="user", password="user_password")
        self.test_user = get_user_model().objects.create_user(username="test_user", password="test_user_password")

        self.data = {
            "username": "User",
            "email": "example@gmail.com",
            "password": "user_password"
        }

    def test_get_users(self):
        #unauthorized user
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_can_create_users(self):
        response = self.client.post(path=reverse("users-list"), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authorized_user_can_not_create_users(self):
        self.client.login(username="user", password="user_password")
        response = self.client.post(path=reverse("users-list"), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_users(self):
        self.client.login(username="admin", password="admin_password")
        response = self.client.post(path=reverse("users-list"), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_admin_user_can_update(self):
        data = {"username": "Some_user"}
        #unauthorized user
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.test_user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.test_user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.test_user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_admin_user_can_delete(self):
        #unauthorized user
        response = self.client.delete(reverse("users-detail", kwargs={"pk": self.test_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.delete(reverse("users-detail", kwargs={"pk": self.test_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.delete(reverse("users-detail", kwargs={"pk": self.test_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_authorized_user_can_check_me_endpoint(self):
        #unauthorized user
        resposne = self.client.get(reverse("me"))
        self.assertEqual(resposne.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized me
        self.client.login(username="test_user", password="test_user_password")
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, f'"id":{self.test_user.pk}')
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, f'"id":{self.admin_user.pk}')
        