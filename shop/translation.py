from modeltranslation.translator import register, TranslationOptions
from .models import Product, PhoneDetails


@register(PhoneDetails)
class PhoneDetailsTranslationOptions(TranslationOptions):
    fields = ('display', 'processor', 'size_and_weight', 'camera', 'video', 'front_cam', 'mobile_cnct')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('ph_color_name',)
