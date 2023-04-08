from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.urls import reverse_lazy

from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    return render(request, template_name='shop/product/list.html',
                  context={'category': category,
                   'categories': categories,
                   'products': products,
                   'cart_product_form': cart_product_form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})


class Search(ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    def get_queryset(self):
        print(self)
        print(Product.objects.filter(name__icontains=self.request.GET.get("q")))
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


