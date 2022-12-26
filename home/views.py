from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Count
from django.db.models import Avg

def home(request):
    context = {
        "popular_category": Category.objects.annotate(product_count = Count("products"),category_count = Count("categories")).filter(category_count=0).order_by("-product_count").first(),
        "categories": Category.objects.annotate(category_count = Count("categories")).filter(category_count=0),
        "discount_categories": Category.objects.exclude(discount = None).order_by("-discount")[0:2],
        "discount_categories_part2": Category.objects.exclude(discount = None).order_by("-discount")[2:4],
        "featured_products": Product.objects.annotate(stars = Avg("reviews__rating"), star_half = Avg("reviews__rating")*10, star_half_value = Avg("reviews__rating")-1, review_count = Count("reviews")).filter(is_featured = True).order_by("?")[0:8],
        "recent_products": Product.objects.annotate(stars = Avg("reviews__rating"), star_half = Avg("reviews__rating")*10, star_half_value = Avg("reviews__rating")-1, review_count = Count("reviews")).order_by("-id")[0:8]

    }
    return render(request, 'home.html', context)
