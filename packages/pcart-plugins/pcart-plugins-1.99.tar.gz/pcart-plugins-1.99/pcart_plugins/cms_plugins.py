from django.utils.translation import ugettext as _
# from django.utils.safestring import mark_safe
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import BigBannerPluginModel
from .forms import BigBannerPluginForm


class BigBannerPluginPublisher(CMSPluginBase):
    model = BigBannerPluginModel  # model where plugin data are saved
    form = BigBannerPluginForm
    module = _("PCart plugins")
    name = _("Big banner")  # name of the plugin in the interface
    render_template = "plugins/banners/big_banner_plugin.html"

    def render(self, context, instance, placeholder):
        from .settings import PCART_BANNER_TEMPLATES
        _context = {
            'template': PCART_BANNER_TEMPLATES[instance.template_name]['template'],
        }
        _context.update({'parent_context': context})
        _context.update({'instance': instance})
        return _context


plugin_pool.register_plugin(BigBannerPluginPublisher)
