from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import WebFormPluginModel
from .forms import WebFormPluginForm


class WebFormPluginPublisher(CMSPluginBase):
    model = WebFormPluginModel  # model where plugin data are saved
    form = WebFormPluginForm
    module = _("Data collections")
    name = _("Web form")  # name of the plugin in the interface
    render_template = "datacollections/plugins/web_form_plugin.html"

    def render(self, context, instance, placeholder):
        _context = {}
        _context.update({'instance': instance})
        return _context

plugin_pool.register_plugin(WebFormPluginPublisher)
