import base64
from django.shortcuts import render, redirect
from django.conf import settings
# from django.urls import reverse
from django.http import HttpResponse
from pcart_customers.utils import get_customer
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import ProductPageVisit


HISTORY_COOKIE_NAME = 'visited_products'


def visited_products(request, template_name='customers/includes/visited_products.html'):
    user = request.user
    if user.is_authenticated():
        customer = get_customer(request)

        history = ProductPageVisit.objects.filter(customer=customer).order_by('-changed')
        context = {
            'user': user,
            'customer': customer,
            'history': history,
        }
    else:
        from pcart_catalog.models import Product, ProductVariant
        history_cookie = request.COOKIES.get(HISTORY_COOKIE_NAME, '')
        if history_cookie:
            history_cookie = base64.b64decode(history_cookie).decode('utf8')

        id_pairs = [x for x in history_cookie.split(';') if x]
        history = []

        for id_pair in id_pairs:
            ids = id_pair.split(':')
            if id_pair and id_pair[-1] == ':':
                # Simple product (not variant)
                try:
                    product = Product.objects.get(pk=ids[0])
                    history.append({
                        'product': product,
                        'variant': None,
                    })
                except Product.DoesNotExist:
                    pass
            else:
                # Seems like variant
                try:
                    product = Product.objects.get(pk=ids[0])
                    variant = ProductVariant.objects.get(pk=ids[1], product=product)
                    history.append({
                        'product': product,
                        'variant': variant,
                    })
                except Product.DoesNotExist:
                    pass
                except ProductVariant.DoesNotExist:
                    pass

        context = {
            'user': user,
            'history': history,
        }
    return render(request, template_name, context)


@csrf_exempt
@require_http_methods(['GET'])
def track_product_visit(request):
    OUTPUT = '''
    /* Product page visit tracking. */
    '''
    response = HttpResponse(OUTPUT, content_type='text/javascript')

    product_id = request.GET.get('product_id')
    variant_id = request.GET.get('variant_id')

    if request.user.is_authenticated():
        from .tasks import save_product_page_visit
        customer = get_customer(request)
        customer_id = customer.id

        save_product_page_visit.delay(
            customer_id=customer_id,
            product_id=product_id,
            variant_id=variant_id,
        )
    else:
        _limit = getattr(settings, 'PCART_VISITS_HISTORY_LENGTH', 30)

        history = request.COOKIES.get(HISTORY_COOKIE_NAME, '')
        if history:
            history = base64.b64decode(history).decode('utf8')

        id_pair = '%s:%s' % (product_id or '', variant_id or '')
        id_pairs = [x for x in history.split(';') if x]
        if id_pair not in id_pairs:
            id_pairs = [id_pair] + id_pairs

        id_pairs = id_pairs[:_limit]
        history = base64.b64encode(';'.join(id_pairs).encode('utf8')).decode('utf8')
        response.set_cookie(HISTORY_COOKIE_NAME, history)

    return response
