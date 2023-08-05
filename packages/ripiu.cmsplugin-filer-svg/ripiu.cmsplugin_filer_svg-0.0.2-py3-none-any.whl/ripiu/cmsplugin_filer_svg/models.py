from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.file import FilerFileField

class FilerSvgImagePluginModel(CMSPlugin):
    """
    An SVG image
    """
    file = FilerFileField(
        blank = False, null = False, verbose_name = _('SVG file'),
        help_text = _('Provide an SVG file')
    )
    
    # see cmsplugin_filer_image.models.FilerImage
    alt_text = models.CharField(_("alt text"), null=False, blank=False, max_length=255)
    # description = models.TextField(_("description"), blank=True, null=True)
    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    
    def __str__(self):
        return self.alt_text
    
    class Meta:
        verbose_name = _("SVG image")
        verbose_name_plural = _("SVG images")
