from django.forms import ModelForm
from .models import Review, FavoriteProduct, Payment

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("review", "rating")

class FavoriteProductForm(ModelForm):
    class Meta:
        model = FavoriteProduct
        fields = "__all__"

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = ("order", "customer","amount")