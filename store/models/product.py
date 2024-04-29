from winreg import QueryInfoKey
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500, default='')
    image = models.ImageField(upload_to='uploads/products/')
     
   
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_name(name):
        if name:
            return Product.objects.filter(name__icontains=name)
        else:
            return Product.objects.all()

    @staticmethod
    def get_products_by_name(name):
        if Product.objects.filter(name__icontains=name):
            lst = set(Product.objects.filter(name__icontains=name))
            print(lst)
            for p in lst:
                return p
       

    @staticmethod
    def get_products_by_id(ids):
        if ids:
            return Product.objects.filter(id__in=ids)
        else:
            return None