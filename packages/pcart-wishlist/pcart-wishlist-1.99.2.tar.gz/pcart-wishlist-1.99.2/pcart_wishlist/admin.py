from django.contrib import admin
# from django.utils.translation import ugettext_lazy as _
from .models import WishListedProduct


class WishListedProductAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'variant', 'site', 'added')
    date_hierarchy = 'added'
    search_fields = ('customer', 'product', 'variant')
    raw_id_fields = ('product', 'variant', 'customer')


admin.site.register(WishListedProduct, WishListedProductAdmin)
