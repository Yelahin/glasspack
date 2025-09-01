from http import HTTPStatus
from django.urls import reverse
from .test_utils import BaseTestCase
from ..models import Product, Category, Color, FinishType
from django.core.files.uploadedfile import SimpleUploadedFile


class GetPages(BaseTestCase):
    def setUp(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )
        bottles = Category.objects.create(name='bottles')
        color = Color.objects.create(name='yellow')
        finish_type = FinishType.objects.create(name='Twist off')
        product = Product.objects.create(model='example 1',
                                         volume=999,
                                         height=999,
                                         weight=999, 
                                         diameter=999,
                                         image=image,
                                         is_published=True)
        
        product.categories.set([bottles])
        product.color = color
        product.finish_type = finish_type

    def test_index_page(self):
        page = self.client.get(reverse('home'))
        self.assertEqual(page.status_code, HTTPStatus.OK)

    def test_about_page(self):
        page = self.client.get(reverse('about'))
        self.assertEqual(page.status_code, HTTPStatus.OK)

    def test_contact_page(self):
        page = self.client.get(reverse('contact'))
        self.assertEqual(page.status_code, HTTPStatus.OK)

    def test_product_page(self):
        page = self.client.get(reverse('products'))
        self.assertEqual(page.status_code, HTTPStatus.OK)
