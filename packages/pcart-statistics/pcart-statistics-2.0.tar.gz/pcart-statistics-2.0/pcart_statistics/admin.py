from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _
from .models import ProductPageVisit


class ProductPageVisitAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'variant', 'number_of_visits', 'site', 'changed')
    raw_id_fields = ('product', 'variant', 'customer')
    search_fields = ('product', 'variant', 'customer')
    date_hierarchy = 'changed'


admin.site.register(ProductPageVisit, ProductPageVisitAdmin)
