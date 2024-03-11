"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py

from django.urls import path
from django.contrib import admin
from my_blog import views
from django.conf.urls.static import static
from django.conf import settings
import uuid
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('login/', views.loginView),
    path('logout/', views.logoutView),
    path('register/', views.RegisterView),
    path('', views.product_list, name='product_list'),
    path('create/product/', views.create_product, name='create_product'),
    path('product/details/<uuid:id>/', views.product_details, name='product_details'),
    path("product/delete/<uuid:id>/", views.delete_product, name='delete_product'),
    path("add/category/", views.add_category, name='add_category'),
    path('product/<str:category>/', views.product_list_category, name='product_list_category'),
    path('search/', views.search_by, name='search_by'),
    path('product/add_favourite/<uuid:product_id>/', views.add_favourite, name='add_favourite'),
    path('product/remove_favourite/<uuid:product_id>/', views.remove_favourite, name='remove_favourite'),
    path('favourite_product/', views.favourite_product, name='favourite_product'),

    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),  name='password_reset'),
    path('password/reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password/reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),  name='password_reset_confirm'),
    path('password/reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),  name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
