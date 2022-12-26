from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Product, Review, Category, Color, Size, FavoriteProduct
from django.db.models import Avg, Count
from .forms import ReviewForm
from django.core.paginator import Paginator
from .filters import ProductFilter
def shop(request, id = None):
    sorting = request.GET.get("sorting")
    page_count = request.GET.get("page_count")
    if not page_count:
        page_count=10
    if id:
        products = Product.objects.filter(category = id)
    else:
        products = Product.objects.all()
    products = ProductFilter(request.GET, queryset = products).qs
    products = products.annotate(stars = Avg("reviews__rating"), star_half = Avg("reviews__rating")*10, star_half_value = Avg("reviews__rating")-1, review_count = Count("reviews"))
    if sorting:
        products = products.order_by(sorting)
    else:
        products = products.order_by("-id")
    categories = Category.objects.filter(parent = None)
    paginator = Paginator(products, page_count)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    context = { 
        "filter": ProductFilter,
        "products": products,
        "colors": Color.objects.all(),
        "sizes": Size.objects.all(),
        "categories": categories,
    }
    return render(request, 'shop.html', context)

def shop_detail(request, id):
    product = Product.objects.annotate(stars = Avg("reviews__rating"), star_half = Avg("reviews__rating")*10, star_half_value = Avg("reviews__rating")-1, review_count = Count("reviews")).get(id = id)
    reviews = Review.objects.filter(product = product)
    paginator = Paginator(reviews, 4)
    page_number = request.GET.get("page")
    reviews = paginator.get_page(page_number)
    nearby_products = Product.objects.annotate(stars = Avg("reviews__rating"), star_half = Avg("reviews__rating")*10, star_half_value = Avg("reviews__rating")-1, review_count = Count("reviews")).filter(category = product.category).exclude(id=id)
    product.view_count+=1
    product.save()
    form = ReviewForm()
    context = { 
        "product": product,
        "reviews": reviews,
        "categories": Category.objects.filter(parent = None),
        "nearby_products":nearby_products,
        "form": form,
    }
    return render(request, 'shop-detail.html', context)

def add_review(request, id):
    product = Product.objects.get(id = id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.owner = request.user
            review.product = product
            review.save()
        return redirect(product.get_absolute_url())

def add_favorites(request, id):
    product = FavoriteProduct.objects.filter(customer = request.user.customer,product = Product.objects.get(id = id))
    if product:
        product.delete()
    else:
        FavoriteProduct.objects.create(customer = request.user.customer,product = Product.objects.get(id = id)).save()
    return redirect("shop")
def favorite_list(request):
    return render(request, 'favorites.html')