from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    path('<slug:slug>/',
         views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',
         views.product_detail,
         name='product_detail'),
]
