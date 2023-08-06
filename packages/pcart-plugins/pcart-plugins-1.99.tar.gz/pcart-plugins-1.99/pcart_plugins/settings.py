from django.conf import settings
from django.utils.translation import ugettext_lazy as _


BANNER_TEMPLATES = {
    'default_big': {
        'template': 'plugins/banners/default_big.html',
        'label': _('Default big'),
    },
    'default_middle': {
        'template': 'plugins/banners/default_middle.html',
        'label': _('Default middle'),
    },
}
PCART_BANNER_TEMPLATES = getattr(settings, 'PCART_BANNER_TEMPLATES', BANNER_TEMPLATES)
