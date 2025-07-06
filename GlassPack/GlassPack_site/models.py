from django.db import models

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