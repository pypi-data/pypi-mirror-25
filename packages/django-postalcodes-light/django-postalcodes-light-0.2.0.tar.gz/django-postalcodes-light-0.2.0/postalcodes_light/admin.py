from django.contrib import admin

from .models import PostalCode


class PostalCodeAdmin(admin.ModelAdmin):
    """
    Admin for the postal code model
    """
    search_fields = ['postal_code', 'country_code', 'place_name', 'admin_name1', 'admin_code1']
    list_filter = ['country_code', 'admin_name1']
    list_display = ['postal_code', 'country_code', 'place_name', 'admin_code1']


admin.site.register(PostalCode, PostalCodeAdmin)
