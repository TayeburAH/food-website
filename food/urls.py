from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('pizza/', views.pizza, name='pizza'),
    path('burger/', views.burger, name='burger'),
    path('fried_chicken/', views.fried_chicken, name='fried_chicken'),
    path('french_fries/', views.french_fries, name='french_fries'),
    path('search/', views.search, name='search'),
]
