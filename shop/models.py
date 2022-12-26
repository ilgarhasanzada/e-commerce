from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "customer")
    def __str__(self) -> str:
        return self.user.username

class Size(models.Model):
    title = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.title

class Color(models.Model):
    title = models.CharField(max_length = 50)
    code = models.CharField(max_length=10, null = True, blank = True)

    def __str__(self) -> str:
        return self.title

class Category(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    discount = models.PositiveIntegerField(null = True, blank = True)
    parent = models.ForeignKey('self', on_delete = models.SET_NULL, null = True, blank = True, related_name = "categories")

    def __str__(self) -> str:
        return f'{self.parent} / {self.title}'
        
    def get_absolute_url(self):
        return reverse("category-shop", kwargs={"id": self.pk})

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_images")
    image = models.ImageField(upload_to = "category/images/")

    def __str__(self) -> str:
        return f'{self.category} / {self.pk}'

class Product(models.Model):
    variants = [
        ("None", 'None'),
        ("Size", 'Size'),
        ("Color", 'Color'),
        ("Color-Size", 'Color-Size'),
    ]
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    discount = models.FloatField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "products")
    variant = models.CharField(max_length=50, choices = variants)
    explanation = models.TextField()
    description = models.TextField()
    information = models.TextField()
    is_featured = models.BooleanField(default = False)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    view_count = models.PositiveIntegerField(default = 0)
    def __str__(self) -> str:
        return f'{self.category} / {self.title}'

    def get_absolute_url(self):
        return reverse("shop-detail", kwargs={"id": self.pk})
    
    class Meta:
        ordering = ("-id",)

class Variant(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="variants") 
    color = models.ForeignKey(Color, on_delete = models.CASCADE, related_name = "variants", null = True, blank = True )
    size = models.ForeignKey(Size, on_delete = models.CASCADE, null = True, blank = True, related_name = "variants" )
    quantity = models.IntegerField(default = 1)
    
    def __str__(self) -> str:
        return self.title

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "orders")
    created_time = models.DateTimeField(auto_now = True)

class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete = models.SET_NULL, null = True, related_name = "order_items")
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "order_items")
    count = models.IntegerField(default = 1)

    def __str__(self) -> str:
        return f'{self.variant.title} / {self.count}'

class FavoriteProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "favorite_products")
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "favorite_products")

    def __str__(self) -> str:
        return f'{self.product} / {self.customer}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'product_images')
    image = models.ImageField(upload_to = 'products/images/')

    def __str__(self) -> str:
        return f'{self.product} / {self.pk}'

class AdditionalInfotmation(models.Model):
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "additional_informations")
    def __str__(self) -> str:
        return f'{self.product} / {self.pk}'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "reviews")
    owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = "reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 5)
    review = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        return f'{self.product} / {self.owner}'

    # def clean(self):
    #     if Review.objects.filter(owner=self.owner, product=self.product).exists():
    #         raise ValidationError('This user has added review!')
