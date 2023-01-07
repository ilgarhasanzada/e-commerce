from django.shortcuts import render, redirect
from .models import Product, Review, Category, Color, Size, FavoriteProduct, OrderItem, Variant, Order, Coupon
from django.db.models import Avg, Count, Sum, F
from .forms import ReviewForm, PaymentForm
from django.core.paginator import Paginator
from .filters import ProductFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def shop(request, id = None):
    sorting = request.GET.get("sorting")
    page_count = request.GET.get("page_count")
    if not page_count:
        page_count=10
    if id:
        products = Product.objects.filter(category = id)
        colors = Color.objects.annotate(product_count = Count("products")).filter(products__category = id)
        sizes = Size.objects.annotate(product_count = Count("products")).filter(products__category = id)
    else:
        products = Product.objects.all()
        colors = Color.objects.annotate(product_count = Count("products")).all()
        sizes = Size.objects.annotate(product_count = Count("products")).all()
    products = ProductFilter(request.GET, products).qs
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
        "colors": colors,
        "sizes": sizes,
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
            review.owner = request.user.customer
            review.product = product
            review.save()
        return redirect(product.get_absolute_url())
@login_required
def add_favorites(request, id):
    url = request.META.get("HTTP_REFERER")
    product = FavoriteProduct.objects.filter(customer = request.user.customer,product = Product.objects.get(id = id))
    if product:
        product.delete()
    else:
        FavoriteProduct.objects.create(customer = request.user.customer,product = Product.objects.get(id = id)).save()
    return redirect(str(url)[:-1] + f"#product{id}")

def favorite_list(request):
    return render(request, 'favorites.html')

def order_list(request):
    order = Order.objects.filter(customer = request.user.customer, is_active = True).last()
    if not order:
        return redirect("home")
    order_items = OrderItem.objects.filter(order = order, order__customer = request.user.customer).annotate(c_price = F("count")*(F("variant__price")-F("coupon__discount")),total_price = F("count")*F("variant__price"), total_discount = F("count")*F("coupon__discount"))
    if request.method == "POST":
        try:
            coupon = Coupon.objects.get(code = request.POST.get("coupon_code"), is_active = True)
            for order_item in order_items:
                if order_item.variant == coupon.variant:
                    order_item.coupon = coupon
                    order_item.save()
        except:
            messages.error(request, "Coupon code is not correct!")
    order_items = OrderItem.objects.filter(order = order, order__customer = request.user.customer).annotate(c_price = F("count")*(F("variant__price")-F("coupon__discount")),total_price = F("count")*F("variant__price"), total_discount = F("count")*F("coupon__discount")).order_by("-id")
    prices = order_items.aggregate(discount =  Sum("total_discount"), sub_total = Sum("total_price"), shipping = (Sum("total_price")-Sum("total_discount"))*0.15, total = (Sum("total_price")-Sum("total_discount"))*1.15, total_without_discount = Sum("total_price")*1.15, shipping_without_discount = Sum("total_price")*0.15)
    context = {
        "order_items": order_items,
        "order": order,
        "sub_total": prices["sub_total"],
        "shipping": prices["shipping"],
        "total": prices["total"],
        "discount": prices["discount"],
        "total_without_discount": prices["total_without_discount"],
        "shipping_without_discount": prices["shipping_without_discount"]
    }
    return render(request, 'order-list.html', context)

def variant_add_order(request, id):
    product = Product.objects.get(id = id)
    if request.method == "POST":
        color = request.POST.get("color")
        count = request.POST.get("count")
        size = request.POST.get("size")
        order = Order.objects.filter(customer = request.user.customer, is_active = True).last()
        variant = Variant.objects.filter(product = product, size = size, color = color).first()
        if not variant:
            return redirect(product.get_absolute_url())
        if not order:
            Order.objects.create(customer = request.user.customer, is_active = True).save()
            order = Order.objects.filter(customer = request.user.customer, is_active = True).last()
        order_item = OrderItem.objects.filter(order = order, variant = variant).first()
        if order_item:
            order_item.count += int(count)
            order_item.save()
        else:
            OrderItem.objects.create(order = order, variant = variant, count = count).save()
    return redirect(product.get_absolute_url())

def increase_quantity_of_order_item(request, id):
    item = OrderItem.objects.get(id = id)
    item.count+=1
    item.save()
    return redirect("order-list")

def decrease_quantity_of_order_item(request, id):
    item = OrderItem.objects.get(id = id)
    item.count-=1
    if item.count>0:
        item.save()
    else:
        item.delete()
    order = Order.objects.annotate(item_count = Count("order_items")).filter(customer = request.user.customer, is_active = True).last()
    if order.item_count<1:
        order.is_active = False
        order.save()
        return redirect("home")
    return redirect("order-list")

def delete_order_item(request, id):
    OrderItem.objects.get(id = id).delete()
    order = Order.objects.annotate(item_count = Count("order_items")).filter(customer = request.user.customer, is_active = True).last()
    if order.item_count<1:
        order.is_active = False
        order.save()
        return redirect("home")
    return redirect("order-list")

def checkout(request):
    order = Order.objects.filter(customer = request.user.customer,is_active = True, ).last()
    if not order:
        return redirect("home")
    order_items = OrderItem.objects.filter(order = order, order__customer = request.user.customer).annotate(c_price = F("count")*(F("variant__price")-F("coupon__discount")),total_price = F("count")*F("variant__price"), total_discount = F("count")*F("coupon__discount"))
    prices = order_items.aggregate(discount =  Sum("total_discount"), sub_total = Sum("total_price"), shipping = (Sum("total_price")-Sum("total_discount"))*0.15, total = (Sum("total_price")-Sum("total_discount"))*1.15, total_without_discount = Sum("total_price")*1.15, shipping_without_discount = (Sum("total_price")*0.15))
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            print(form)
            checkout = form.save(commit = False)
            checkout.order = order
            checkout.customer = request.user.customer
            if prices["total"]:
                checkout.amount = prices["total"]
            else:
                checkout.amount = prices["total_without_discount"]
            for order_item in order_items:
                if order_item.variant.quantity < order_item.count:
                    messages.error(request, "Stokda kifayet qeder mehsul yoxdur")
                    return redirect('checkout')
                order_item.variant.quantity -= order_item.count
                order_item.variant.save()
            checkout.save()
            order.is_active = False
            order.save()
    context = {
        "form": PaymentForm,
        "order_items": order_items,
        "sub_total": prices["sub_total"],
        "shipping": prices["shipping"],
        "total": prices["total"],
        "discount": prices["discount"],
        "total_without_discount": prices["total_without_discount"],
        "shipping_without_discount": prices["shipping_without_discount"]
    }
    return render(request, "checkout.html", context)