from django.db import models
from django.utils.translation import ugettext_lazy as _


class PostalCode(models.Model):
    """
    A model to represent postal codes and their location data.

    Originally based on the Census Bureau's zip code data
    http://www.census.gov/geo/www/gazetteer/gazetteer2010_layout.html#zcta
    """
    country_code = models.CharField(_("country_code"), max_length=2)
    postal_code = models.CharField(_("postal_code"), max_length=20)
    place_name = models.CharField(_("place_name"), max_length=200, blank=True, null=True)
    admin_name1 = models.CharField(_("admin_name1"), max_length=100, blank=True, null=True)
    admin_code1 = models.CharField(_("admin_code1"), max_length=20, blank=True, null=True)
    admin_name2 = models.CharField(_("admin_name2"), max_length=100, blank=True, null=True)
    admin_code2 = models.CharField(_("admin_code2"), max_length=20, blank=True, null=True)
    admin_name3 = models.CharField(_("admin_name3"), max_length=100, blank=True, null=True)
    admin_code3 = models.CharField(_("admin_code3"), max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = _("Postal code")
        verbose_name_plural = _("Postal codes")
        unique_together = (
            ('country_code', 'postal_code'),
        )

    def __str__(self):
        return u"%s" % self.postal_code
