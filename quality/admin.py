from django.contrib import admin
from .models import *


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
   model = Backup
   verbose_name = 'Sauvegarde'
   list_per_page = 50

# @admin.register(SelectedProduct)
# class SelectedProductAdmin(admin.ModelAdmin):
#     model = SelectedProduct
#     verbose_name = 'Produit selectionné'



@admin.register(SubstitutProduct)
class SubstitutProductAdmin(admin.ModelAdmin):
    model = SubstitutProduct
    verbose_name = 'Produit substitué'
    list_per_page = 50
    ordering = ['-id']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    verbose_name = 'Table produit'
    list_per_page = 50
    ordering = ['-id']
    search_fields = ['name']


