from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

#Models for products

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "4. Categories"
        verbose_name_plural = "4. Categories"

    def __str__(self):
        return self.name
    

class FinishType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "2. Types of finish"
        verbose_name_plural = "2. Types of finish"

    def __str__(self):
        return self.name 
    

class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "3. Colors"
        verbose_name_plural = '3. Colors'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    model = models.CharField(max_length=100)
    volume = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    diameter = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.PROTECT, null=True, blank=True)
    finish_type = models.ForeignKey(FinishType, on_delete=models.PROTECT, null=True, blank=True)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=100, blank=True)
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
        return self.model
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.model)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})