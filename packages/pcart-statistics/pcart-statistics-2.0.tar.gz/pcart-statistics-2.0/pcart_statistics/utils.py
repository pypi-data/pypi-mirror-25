from django.conf import settings
from django.contrib.sites.models import Site
from .models import ProductPageVisit


def clean_visits_history():
    from django.db.models import Count
    site = Site.objects.get_current()
    _limit = getattr(settings, 'PCART_VISITS_HISTORY_LENGTH', 30)
    visits_counts = \
        ProductPageVisit.objects.filter(site=site).order_by('customer').values('customer') \
        .annotate(history_length=Count('customer')).filter(history_length__gt=_limit)

    for v in visits_counts:
        history = ProductPageVisit.objects.filter(customer=v['customer'], site=site).order_by('-changed')[_limit:]
        for entry in history:
            entry.delete()
