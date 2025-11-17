from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


class UserMessage(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    comment = models.TextField(max_length=1000, validators=[MinLengthValidator(10)])
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        verbose_name = "5. User messages"
        verbose_name_plural = "5. User messages"

    def __str__(self):
        return f"{self.full_name} {self.email} {self.date}"
    
    