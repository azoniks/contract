from django.contrib import admin
from django.core.files.base import ContentFile
from django.utils.html import format_html

from contracts_generator.forms import RentContractAdminForm, SaleContractAdminForm, BrokerSearchAdminForm, \
    SearchContractAdminForm
from contracts_generator.models import RentContract, SaleContract, BrokerSearch, SearchContract
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
