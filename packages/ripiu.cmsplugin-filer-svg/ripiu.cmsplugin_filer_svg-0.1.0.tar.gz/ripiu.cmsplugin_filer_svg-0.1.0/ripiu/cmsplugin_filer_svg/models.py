from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.file import FilerFileField

class SVGPluginModel(CMSPlugin):
    """
    Base SVG plugin model
    """
    
    file = FilerFileField(
        blank = False, null = False, verbose_name = _('SVG file'),
        help_text = _('Provide an SVG file')
    )
    
    class Meta:
        abstract = True

class FilerSvgInlinePluginModel(SVGPluginModel):
    """
    An inline SVG image
    """
    
    def get_svg_code(self):
        try:
            return self.file.file.read()
        except IOError:
            return ""
    
    def __str__(self):
        return u'Inline SVG'
    
    class Meta:
        verbose_name = _("Inline SVG image")
        verbose_name_plural = _("Inline SVG images")

class FilerSvgImagePluginModel(SVGPluginModel):
    """
    An SVG image
    """
    
    # see cmsplugin_filer_image.models.FilerImage
    alt_text = models.CharField(_("alt text"), null=False, blank=False, max_length=255)
    
    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    
    def __str__(self):
        return self.alt_text
    
    class Meta:
        verbose_name = _("SVG image")
        verbose_name_plural = _("SVG images")
