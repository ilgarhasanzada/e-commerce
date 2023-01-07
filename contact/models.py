from django.db import models
from django.core.exceptions import ValidationError
from account.models import Customer
# Create your models here.

class Message(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True, related_name = "messages")
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    subject = models.CharField(max_length = 200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f'{self.name} / {self.subject}'

class Contact(models.Model):
    street = models.CharField(max_length = 150)
    city = models.CharField(max_length = 150, null=True)
    country = models.CharField(max_length = 150, null = True)
    location_iframe = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return "contact"

    def clean(self) -> None:
        if Contact.objects.exists() and not self.pk:
            raise ValidationError("Contact already exists!")