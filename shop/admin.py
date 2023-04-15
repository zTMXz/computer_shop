from django.contrib import admin
from .models import Category, Product, PhoneConfiguration, PhoneColors, PhoneDetails
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class PhoneConfigInline(admin.TabularInline):
    model = PhoneConfiguration
    list_display = ['id', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    raw_id_fields = ['phone_id']


class PhoneColorInline(admin.TabularInline):
    model = PhoneColors
    list_display = ['id', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    raw_id_fields = ['phone_id']


# @admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'stock', 'available', 'details', 'ph_color_hex', 'ph_color_name']
    list_filter = ['name', 'available']
    list_editable = ['price', 'stock', 'available', 'details', 'ph_color_hex', 'ph_color_name']
    inlines = [PhoneConfigInline, PhoneColorInline]
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

admin.site.register(PhoneConfiguration)
admin.site.register(PhoneColors)
admin.site.register(PhoneDetails)

