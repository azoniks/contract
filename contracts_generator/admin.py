from functools import partial

from django.contrib import admin
from django.core.files.base import ContentFile
from django.utils.html import format_html

from contracts_generator.forms import (
    RentContractAdminForm,
    SaleContractAdminForm,
    SaleContractAlleinauftragAdminForm,
    BrokerSearchAdminForm,
    SearchContractAdminForm,
    WGBestaetigungAdminForm,
    WohnungsuebergabeProtokollArendaAdminForm,
)
from contracts_generator.models import (
    RentContract,
    SaleContract,
    SaleContractAlleinauftrag,
    BrokerSearch,
    SearchContract,
    WGBestaetigung,
    WohnungsuebergabeProtokollArenda,
)
 
from contracts_generator.pdf_utils import PDFWriter


class BaseContractAdmin(admin.ModelAdmin):
    """ Base class for models of contracts. """
    person_name = None
    contract_name = None
    contract = None
    ordering = ('-id',)
    exclude = ['pdf_document']

    def save_model(self, request, obj, form, change):
        pdf_document = self.contract(contracts_info=form.cleaned_data)
        pdf_name = f'{getattr(obj, self.person_name)} ({self.contract_name}).pdf'
        obj.pdf_document.save(pdf_name, ContentFile(pdf_document))
        super().save_model(request, obj, form, change)

    def download_button(self, obj):
        """ Download contract button. """
        pdf_name = f'{getattr(obj, self.person_name)} ({self.contract_name}).pdf'
        pdf_admin_link = format_html(f'<a href="{obj.pdf_document.url}" download="{pdf_name}">{pdf_name}</a>')
        result = pdf_admin_link if obj.pdf_document else 'No file'

        return result

    download_button.short_description = 'Загрузить'


# Mietvertrag Stallschreiberstr contract.
@admin.register(RentContract)
class RentContractAdmin(BaseContractAdmin):
    list_display = ('landlord', 'renter', 'download_button')
    person_name = 'renter'
    contract_name = 'Mietvertrag'
    pdf_writer = PDFWriter()
    contract = pdf_writer.rent_contract
    form = RentContractAdminForm


# Maklervertrag Verkauf contract.
@admin.register(SaleContract)
class SaleContractAdmin(BaseContractAdmin):
    list_display = ('customer', 'download_button')
    person_name = 'customer'
    contract_name = 'Maklervertrag Verkauf'
    pdf_writer = PDFWriter()
    contract = pdf_writer.sale_contract
    form = SaleContractAdminForm


# Maklervertrag Verkauf Alleinauftrag contract.
@admin.register(SaleContractAlleinauftrag)
class SaleContractAlleinauftragAdmin(BaseContractAdmin):
    list_display = ('customer', 'download_button')
    person_name = 'customer'
    contract_name = 'Maklervertrag Verkauf Alleinauftrag'
    pdf_writer = PDFWriter()
    contract = partial(pdf_writer.sale_contract, template_filename='sale_all_contract.pdf')
    form = SaleContractAlleinauftragAdminForm


@admin.register(WGBestaetigung)
class WGBestaetigungAdmin(BaseContractAdmin):
    list_display = ('provider_name', 'move_type', 'move_date', 'download_button')
    person_name = 'provider_name'
    contract_name = 'Wohnungsgeberbestätigung'
    pdf_writer = PDFWriter()
    contract = pdf_writer.wg_bestaetigung
    form = WGBestaetigungAdminForm
    fieldsets = (
        ('1. Angaben zum Wohnungsgeber oder zur beauftragten Person', {
            'fields': (
                'provider_name', 'provider_street',
                ('provider_postal_code', 'provider_city'),
            ),
        }),
        ('2. Angaben zum Eigentümer der Wohnung', {
            'description': 'Nur auszufüllen, wenn der Wohnungsgeber nicht selbst Eigentümer ist.',
            'fields': (
                'owner_name', 'owner_street',
                ('owner_postal_code', 'owner_city'),
            ),
        }),
        ('3. Einzug / Auszug und Wohnung', {
            'fields': (
                ('move_type', 'move_date'), 'apartment_street', 'apartment_additional',
                ('apartment_postal_code', 'apartment_city'),
            ),
        }),
        ('4. Person/en', {
            'fields': tuple(
                (f'person_{row}_family_name', f'person_{row}_first_name')
                for row in range(1, 11)
            ),
        }),
    )


@admin.register(WohnungsuebergabeProtokollArenda)
class WohnungsuebergabeProtokollArendaAdmin(BaseContractAdmin):
    list_display = ('tenant_name', 'handover_date', 'defect_status', 'download_button')
    person_name = 'tenant_name'
    contract_name = 'Wohnungsübergabe Protokoll ARENDA'
    pdf_writer = PDFWriter()
    contract = pdf_writer.wohnungsuebergabe_protokoll_arenda
    form = WohnungsuebergabeProtokollArendaAdminForm
    fieldsets = (
        ('Wohnung und Übergabe', {
            'fields': ('tenant_name', 'apartment_address', ('handover_date', 'defect_status')),
        }),
        *tuple(
            (f'{row}. {room_name}', {
                'fields': ((f'room_{row}_ok', f'room_{row}_defects', f'room_{row}_remarks'),),
            })
            for row, room_name in enumerate(WohnungsuebergabeProtokollArendaAdminForm.ROOM_NAMES, start=1)
        ),
        ('Zählerstände', {
            'fields': (
                ('electricity_meter_number', 'electricity_reading'),
                ('gas_meter_number', 'gas_reading'),
                ('water_meter_number_1', 'water_reading_1'),
                ('water_meter_number_2', 'water_reading_2'),
            ),
        }),
        ('Schlüssel und Notizen', {
            'fields': ('keys_handed_over', 'keys_pending', 'notes'),
        }),
        ('Datum', {
            'fields': (('landlord_date', 'tenant_date'),),
        }),
    )


# Makler Suchauftrag Vorlage contract.
@admin.register(BrokerSearch)
class BrokerSearchAdmin(BaseContractAdmin):
    list_display = ('customer', 'contract_date', 'download_button')
    person_name = 'customer'
    contract_name = 'Makler Suchauftrag Vorlage'
    pdf_writer = PDFWriter()
    contract = pdf_writer.broker_search
    form = BrokerSearchAdminForm


# Mietersuche Vertrag contract.
@admin.register(SearchContract)
class SearchContractAdmin(BaseContractAdmin):
    list_display = ('customer', 'download_button')
    person_name = 'customer'
    contract_name = 'Mietersuche Vertrag'
    pdf_writer = PDFWriter()
    contract = pdf_writer.search_contract
    form = SearchContractAdminForm
