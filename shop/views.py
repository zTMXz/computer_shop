from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from .models import Category, Product, PhoneConfiguration, PhoneColors
from cart.forms import CartAddProductForm


def product_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    colors = Product.objects.order_by('ph_color_hex').values_list('ph_color_hex', 'ph_color_name_en').distinct()
    memory = Product.objects.order_by('details__product__memory').values_list('details__product__memory', flat=True).distinct()
    cart_product_form = CartAddProductForm()
    if slug:
        if slug == 'android' or slug == 'iOS':
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        elif slug[0].isnumeric():
            products = products.filter(memory=slug)
        else:
            products = products.filter(ph_color_name_en=slug)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, template_name='shop/product/list.html',
                  context={'category': category,
                           'categories': categories,
                           'products': products,
                           'cart_product_form': cart_product_form,
                           'colors': colors,
                           'memory': memory})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug, )

    phone_configs = PhoneConfiguration.objects.filter(phone_id=id)[0].phone_configurations.all()
    phone_colors = PhoneColors.objects.filter(phone_id=id)[0].phone_colors.all()

    product.details.display = product.details.display.split(';')
    product.details.camera = product.details.camera.split(';')
    product.details.front_cam = product.details.front_cam.split(';')
    product.details.processor = product.details.processor.split(';')
    product.details.size_and_weight = product.details.size_and_weight.split(';')
    product.details.video = product.details.video.split(';')
    product.details.mobile_cnct = product.details.mobile_cnct.split(';')

    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form,
                                                        'phone_configs': phone_configs,
                                                        'phone_colors': phone_colors,
                                                        'range': range(1, product.stock + 1)})


class Search(ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        context['categories'] = Category.objects.all()
        return context
