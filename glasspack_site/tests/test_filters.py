from .test_utils import BaseTestCase
from ..models import Color, FinishType, Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductFilters(BaseTestCase):
    @classmethod
    def setUpTestData(self):
        img = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )

        # Set up test filter options
        self.cat_00 = Category.objects.create(name='empty')
        self.cat_1 = Category.objects.create(name='bottles')
        self.cat_2 = Category.objects.create(name='jars')
        self.color_yel = Color.objects.create(name='yellow')
        self.color_black = Color.objects.create(name='black')
        self.fin_type_Twist = FinishType.objects.create(name='Twist off')
        self.fin_type_Crown = FinishType.objects.create(name='Crown')

        # Set up test db 
        Product.objects.create(model='prod_1', volume=100, height=1000, weight=500, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_2', volume=200, height=900, weight=600, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_3', volume=300, height=800, weight=700, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_4', volume=400, height=700, weight=800, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_5', volume=500, height=600, weight=900, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_6', volume=600, height=500, weight=100, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_7', volume=700, height=400, weight=200, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_8', volume=800, height=300, weight=300, diameter=100, image=img, is_published=True)
        Product.objects.create(model='prod_9', volume=900, height=200, weight=400, diameter=100, image=img, is_published=False)
        Product.objects.create(model='prod_10', volume=1000, height=100, weight=500, diameter=100, image=img, is_published=True)

        products = Product.objects.all()

        # Set up categories
        for p in products[:3]:
            p.categories.set([self.cat_1])
        for p in products[3:]:
            p.categories.set([self.cat_2])

        # Set up Colors + Set up finish_type
        for p in products:

            if p.volume < 600:
                p.color = self.color_yel
            if p.volume > 500:
                p.color = self.color_black

            if p.weight < 600:
                p.finish_type = self.fin_type_Twist
            if p.weight > 500:
                p.finish_type = self.fin_type_Crown

            p.save()

    def test_is_published(self):
        expected_result = Product.objects.filter(is_published=True).count()
        result = self.client.get("/products").context['paginator'].count
        self.assertEqual(result, expected_result)
        
    def test_categories_filter(self):
        expected_result = sorted(Product.objects.filter(is_published=True, categories=self.cat_1).values_list('model', flat=True))
        response = self.client.get('/products?categories=bottles')
        result = sorted(response.context['object_list'].values_list('model', flat=True))
        self.assertEqual(result, expected_result)
    

    def test_type_of_finish_filter(self):
        expected_result = sorted(Product.objects.filter(is_published=True, finish_type=self.fin_type_Twist).values_list('model', flat=True))
        response = self.client.get('/products?categories=bottles%2Cjars&finish_types=Twist+off')
        result = sorted(response.context['object_list'].values_list('model', flat=True))
        self.assertEqual(result, expected_result)

    def test_color_filter(self):
        expected_result = sorted(Product.objects.filter(is_published=True, color=self.color_yel).values_list('model', flat=True))
        response = self.client.get('/products?categories=bottles%2Cjars&colors=yellow')
        result = sorted(response.context['object_list'].values_list('model', flat=True))
        self.assertEqual(result, expected_result)

    def test_color_finish_type(self):
        expected_result = sorted(Product.objects.filter(is_published=True, color=self.color_yel, finish_type=self.fin_type_Crown).values_list('model', flat=True))
        response = self.client.get('/products?categories=jars%2Cbottles&color=yellow&finish_types=Crown')
        result = sorted(response.context['object_list'].values_list('model', flat=True))
        self.assertEqual(result, expected_result)

    def test_categories_color(self):
        expected_result = sorted(Product.objects.filter(is_published=True, categories=self.cat_2, color=self.color_black).values_list('model', flat=True))
        response = self.client.get('/products?categories=jars&colors=black')
        result = sorted(response.context['object_list'].values_list('model', flat=True))
        self.assertEqual(result, expected_result)

    def test_empty_result(self):
        expected_result = list(Product.objects.filter(categories=self.cat_00))
        response = self.client.get("/products?categories=empty")
        result = list(response.context['object_list'])
        self.assertEqual(result, expected_result)

