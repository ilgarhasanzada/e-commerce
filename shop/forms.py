from django.forms import ModelForm
from .models import Review, FavoriteProduct

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("review", "rating")

class FavoriteProductForm(ModelForm):
    class Meta:
        model = FavoriteProduct
        fields = "__all__"