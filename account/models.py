from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "customer")
    def __str__(self) -> str:
        return self.user.username

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name
    @property
    def last_name(self):
        return self.user.last_name
    @property
    def email(self):
        return self.user.email