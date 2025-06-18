from django.contrib import admin
from .models import Lead, Company
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db import transaction
import csv
from import_export.formats import base_formats

class LeadResource(resources.ModelResource):
    class Meta:
        model = Lead
        import_id_fields = ['mellicode']
        fields = ('first_name', 'last_name', 'city', 'phone', 'phone_number', 'source', 'city', 'requested_products')
        skip_unchanged = True
        report_skipped = True

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
            base_formats.CSV,
        )
        return [f for f in formats if f().can_import()]

    def before_import_row(self, row, **kwargs):
        # Split full name into first_name and last_name
        full_name = row.get('first_name', '')
        if full_name:
            name_parts = full_name.strip().split(' ', 1)
            if len(name_parts) == 2:
                row['first_name'] = name_parts[0]
                row['last_name'] = name_parts[1]
            else:
                row['first_name'] = full_name
                row['last_name'] = ''

        mellicode = row.get('mellicode')
        source = row.get('source')
        requested_products = row.get('requested_products')

        if mellicode and source and requested_products:
            # Check if a lead with the same mellicode, source, and requested_products exists
            existing_leads = Lead.objects.filter(
                mellicode=mellicode,
                source=source
            )
            
            # Get the requested products from the import row
            requested_products_list = [p.strip() for p in requested_products.split(',')]
            
            # Check each existing lead for matching requested products
            for lead in existing_leads:
                lead_products = set(lead.requested_products.values_list('id', flat=True))
                import_products = set(requested_products_list)
                
                if lead_products == import_products:
                    # Skip this row instead of raising an error
                    return False

        return True

    def import_row(self, row, instance_loader, **kwargs):
        # Skip the row if before_import_row returned False
        if not self.before_import_row(row, **kwargs):
            return None
        return super().import_row(row, instance_loader, **kwargs)

class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = LeadResource
    list_display = ('first_name', 'last_name', 'phone_number', 'source', 'city')
    search_fields = ('first_name', 'last_name', 'phone_number', 'mellicode')
    list_filter = ('source', 'city')

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
            base_formats.CSV,
        )
        return [f for f in formats if f().can_import()]

admin.site.register(Lead, LeadAdmin)

admin.site.register(Company)