from django.urls import path
from .views import UserRegisterView,UserLogin,ProductView,CartView,Order
urlpatterns = [
path("auth/register",UserRegisterView.as_view(),name = 'register'),
path("auth/login",UserLogin.as_view(),name = 'login'),
path("products/all",ProductView.as_view(),name = 'products_list'),
path("products/<uuid:id>",ProductView.as_view(),name = 'products_detail'),
path("cart/",CartView.as_view(),name = 'view_cart'),
path("cart/add/<uuid:product_id>",CartView.as_view(),name = 'view_cart'),
path("cart/delete/<uuid:product_id>",CartView.as_view(),name = 'view_cart'),
path("order",Order.as_view(),name = 'place_order')





]