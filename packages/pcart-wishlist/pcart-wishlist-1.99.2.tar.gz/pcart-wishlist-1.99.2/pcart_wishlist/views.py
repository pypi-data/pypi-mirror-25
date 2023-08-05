from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from pcart_customers.utils import get_customer
from .models import WishListedProduct


def _add_item_to_wishlist(customer, site, item_id, item_type='product'):
    from pcart_catalog.models import Product, ProductVariant
    variant = product = None
    if item_type == 'variant':
        variant = ProductVariant.objects.get(pk=item_id)
        product = variant.product
    elif item_type == 'product':
        product = Product.objects.get(pk=item_id)

    if not WishListedProduct.objects.filter(
            customer=customer, product=product, variant=variant, site=site).exists():
        WishListedProduct.objects.create(
            customer=customer,
            product=product,
            variant=variant,
            site=site,
        )


def wishlist(request, template_name='customers/wish_list.html'):
    site = get_current_site(request)
    user = request.user
    customer = get_customer(request)

    if 'view' in request.GET:
        template_name = settings.PCART_WISH_LISTS_TEMPLATES[request.GET['view']]

    if request.method == 'POST':
        if 'add-item' in request.POST:
            item_id = request.POST.get('item-id')
            item_type = request.POST.get('item-type')
            if item_id and item_type:
                _add_item_to_wishlist(customer, site, item_id, item_type)
                if not request.is_ajax():
                    return redirect(
                        reverse(
                            'pcart_customers:customer-profile-section',
                            args=('wishlist',)
                        ))
        else:
            for k in request.POST:
                if k.startswith('item-remove-'):
                    _id = k[len('item-remove-'):]
                    WishListedProduct.objects.filter(pk=_id, customer=customer).delete()
            if not request.is_ajax():
                return redirect(
                    reverse(
                        'pcart_customers:customer-profile-section',
                        args=('wishlist',)
                    ))

    items = WishListedProduct.objects.filter(customer=customer)

    context = {
        'user': user,
        'customer': customer,
        'customer_menu': settings.PCART_CUSTOMER_PROFILE_SECTIONS,
        'items': items,
    }
    return render(request, template_name, context)


@csrf_exempt
@require_http_methods(['POST'])
def add_product(request):
    site = get_current_site(request)
    customer = get_customer(request)

    item_id = request.POST.get('item-id')
    item_type = request.POST.get('item-type')

    if item_id and item_type:
        _add_item_to_wishlist(customer, site, item_id, item_type)

    if not request.is_ajax() and 'next' in request.POST:
        return redirect(request.POST['next'])
    return HttpResponse('OK')
