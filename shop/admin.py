from django.contrib import admin
from django.contrib.admin import TabularInline
from . import models

class OrderItemInline(TabularInline):
    extra = 1
    model = models.OrderItem
    readonly_fields = ("count", "coupon_code","price")
    exclude = ("coupon", )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('customer', 'is_active', 'created_time')

@admin.register(models.VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = ( "title", 'category', "color", "size", "image_detail")
    readonly_fields = ("show_image",)
    
class VariantImageInline(TabularInline):
    extra = 1
    model = models.VariantImage
    readonly_fields = ("image_detail",)

class CouponInline(TabularInline):
    extra = 1
    model = models.Coupon

@admin.register(models.Variant)
class VariantAdmin(admin.ModelAdmin):
    inlines = (CouponInline, VariantImageInline)
    list_display = ("title", 'category',  "color", "size", "price", "quantity", "image" )
    list_editable = ("quantity",)

@admin.register(models.AdditionalInfotmation)
class AdditionalInfotmationAdmin(admin.ModelAdmin):
    list_display = ('product', "content")
    
@admin.register(models.CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ('title', "parent", "image_detail")
    readonly_fields = ("show_image",)

class CategoryImageInline(TabularInline):
    extra = 1
    model = models.CategoryImage
    readonly_fields = ("image_detail",)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (CategoryImageInline,)
    list_display = ('title', "parent", "discount", "image")

@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'category', "title", "color", "size",)
    list_editable = ("is_active",)

class ProductImageInline(TabularInline):
    extra = 1
    model = models.ProductImage
    readonly_fields = ("image_detail",)

class AdditionalInformationInline(TabularInline):
    extra = 1
    model = models.AdditionalInfotmation

class ReviewInline(TabularInline):
    extra = 1
    model = models.Review

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (AdditionalInformationInline, ProductImageInline, ReviewInline)
    list_display = ('title', "category","price","created_time", "discount", "is_featured", "view_count", "image")
    list_editable = ("price", "discount", "is_featured",)

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('title', "category", "image_detail")
    readonly_fields = ("show_image",)

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title","category", 'owner',"rating", "review", )
    readonly_fields = ("product", 'owner',"rating", "review" )

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "first_name", "last_name", "payment_time" ,"amount")

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category","order", "color", "size", "price","count","image" )
    readonly_fields = ("show_image",)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.FavoriteProduct)