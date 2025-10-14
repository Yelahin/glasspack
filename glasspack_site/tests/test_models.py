from django.db import IntegrityError
from django.test import TestCase
from glasspack_site.models import Category, Color, FinishType, Product

class ProductModelTest(TestCase):
    def setUp(self):
        cat_bottle = Category.objects.create(name="bottles")
        color_bottle = Color.objects.create(name="green")
        finish_type_bottle = FinishType.objects.create(name="Crown")

        self.product = Product.objects.create(
            model="Bottle 1",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
        )

        self.product.categories.set([cat_bottle])
        self.product.color = color_bottle
        self.product.finish_type = finish_type_bottle


    #checks constraints of Product model
    def negative_value_validation(self, field):
        setattr(self.product, field, -1)
        with self.assertRaises(IntegrityError):
            self.product.save()

    def test_negative_value_validation(self):
        self.negative_value_validation("volume")

    def test_negative_height_validation(self):
        self.negative_value_validation("height")

    def test_negative_weight_validation(self):
        self.negative_value_validation("weight")

    def test_negative_diameter_validation(self):
        self.negative_value_validation("diameter")

    #test slugify

    def test_product_save_slugify(self):
        self.assertEqual(self.product.slug, "bottle-1")

        product = Product.objects.create(
            model=" BOTTLe!()&*%$#_-- 1 ",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
        )

        self.assertEqual(product.slug, "bottle_-1")

