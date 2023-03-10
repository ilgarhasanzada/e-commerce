from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Customer, Product, Variant

User = get_user_model()
 
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.customer.save()

@receiver(post_save, sender = Product)
def create_variant(sender, instance, created, **kwargs):
    if created:
        Variant.objects.create(price = instance.price, product = instance, color = None, size = None)

# @receiver(post_save, sender=Product)
# def save_variant(sender, instance, **kwargs):
#         instance.variants.save()