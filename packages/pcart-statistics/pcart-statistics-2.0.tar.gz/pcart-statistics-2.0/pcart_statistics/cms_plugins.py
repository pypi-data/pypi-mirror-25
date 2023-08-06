from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import LastVisitedPluginModel
from .forms import LastVisitedPluginForm


class LastVisitedPluginPublisher(CMSPluginBase):
    model = LastVisitedPluginModel  # model where plugin data are saved
    form = LastVisitedPluginForm
    module = _("Statistics")
    name = _("Last visited products")  # name of the plugin in the interface
    render_template = "statistics/plugins/last_visited_plugin.html"

    def render(self, context, instance, placeholder):
        _context = {}
        _context.update({'parent_context': context})
        _context.update({'instance': instance})
        return _context


plugin_pool.register_plugin(LastVisitedPluginPublisher)
