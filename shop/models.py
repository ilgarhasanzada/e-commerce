from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from account.models import Customer

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
    
    @property
    def image(self):
        image = CategoryImage.objects.filter(category = self).first()
        if image:
            return mark_safe(f"<img width=50 src={image.image.url}></img>")

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category_images")
    image = models.ImageField(upload_to = "category/images/")

    def __str__(self) -> str:
        return f'{self.category} / {self.pk}'

    @property
    def parent(self):
        return self.category.parent
    @property
    def title(self):
        return self.category.title
    @property
    def image_detail(self):
        return mark_safe(f"<img width=50 src={self.image.url}></img>")
    @property
    def show_image(self):
        return mark_safe(f"<img width=200 src={self.image.url}></img>")

class Product(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    discount = models.FloatField(null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "products")
    colors = models.ManyToManyField(Color, related_name = "products")
    sizes = models.ManyToManyField(Size, related_name = "products")
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
    @property
    def image(self):
        image = ProductImage.objects.filter(product = self).first()
        if image:
            return mark_safe(f"<img width=50 src={image.image.url}></img>")


class Variant(models.Model):
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="variants") 
    color = models.ForeignKey(Color, on_delete = models.CASCADE, related_name = "variants", null = True, blank = True )
    size = models.ForeignKey(Size, on_delete = models.CASCADE, null = True, blank = True, related_name = "variants" )
    quantity = models.IntegerField(default = 1)
    def __str__(self) -> str:
        return f'{self.product}-{self.color}-{self.size}'
    
    def clean(self) -> None:
        if Variant.objects.filter(color = self.color, size = self.size).exclude(pk = self.pk):
            raise ValidationError("Such an variant is already exists")

    @property
    def category(self):
        return self.product.category
    @property
    def title(self):
        return self.product.title
    @property
    def image(self):
        image = VariantImage.objects.filter(variant = self).first()
        product_image = ProductImage.objects.filter(product = self.product).first()
        if image:
            return mark_safe(f"<img width=50 src={image.image.url}></img>")
        elif product_image:
            return mark_safe(f"<img width=50 src={product_image.image.url}></img>")


class Coupon(models.Model):
    code = models.PositiveBigIntegerField(unique = True)
    variant = models.ForeignKey(Variant, on_delete = models.CASCADE, related_name = "coupons")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)
    discount = models.IntegerField()

    def __str__(self):
        return f'{self.variant} / {self.code}'
    
    def clean(self) -> None:
        if self.discount >= self.variant.price:
            raise ValidationError("The discount cannot be greater than the price")
    @property
    def category(self):
        return self.variant.product.category
    @property
    def title(self):
        return self.variant.product.title
    @property
    def size(self):
        return self.variant.size
    @property
    def color(self):
        return self.variant.color

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "orders")
    created_time = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)

class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete = models.SET_NULL, null = True, related_name = "order_items")
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "order_items")
    count = models.IntegerField(default = 1)
    coupon = models.ForeignKey(Coupon, on_delete = models.SET_NULL,null = True, blank = True, related_name = "order_items")
    def __str__(self) -> str:
        return f'{self.variant} / {self.count}'
    
    def clean(self) -> None:
        if OrderItem.objects.filter(variant = self.variant, order = self.order).exclude(pk = self.pk):
            raise ValidationError("Such an order item is already exists")

    @property
    def price(self):
        return self.variant.price
    @property
    def coupon_code(self):
        return self.coupon.code
    @property
    def category(self):
        return self.variant.product.category
    @property
    def title(self):
        return self.variant.product.title
    @property
    def size(self):
        return self.variant.size
    @property
    def color(self):
        return self.variant.color
    
    @property
    def image(self):
        image = VariantImage.objects.filter(variant = self.variant).first()
        product_image = ProductImage.objects.filter(product = self.variant.product).first()
        if image:
            return mark_safe(f"<img width=50 src={image.image.url}></img>")
        elif product_image:
            return mark_safe(f"<img width=50 src={product_image.image.url}></img>")
    @property
    def show_image(self):
        image = VariantImage.objects.filter(variant = self.variant).first()
        product_image = ProductImage.objects.filter(product = self.variant.product).first()
        if image:
            return mark_safe(f"<img width=200 src={image.image.url}></img>")
        elif product_image:
            return mark_safe(f"<img width=200 src={product_image.image.url}></img>")
        
class Payment(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length = 100)
    address_line_1 = models.CharField(max_length = 100)
    address_line_2 = models.CharField(max_length = 100, null = True, blank = True )
    country = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zip_code = models.PositiveIntegerField(default=0)
    order = models.OneToOneField(Order, on_delete = models.CASCADE, related_name="payment")
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True,  related_name = "payments")
    amount = models.FloatField(default = 0)
    payment_time = models.DateTimeField(auto_now_add = True)
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} / {self.order}"

class FavoriteProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = "favorite_products")
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "favorite_products")

    def __str__(self) -> str:
        return f'{self.product} / {self.customer}'

    @property
    def image(self):
        product_image = ProductImage.objects.filter(product = self.product).first()
        if product_image:
            return mark_safe(f"<img width=50 src={product_image.image.url}></img>")

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'product_images')
    image = models.ImageField(upload_to = 'products/images/')

    def __str__(self) -> str:
        return f'{self.product} / {self.pk}'

    @property
    def category(self):
        return self.product.category
    @property
    def title(self):
        return self.product.title
    @property
    def image_detail(self):
        return mark_safe(f"<img width=50 src={self.image.url}></img>")
    @property
    def show_image(self):
        return mark_safe(f"<img width=200 src={self.image.url}></img>")

class VariantImage(models.Model):
    variant = models.ForeignKey(Variant, on_delete = models.CASCADE, related_name = 'variant_images')
    image = models.ImageField(upload_to = 'variants/images/')

    def __str__(self) -> str:
        return f'{self.variant} / {self.pk}'
    @property
    def category(self):
        return self.variant.product.category
    @property
    def title(self):
        return self.variant.product.title
    @property
    def image_detail(self):
        return mark_safe(f"<img width=50 src={self.image.url}></img>")
    @property
    def show_image(self):
        return mark_safe(f"<img width=200 src={self.image.url}></img>")
    @property
    def size(self):
        return self.variant.size
    @property
    def color(self):
        return self.variant.color

class AdditionalInfotmation(models.Model):
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "additional_informations")
    def __str__(self) -> str:
        return f'{self.product} / {self.pk}'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "reviews")
    owner = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, related_name = "reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 5)
    review = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ("-id",)

    @property
    def category(self):
        return self.product.category
    @property
    def title(self):
        return self.product.title

    def __str__(self) -> str:
        return f'{self.product} / {self.owner}'

    # def clean(self):
    #     if Review.objects.filter(owner=self.owner, product=self.product).exists():
    #         raise ValidationError('This user has added review!')
