
from django.contrib import admin
from django.urls import path
from .views import home, recommend, store, signin, login, logout,index,cart,checkout,orders
urlpatterns = [
    path('', index,name="homepage"),
    path('index', index),
    path('home', home),
    path('store', store),
    path('query', store),
    path('signin', signin),
    path('login', login),
    path('logout', logout),
    path('cart', cart),
    path('rec',recommend),
    path('check-out', checkout),
    path('orders', orders)
]
