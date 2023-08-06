from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import BigBannerPluginModel


def get_banner_template_choices():
    from .settings import PCART_BANNER_TEMPLATES
    result = []
    for k in PCART_BANNER_TEMPLATES:
        result.append((
            k,
            PCART_BANNER_TEMPLATES[k].get('label') or
            PCART_BANNER_TEMPLATES[k].get('template')
        ))
    return result


class BigBannerPluginForm(forms.ModelForm):
    model = BigBannerPluginModel

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BigBannerPluginForm, self).__init__(*args, **kwargs)
        self.fields['template_name'] = forms.ChoiceField(
            choices=get_banner_template_choices(),
            label=_('Template name'),
        )
