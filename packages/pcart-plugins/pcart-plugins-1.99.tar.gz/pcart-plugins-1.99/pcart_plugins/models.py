from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField


class BigBannerPluginModel(CMSPlugin):
    """
    Represents a big banner with link and a simple descriptions.
    """
    title_1 = models.CharField(_('Title 1'), max_length=255, default='', blank=True)
    title_2 = models.CharField(_('Title 2'), max_length=255, default='', blank=True)
    description = HTMLField(_('Description'), blank=True)
    url = models.CharField(_('URL'), max_length=255, default='', blank=True)
    open_in_new_tab = models.BooleanField(_('Open in new tab'), default=False)
    image = FilerImageField(verbose_name=_('Image'), null=True, blank=True, related_name='big_banners')
    template_name = models.CharField(_('Template name'), default='', blank=True, max_length=100)
    extra_css_classes = models.CharField(_('Extra CSS classes'), max_length=255, default='', blank=True)

    def __init__(self, *args, **kwargs):
        super(BigBannerPluginModel, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.title_1 or self.title_2
