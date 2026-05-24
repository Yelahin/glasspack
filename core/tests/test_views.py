from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from core.models import Product, Color, FinishType, Category
from glasspack.settings.base import PRODUCT_PAGINATE_BY
import math

class BaseTemplateTests(TestCase):
    def test_basic_template_used_in_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "example@gmail.com")


class HomePageTests(TestCase):
    def test_home_page_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')


class AboutUsPageTests(TestCase):
    def test_about_page_use_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'core/about.html')


class ContactUsPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Contact page renders only for login users, so i make this registration and login in this class.
           Tests for users and permissions you can find in test folder of users app"""
        cls.user = get_user_model().objects.create_user(username="testuser", password="123456789")

    def test_contact_page_use_correct_template(self):
        self.client.login(username="testuser", password="123456789")
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'core/contact.html')

    
class ProductPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create some parameters for products
        cls.category1 = Category.objects.create(name="test_category1")
        cls.category2 = Category.objects.create(name="test_category2")
        cls.color1 = Color.objects.create(name="test_color1")
        cls.color2 = Color.objects.create(name="test_color2")
        cls.finish_type1 = FinishType.objects.create(name="test_finish_type1")
        cls.finish_type2 = FinishType.objects.create(name="test_finish_type2")

        cls.products_count = 100

        for number in range(cls.products_count):
            #Create products with different parameters to check - is filters work correctly
            prod = Product.objects.create(
                name=f"product_{number}",
                volume=100,
                height=100,
                weight=100,
                diameter=100, 
                color=cls.color1 if number % 2 == 0 else cls.color2, 
                finish_type=cls.finish_type1 if number % 3 == 0 else cls.finish_type2
            )
            prod.categories.set([cls.category1] if number % 5 == 0 else [cls.category2])
    
    def test_product_page_use_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, "core/products.html")

    def test_product_page_pagination(self):
        response = self.client.get(reverse('products'))
        products_count = Product.objects.filter(is_published=True).count()
        expected_pages_count = response.context['page_obj'].paginator.num_pages

        pages_count = math.ceil(products_count / PRODUCT_PAGINATE_BY)

        self.assertEqual(expected_pages_count, pages_count)
         
    def test_product_page_context(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['selected_production']), PRODUCT_PAGINATE_BY)
        self.assertContains(response, "product_")
        
    def test_product_page_filters(self):
        # Categories
        response = self.client.get(reverse("products") + f"?categories={self.category2}")
        pages_count = math.ceil(Product.objects.filter(categories=self.category2).count() / PRODUCT_PAGINATE_BY)
        expected_pages_count = response.context["page_obj"].paginator.num_pages

        self.assertEqual(expected_pages_count, pages_count)

        # Color
        response = self.client.get(reverse("products") + f"?colors={self.color2}")
        pages_count = math.ceil(Product.objects.filter(color=self.color2).count() / PRODUCT_PAGINATE_BY)
        expected_pages_count = response.context["page_obj"].paginator.num_pages

        self.assertEqual(expected_pages_count, pages_count)

        # Finish type
        response = self.client.get(reverse("products") + f"?finish_types={self.finish_type2}")
        pages_count = math.ceil(Product.objects.filter(finish_type=self.finish_type2).count() / PRODUCT_PAGINATE_BY)
        expected_pages_count = response.context["page_obj"].paginator.num_pages

        self.assertEqual(expected_pages_count, pages_count)

        # Categories + color + finish type
        response = self.client.get(reverse("products") + f"?categories={self.category1}&colors={self.color1}&finish_types={self.finish_type1}")
        pages_count = math.ceil(Product.objects.filter(categories=self.category1, color=self.color1, finish_type=self.finish_type1).count() / PRODUCT_PAGINATE_BY)
        expected_pages_count = response.context["page_obj"].paginator.num_pages

        self.assertEqual(expected_pages_count, pages_count)


class ShowProductPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        color = Color.objects.create(name="example_color")
        finish_type = FinishType.objects.create(name="example_finish_type")

        cls.product = Product.objects.create(
            name="example_model",
            volume=100,
            height=100,
            weight=100,
            diameter=100, 
            color=color,
            finish_type=finish_type,
        )

    def test_show_page_use_correct_template(self):
        response = self.client.get(reverse("products") + f"{self.product.name}/")
        self.assertTemplateUsed(response, "core/show_product.html")

    def test_show_page_context(self):
        response = self.client.get(reverse("products") +  f"{self.product.name}/")
        self.assertContains(response, "Volume")
        self.assertContains(response, "100 ml")
