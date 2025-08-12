from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


class GetPages(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )
        category = Category.objects.create(name='bottles')
        product = Product.objects.create(model='example 1',
                                         volume=999,
                                         height=999,
                                         weight=999, 
                                         diameter=999,
                                         color='Black',
                                         finish_type='Some type',
                                         image=image,
                                         is_published=True)
        
        product.categories.add(category)

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