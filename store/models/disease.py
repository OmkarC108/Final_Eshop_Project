from unicodedata import name
from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=300)

    @staticmethod
    def get_disease_name(name):
        if Disease.objects.get(name__icontains=name):
            return Disease.objects.get(name__icontains=name)
        else:
            return None