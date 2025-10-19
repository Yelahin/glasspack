from django.contrib.auth import get_user_model
from glasspack import settings
from django.test import TestCase
from django.urls import reverse
from glasspack_site.models import IndexContent, FooterContent, AboutContent, ContactContent, Product, Color, FinishType, Category

class BaseTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        FooterContent.objects.create(
            company_name="some company",
            company_info="test company",
            address="some address",
            work_time="01:00 - 16:00",
            registration_number="1234567",
            email="example@gmail.com",
            phone="+111111111"
        )


    def test_base_template_context(self):
        response = self.client.get(reverse('home'))

        def _check_all_footer_info(text):
            self.assertContains(response, "some company")

        footer_info = [
            "some company", 
            "test company", 
            "some_address",
             "01:00 - 16:00", 
            "1234567",
            "example@gmail.com",
            "+111111111",
            "Home",
            "About us", 
            "Contact us",
            "Products",
                       ]
        
        for footer_text in footer_info:
            _check_all_footer_info(footer_text)
        

class HomePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        IndexContent.objects.create(
            title="Home page",
            subtitle="This is home page",
            mission_intro="Our mission",
            mission_details="We are providing bottles and jars",
            contact_text="You can contact us!",
            products_subtitle="This is our products"
        )

    def test_home_page_use_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'glasspack_site/index.html')

    def test_home_page_context(self):
        response = self.client.get(reverse('home'))

        def _check_home_page_info(text):
            self.assertContains(response, text)
            
        home_page_info = [
            "Home page",
            "This is home page", 
            "Our mission",
            "We are providing bottles and jars",
            "You can contact us!",
            "This is our products",
        ]

        for info in home_page_info:
            _check_home_page_info(info)


class AboutUsPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AboutContent.objects.create(content="some content")

    def test_about_page_use_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'glasspack_site/about.html')

    def test_about_page_context(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, "some content")


class ContactUsPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ContactContent.objects.create(subtitle="You can contact us - here!")

        """Contact page renders only for login users, so i make this registration and login in this class.
           Tests for users and permissions you can find in test folder of glasspack_users app"""
        cls.user = get_user_model().objects.create_user(username="testuser", password="123456789")

    def test_contact_page_use_correct_template(self):
        self.client.login(username="testuser", password="123456789")
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'glasspack_site/contact.html')

    def test_contact_page_context(self):
        self.client.login(username="testuser", password="123456789")
        response = self.client.get(reverse('contact'))
        self.assertContains(response, "You can contact us - here!")

    
class ProductPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category_test1 = Category.objects.create(name="test_category1")
        category_test2 = Category.objects.create(name="test_category2")
        color_test1 = Color.objects.create(name="test_color1")
        color_test2 = Color.objects.create(name="test_color2")
        finish_type_test1 = FinishType.objects.create(name="test_finish_type1")
        finish_type_test2 = FinishType.objects.create(name="test_finish_type2")

        cls.products_count = 100

        for number in range(cls.products_count):
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
            response = self.client.get(reverse('products') + f"?page={page}")
            obj_count = len(response.context['selected_production'])
            if page != num_pages:
                self.assertEqual(obj_count, settings.PRODUCT_PAGINATE_BY)
            else:
                self.assertEqual(obj_count,  self.products_count % settings.PRODUCT_PAGINATE_BY)
                
    def test_product_page_context(self):
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

        self._check_product_page_context("", Product.objects.all())

        for parameters in filters_parameters:
            filter_param = {f"{key}__name": value for key, value in parameters.items()}

            objects_list = Product.objects.filter(**filter_param)

            url_filter = "?" + "&".join([f"{key}={value}" for key, value in filter_param.items()])

            self._check_product_page_context(url_filter, objects_list)
        
    def test_product_page_filters_info(self):
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

    def _check_product_page_context(self, filter_url, filtered_products):
        response = self.client.get(reverse('products') + filter_url)
        num_pages = response.context['page_obj'].paginator.num_pages

        view_products = []
        for page_number in range(1, num_pages+1):
            if filter_url:
                response = self.client.get(reverse('products') + filter_url + f"&page={page_number}")
            else:
                response = self.client.get(reverse('products') + f"?page={page_number}")

            self.assertEqual(response.status_code, 200)

            for product in response.context["selected_production"]:
                if product in filtered_products:
                    view_products.append(product)

        self.assertQuerySetEqual(view_products, filtered_products, ordered=False)
        

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
