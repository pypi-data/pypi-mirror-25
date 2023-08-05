from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import IubendaStandardPluginModel

class IubendaStandardPlugin(CMSPluginBase):
    model = IubendaStandardPluginModel
    name = _('Iubenda button (standard)')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_iubenda/button.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(IubendaStandardPlugin)
