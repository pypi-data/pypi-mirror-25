from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PCartWishListConfig(AppConfig):
    name = 'pcart_wishlist'
    verbose_name = _('Wish list')
