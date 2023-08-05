from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin

class IubendaStandardPluginModel(CMSPlugin):
    """
    Iubenda standard embedding option
    """
    
    user_id = models.CharField(
        _('user id'), max_length=400, default='', blank=False,
        help_text=_('Your user ID on Iubenda')
    )
    
    def __str__(self):
        return self.user_id
    
    class Meta:
        verbose_name = _('Iubenda button (standard)')
        verbose_name_plural = _('Iubenda buttons (standard)')
