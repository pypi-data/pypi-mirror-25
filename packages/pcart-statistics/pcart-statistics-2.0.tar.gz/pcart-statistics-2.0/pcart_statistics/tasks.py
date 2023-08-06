from celery import task
from django.contrib.sites.models import Site


@task
def save_product_page_visit(customer_id, product_id, variant_id=None):
    from .models import ProductPageVisit
    site = Site.objects.get_current()
    try:
        visit = ProductPageVisit.objects.get(
            customer_id=customer_id, product_id=product_id, variant_id=variant_id, site=site)
        visit.increase_visits()
    except ProductPageVisit.MultipleObjectsReturned:
        visits = ProductPageVisit.objects.filter(
            customer_id=customer_id, product_id=product_id, variant_id=variant_id, site=site)
        visit = visits.first()
        visit.increase_visits()
        visits.exclude(pk=visit.pk).delete()
    except ProductPageVisit.DoesNotExist:
        visit = ProductPageVisit(
            customer_id=customer_id,
            product_id=product_id,
            variant_id=variant_id,
            site=site,
        )
    visit.save()


# Run this task automatically every 1 hour
@task.periodic_task(run_every=60*60)
def clean_visits_history():
    from .utils import clean_visits_history
    clean_visits_history()
