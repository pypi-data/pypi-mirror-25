from django.urls import reverse
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag
def track_product_visit(item):
    item_type = item.type()
    product_id = variant_id = None
    if item_type == 'product':
        product_id = item.id
    elif item_type == 'variant':
        product_id = item.product_id
        variant_id = item.id

    track_url = reverse('pcart_statistics:track-product-visit')
    if product_id:
        track_url += '?product_id=%s' % product_id
    if variant_id:
        track_url += '&variant_id=%s' % variant_id

    TEMPLATE = '''
<script src="%s"></script>
'''
    return mark_safe(TEMPLATE % track_url)
