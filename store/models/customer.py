import email
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Customer(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=500)
    password= models.CharField(max_length=500)
    
    def register(self):
        self.save()
    
    @staticmethod
    def get_customer_by_email(email):
        if email:
           return Customer.objects.get(email=email)
        else:
            return False

    def isExist(self):
        if Customer.objects.filter(email=self.email):
           return Customer.objects.filter(email=self.email)
        else:
            return False