from django.db import IntegrityError
from django.test import TransactionTestCase
from core.models import Category, Color, FinishType, Product
from django.utils.text import slugify

class ProductTests(TransactionTestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="bottles")
        self.color = Color.objects.create(name="Green")
        self.finish_type = FinishType.objects.create(name="Crown")

        self.product = Product.objects.create(
            name="Bottle 1",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
            color=self.color,
            finish_type=self.finish_type,
        )

        self.product.categories.set([self.cat])

    def test_negative_values_for_parameters(self):
        parameters = ["volume", "height", "weight", "diameter"]
        for parameter in parameters:
            self.validate_negative_value(parameter)

    def test_auto_slugify(self):
        product = Product.objects.create(
            name=" BOTTLe!()&*%$#_-- 1 ",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
            color=self.color,
            finish_type=self.finish_type
        )

        self.assertEqual(product.slug, "bottle_-1")
        self.assertEqual(product.slug, slugify(product.name))

    def test_sligify_uniqueness(self):
        # Test 1
        duplicate = Product(
            name="Bottle 1",
            volume=100,
            height=100,
            weight=100, 
            diameter=100, 
            color=self.color,
            finish_type=self.finish_type,
        )

        self.assertEqual(self.product.name, duplicate.name)

        with self.assertRaises(IntegrityError):
            duplicate.save()

        # Test 2

        duplicate.name = "bottle 1"

        self.assertNotEqual(self.product.name, duplicate.name)
        self.assertEqual(self.product.slug, slugify(duplicate.name))

        with self.assertRaises(IntegrityError):
            duplicate.save()

    #checks constraints of Product object
    def validate_negative_value(self, field):
        setattr(self.product, field, -1)
        with self.assertRaises(IntegrityError):
            self.product.save()
