from django.contrib import admin
from .models.product import Product
from .models.customer import Customer
from .models.ui import UI
from .models.disease import Disease
from .models.orders import Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(UI)
admin.site.register(Disease)
admin.site.register(Order)