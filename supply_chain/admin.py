from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Organization, Product, Transaction

admin.site.register(Organization)
admin.site.register(Product)
admin.site.register(Transaction)
