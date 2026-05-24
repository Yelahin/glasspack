from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.

#Models for products

class SlugifyModel(models.Model):
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def clean(self):
        slug = self.slug if self.slug else slugify(self.name)

        if self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            raise ValidationError(f"Object with slug {slug} already exists!")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(SlugifyModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "4. Categories"
        verbose_name_plural = "4. Categories"

    def __str__(self):
        return self.name
    

class FinishType(SlugifyModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "2. Types of finish"
        verbose_name_plural = "2. Types of finish"

    def __str__(self):
        return self.name 
    

class Color(SlugifyModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "3. Colors"
        verbose_name_plural = '3. Colors'

    def __str__(self):
        return self.name
    

class Product(SlugifyModel):
    name = models.CharField(max_length=100, unique=True)
    volume = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    diameter = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    finish_type = models.ForeignKey(FinishType, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='products/', blank=True)
    is_published = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = "1. Products"
        verbose_name_plural = "1. Products"

        constraints = [
            models.CheckConstraint(condition=models.Q(volume__gte=0), name="volume_gte_0"),
            models.CheckConstraint(condition=models.Q(height__gte=0), name="height_gte_0"),
            models.CheckConstraint(condition=models.Q(weight__gte=0), name="weight_gte_0"),
            models.CheckConstraint(condition=models.Q(diameter__gte=0), name="diameter_gte_0"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
