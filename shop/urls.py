from django.urls import path
from .import views

urlpatterns = [
    path('', views.shop, name = 'shop'),
    path('categories/<int:id>/', views.shop, name = 'category-shop'),
    path('<int:id>/', views.shop_detail, name = 'shop-detail'),
    path('<int:id>/add-review/', views.add_review, name = 'add-review'),
    path('<int:id>/add-favorites/', views.add_favorites, name = 'add-favorites'),
    path('favorites/', views.favorite_list, name = 'favorites')
]
