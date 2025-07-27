from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

#Models for templates

class FooterInfo(models.Model):
    company_name = models.CharField(max_length=50)
    company_info = models.TextField()
    address = models.CharField(max_length=100)
    work_time = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=25)

    class Meta:
        verbose_name = "3. Footer information"
        verbose_name_plural = "3. Footer information"



    def __str__(self):
        return self.company_name
    

class ContactInfo(models.Model):
    subtitle = models.TextField()

    class Meta:
        verbose_name = "6. Contact us page information"
        verbose_name_plural = "6. Contact us page information"

    def __str__(self):
        return self.subtitle
    

class AboutInfo(models.Model):
    content = models.TextField()

    class Meta:
        verbose_name = "5. About us page information"
        verbose_name_plural = "5. About us page information"

    def __str__(self):
        return self.content
    

class IndexContent(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    mission_intro = models.TextField(max_length=350)
    mission_details = models.TextField(max_length=350)
    contact_text = models.CharField(max_length=150)
    products_subtitle = models.TextField(max_length=500)

    class Meta:
        verbose_name = "4. Home page information"
        verbose_name_plural = "4. Home page information"

    def __str__(self):
        return self.title


#Models for production

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "2. Categories"
        verbose_name_plural = "2. Categories"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    model = models.CharField(max_length=100)
    volume = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    diameter = models.IntegerField()
    color = models.CharField(max_length=30)
    finish_type = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    is_published = models.BooleanField()
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = "1. Products"
        verbose_name_plural = "1. Products"

    def __str__(self):
        return self.model
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.model)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

#Contact Form
class UserMessage(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "7. User messages"
        verbose_name_plural = "7. User messages"

    def __str__(self):
        return f"{self.full_name} {self.email} {self.date}"