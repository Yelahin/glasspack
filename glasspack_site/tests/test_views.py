from django.contrib.auth import get_user_model
from glasspack import settings
from django.test import TestCase
from django.urls import reverse
from glasspack_site.models import Product, Color, FinishType, Category

class BaseTemplateTest(TestCase):
    def test_basic_template_used_in_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "example@gmail.com")


class HomePageTest(TestCase):
    def test_home_page_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'glasspack_site/index.html')


class AboutUsPageTest(TestCase):
    def test_about_page_use_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'glasspack_site/about.html')


class ContactUsPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Contact page renders only for login users, so i make this registration and login in this class.
           Tests for users and permissions you can find in test folder of glasspack_users app"""
        cls.user = get_user_model().objects.create_user(username="testuser", password="123456789")

    def test_contact_page_use_correct_template(self):
        self.client.login(username="testuser", password="123456789")
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'glasspack_site/contact.html')

    
class ProductPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create some parameters for products
        category_test1 = Category.objects.create(name="test_category1")
        category_test2 = Category.objects.create(name="test_category2")
        color_test1 = Color.objects.create(name="test_color1")
        color_test2 = Color.objects.create(name="test_color2")
        finish_type_test1 = FinishType.objects.create(name="test_finish_type1")
        finish_type_test2 = FinishType.objects.create(name="test_finish_type2")

        cls.products_count = 100

        for number in range(cls.products_count):
            #Create products with different parameters to check - is filters work correctly
            prod = Product.objects.create(
                model=f"product_{number}",
                volume=100,
                height=100,
                weight=100,
                diameter=100, 
                color=color_test1 if number % 2 == 0 else color_test2, 
                finish_type=finish_type_test1 if number % 3 == 0 else finish_type_test2
            )
            prod.categories.set([category_test1] if number % 5 == 0 else [category_test2])
    

    def test_product_page_use_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, "glasspack_site/products.html")

    def test_product_page_pagination(self):
        response = self.client.get(reverse('products'))
        num_pages = response.context['page_obj'].paginator.num_pages
        
        for page in range(1, num_pages+1):
            #Getting products count from different pages
            response = self.client.get(reverse('products') + f"?page={page}")
            obj_count = len(response.context['selected_production'])

            if page != num_pages:
                #if page not equal num_pages - it isn't the last page. obj_count should be equal to PRODUCT_PAGINATE_BY
                self.assertEqual(obj_count, settings.PRODUCT_PAGINATE_BY)
            else:
                #if it is the last page - obj_count should be equal to expected_valud
                expected_value = self.products_count - ((num_pages - 1) * settings.PRODUCT_PAGINATE_BY)
                self.assertEqual(obj_count,  expected_value)
                
    def test_product_page_context(self):
        #test without any filters
        self._check_product_page_context("", Product.objects.all())

        filters_parameters = [
            {"categories": "test_category1"},
            {"categories": "test_category2"},
            {"color": "test_color1"},
            {"color": "test_color2"},
            {"finish_type": "test_finish_type1"},
            {"finish_type": "test_finish_type2"},
            {"categories": "test_category1", "color": "test_color2"},
            {"color": "test_color1", "finish_type": "test_finish_type2"},
            {"categories": "test_category1", "color": "test_color2", "finish_type": "test_finish_type2"},
        ]

        #tests with filters
        for parameters in filters_parameters:
            filter_param = {f"{key}__name": value for key, value in parameters.items()}

            objects_list = Product.objects.filter(**filter_param)

            #create url with filters on
            url_filter = "?" + "&".join([f"{key}={value}" for key, value in filter_param.items()])

            self._check_product_page_context(url_filter, objects_list) 
        
    def test_product_page_filters_shows_expected_count_of_products(self):
        response = self.client.get(reverse('products'))

        filter_parameters = [
            {"color": "test_color1"},
            {"color": "test_color2"},
            {"finish_type": "test_finish_type1"},
            {"finish_type": "test_finish_type2"},
        ]

        def _check_filter_info(filter_parameters: dict):
            filter_parameters = {f"{key}__name": value for key, value in filter_parameters.items()}
            filter_products_count = Product.objects.filter(**filter_parameters).count()
            self.assertContains(response, f"{list(filter_parameters.values())[0]} ({filter_products_count})")

        for parameter in filter_parameters:
            _check_filter_info(parameter)


    def _check_product_page_context(self, filter_url, expected_products):
            #Get page with filter on 
            response = self.client.get(reverse('products') + filter_url)
            num_pages = response.context['page_obj'].paginator.num_pages

            view_products = []
            for page_number in range(1, num_pages+1):
                if filter_url:
                    #if filter on
                    response = self.client.get(reverse('products') + filter_url + f"&page={page_number}")
                else:
                    #if filter off
                    response = self.client.get(reverse('products') + f"?page={page_number}")

                self.assertEqual(response.status_code, 200)

                for product in response.context["selected_production"]:
                    if product in expected_products:
                        view_products.append(product)

            self.assertQuerySetEqual(view_products, expected_products, ordered=False)  


class ShowProductPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        color = Color.objects.create(name="example_color")
        finish_type = FinishType.objects.create(name="example_finish_type")

        Product.objects.create(
            model="example_model",
            volume=100,
            height=100,
            weight=100,
            diameter=100, 
            color=color,
            finish_type=finish_type,
        )

    def test_show_page_use_correct_template(self):
        response = self.client.get('/products/example_model/')
        self.assertTemplateUsed(response, "glasspack_site/show_product.html")

    def test_show_page_context(self):
        response = self.client.get('/products/example_model/')
        self.assertContains(response, "Volume")
        self.assertContains(response, "100 ml")
