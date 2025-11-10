from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from glasspack_site.models import Product, Category, Color, FinishType

class ProductAPITestCase(APITestCase):
    def setUp(self):
        #Create users
        self.admin_user = get_user_model().objects.create_superuser(username="admin", password="admin_password")
        self.user = get_user_model().objects.create_user(username="user", password="user_password")

        #Create a product
        self.cat_bottle = Category.objects.create(name="bottles")
        self.color_bottle = Color.objects.create(name="green")
        self.finish_type_bottle = FinishType.objects.create(name="Crown")

        self.product = Product.objects.create(
            model="Bottle 1",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
        )

        self.product.categories.set([cls.cat_bottle])
        self.product.color = cls.color_bottle
        self.product.finish_type = cls.finish_type_bottle

        #Create url
        self.url = reverse("products-list")
            
    def test_get_product(self):
        resposne = self.client.get(self.url)
        self.assertEqual(resposne.status_code, status.HTTP_200_OK)
        self.assertEqual(resposne.data['results'][0]['model'], self.product.model)

    def test_only_super_user_can_create_product(self):
        #Set parameters for product
        data = {
            "model": "Bottle 2",
            "volume": 100, 
            "height": 100,
            "weight": 100, 
            "diameter": 100,
            "categories": [self.cat_bottle.pk],
            "color": self.color_bottle.pk,
            "finish_type": self.finish_type_bottle.pk,
        }

        #unauthorized user
        response = self.client.post(path=reverse("products-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.post(path=reverse("products-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.post(path=reverse("products-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_super_user_can_update_product(self):
        data = {"model": "New model"}
        #unauthorized user
        response = self.client.patch(reverse("products-detail", kwargs={"pk": self.product.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.patch(reverse("products-detail", kwargs={"pk": self.product.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.patch(reverse("products-detail", kwargs={"pk": self.product.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_super_user_can_delete_prodcut(self):
        #unauthorized user
        response = self.client.delete(reverse("products-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(model="Bottle 1").exists())
        #authorized user
        self.client.login(username="user", password="user_password")
        response = self.client.delete(reverse("products-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(model="Bottle 1").exists())
        #admin user
        self.client.login(username="admin", password="admin_password")
        response = self.client.delete(reverse("products-detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(model="Bottle 1").exists())

