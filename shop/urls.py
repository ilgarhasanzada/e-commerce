from django.urls import path
from .import views

urlpatterns = [
    path('', views.shop, name = 'shop'),
    path('categories/<int:id>/', views.shop, name = 'category-shop'),
    path('<int:id>/', views.shop_detail, name = 'shop-detail'),
    path('<int:id>/add-review/', views.add_review, name = 'add-review'),
    path('<int:id>/add-favorites/', views.add_favorites, name = 'add-favorites'),
    path('favorites/', views.favorite_list, name = 'favorites'),
    path('order/', views.order_list, name = 'order-list'),
    path('<int:id>/variant-add-order/', views.variant_add_order, name = 'variant-add-order-list'),
    path('order-items/<int:id>/increase/', views.increase_quantity_of_order_item, name = 'increase_quantity_of_order_item'),
    path('order-items/<int:id>/decrease/', views.decrease_quantity_of_order_item, name = 'decrease_quantity_of_order_item'),
    path('order-items/<int:id>/delete/', views.delete_order_item, name = 'delete_order_item'),
    path('checkout/', views.checkout, name = 'checkout'),
]
