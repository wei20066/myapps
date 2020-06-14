from django.contrib import admin
from django.urls import path
from login import views

app_name = 'login'
urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
]