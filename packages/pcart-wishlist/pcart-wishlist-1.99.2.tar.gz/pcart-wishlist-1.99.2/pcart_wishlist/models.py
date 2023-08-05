from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
import uuid


class WishListedProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        'pcart_catalog.Product', verbose_name=_('Product'), related_name='wishlisted', on_delete=models.CASCADE)
    variant = models.ForeignKey(
        'pcart_catalog.ProductVariant', verbose_name=_('Variant'), related_name='wishlisted', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    customer = models.ForeignKey(
        'pcart_customers.Customer', verbose_name=_('Customer'), related_name='wishlisted')
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), on_delete=models.PROTECT, related_name='wishlisted')

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Wish list product')
        verbose_name_plural = _('Wish list products')
        ordering = ['-added']

    def __str__(self):
        if self.variant:
            return str(self.variant)
        else:
            return str(self.product)
