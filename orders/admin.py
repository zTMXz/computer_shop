import os

from django.contrib import admin
from .models import Order, OrderItem
from django.db.models import Count
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from computer_store import settings

import csv
import matplotlib.pyplot as plt
import base64
import io


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_history_diagrams(modeladmin, request, queryset):
    order_data = OrderItem.objects.values('product__name').annotate(count=Count('product__name'))

    labels = []
    sizes = []

    for data in order_data:
        labels.append(data['product__name'])
        sizes.append(data['count'])

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    filename = f'order_history_{datetime.now().strftime("%d-%m-%Y")}'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    filepath = filepath.replace('\\', '/')
    plt.savefig(filepath)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    img_dgrm = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')

    return render(request, template_name='analytics.html', context={'path': img_dgrm})

order_history_diagrams.short_description = 'Diagram to png'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv, order_history_diagrams]

admin.site.register(Order, OrderAdmin)