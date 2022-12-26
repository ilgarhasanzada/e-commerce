from django.contrib import admin
from . import models

admin.site.register(models.AdditionalInfotmation)
admin.site.register(models.Category)
admin.site.register(models.CategoryImage)
admin.site.register(models.Color)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Review)
admin.site.register(models.Size)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.FavoriteProduct)
admin.site.register(models.Variant)