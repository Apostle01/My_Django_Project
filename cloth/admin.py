from django.contrib import admin
from .models import Cloth, Category


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name',)


@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'slug')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
