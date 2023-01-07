from django.contrib import admin
from .models import Customer
from django.contrib.admin import TabularInline
from shop.models import Payment, Order, FavoriteProduct

class FavoriteProductInline(TabularInline):
    extra = 1
    model = FavoriteProduct
    readonly_fields=("product","image")

class PaymentInline(TabularInline):
    extra = 1
    model = Payment
    fields = ("order", "amount")
    readonly_fields = ("order", "amount")
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = (FavoriteProductInline,PaymentInline )
    list_display = ("username", "first_name", "last_name", "email")
    