from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
import uuid


class ProductPageVisit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        'pcart_catalog.Product', verbose_name=_('Product'), related_name='visits', on_delete=models.CASCADE)
    variant = models.ForeignKey(
        'pcart_catalog.ProductVariant', verbose_name=_('Variant'), related_name='visits', on_delete=models.CASCADE,
        null=True, blank=True,
    )

    customer = models.ForeignKey(
        'pcart_customers.Customer', verbose_name=_('Customer'), related_name='visits',
        on_delete=models.CASCADE)
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), on_delete=models.PROTECT, related_name='visits')

    number_of_visits = models.PositiveIntegerField(_('Number of visits'), default=1)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Product page visit')
        verbose_name_plural = _('Product pages visits')
        ordering = ['-changed']

    def __str__(self):
        if self.variant:
            return str(self.variant)
        else:
            return str(self.product)

    def increase_visits(self, delta=1, save=False):
        self.number_of_visits += delta
        if save:
            self.save()


class LastVisitedPluginModel(CMSPlugin):
    """ Represents a plugin with a list of last visited products for current customer.
    """
    title = models.CharField(_('Title'), max_length=255, default='', blank=True)

    def __init__(self, *args, **kwargs):
        super(LastVisitedPluginModel, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
