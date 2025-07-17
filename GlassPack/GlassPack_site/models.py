from django.db import models
from django.utils.text import slugify

# Create your models here.

class FooterInfo(models.Model):
    company_name = models.CharField(max_length=50)
    company_info = models.TextField()
    address = models.CharField(max_length=100)
    work_time = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=25)


    def __str__(self):
        return self.company_name
    

class ContactText(models.Model):
    subtitle = models.TextField()

    def __str__(self):
        return self.subtitle
    

class AboutInfo(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
    

class IndexContent(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    mission_intro = models.TextField(max_length=350)
    mission_details = models.TextField(max_length=350)
    contact_text = models.CharField(max_length=150)
    products_subtitle = models.TextField(max_length=500)

    def __str__(self):
        return self.title


class Product(models.Model):
    PRODUCT_TYPE = [
        ('bottles', 'Bottles'),
        ('jars', 'Jars')
    ]
    model = models.CharField(max_length=100, null=True)
    volume = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField(null=True)
    diameter = models.IntegerField(null=True)
    color = models.CharField(max_length=30, null=True)
    finish_type = models.CharField(max_length=100, null=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE)
    slug = models.SlugField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.model
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.model)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return 

