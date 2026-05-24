from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UsersAPITests(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username="admin", password="admin_password")
        get_user_model().objects.create_user(username="user", password="user_password")
        self.test_user = get_user_model().objects.create_user(username="test_user", password="test_user_password")

        self.data = {
            "username": "User",
            "email": "example@gmail.com",
            "password": "user_password"
        }

    def test_register_valid_data(self):
        username = "Test_user"
        password = "password1234!"
        email = "test@gmail.com"

        self.assertFalse(get_user_model().objects.filter(username=username).exists())

        response = self.client.post(
            reverse("register"), 
            data={"username": username, "password": password, "email": email})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username=username).exists())

    def test_register_invalid_password(self):
        username = "Test_user"
        password = "1"

        self.assertFalse(get_user_model().objects.filter(username=username).exists())

        response = self.client.post(
            reverse("register"), 
            data={"username": username, "password": password})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(username=username).exists())

    def test_register_invalid_password(self):
        username = "Test_user"
        password = "password1234!"
        email = "invalid@.com"

        self.assertFalse(get_user_model().objects.filter(username=username).exists())

        response = self.client.post(
            reverse("register"), 
            data={"username": username, "password": password, "email": email})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(username=username).exists())

    def test_get_users(self):
        #unauthorized user 
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
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
        self.assertEqual(resposne.status_code, status.HTTP_403_FORBIDDEN)
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
        

class UsersJWTTests(APITestCase):
    def setUp(self):
        self.username = "Test_user"
        self.password = "password1234!"

        self.user = get_user_model().objects.create_user(
            username=self.username,
            email="test@gmail.com",
            password=self.password
        )

        tokens = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": self.username, "password": self.password},
            format="json"
        ).data

        self.access_token = tokens["access"]
        self.refresh_token = tokens["refresh"]

    def test_get_tokens_valid_credentials(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": self.username, "password": self.password},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_tokens_invalid_credentials(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "Invalid_user", "password": self.password},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_access_endpoint_with_valid_token(self):
        response = self.client.get(
            reverse("me"),
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.username, response.data.values())

    def test_access_endpoint_without_token(self):
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(self.username, response.data.values())

    def test_access_endpoint_with_invalid_token(self):
        response = self.client.get(
            reverse("me"),
            headers={"Authorization": f"Bearer {self.access_token}invalid"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(self.username, response.data.values())

    def test_refresh_access_token_with_valid_refresh_token(self):
        response = self.client.post(
            reverse("token_refresh"),
            data={"refresh": self.refresh_token}
        )

        new_access_token = response.data["access"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(new_access_token, self.access_token)

    def test_refresh_access_token_with_invalid_refresh_token(self):
        response = self.client.post(
            reverse("token_refresh"),
            data={"refresh": self.refresh_token + "invalid"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)

    def test_refreshed_access_token_works(self):
        response = self.client.post(
            reverse("token_refresh"),
            data={"refresh": self.refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_access_token = response.data["access"]

        response = self.client.get(
            reverse("me"),
            headers={"Authorization": f"Bearer {new_access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.username, response.data["username"])
