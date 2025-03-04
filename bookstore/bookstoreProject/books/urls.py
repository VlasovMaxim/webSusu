from django.urls import path
from . import views
from .views import register, login_view, logout_view, profile, add_to_cart, cart, checkout, orders

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_create'),
    path('update/<int:book_id>/', views.book_update, name='book_update'),
    path('delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("cart/add/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("orders/", orders, name="orders"),

]