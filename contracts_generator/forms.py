from django import forms

from contracts_generator.models import (
    RentContract,
    SaleContract,
    SaleContractAlleinauftrag,
    BrokerSearch,
    SearchContract,
)


class RentContractAdminForm(forms.ModelForm):
    class Meta:
        model = RentContract
        fields = '__all__'

    field_size = {'size': 90}

    landlord = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs=field_size), label='Vermieter')

    renter = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs=field_size), label='Mieter')

    resident = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Wohnhaft')

    address = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Adresse')

    recipient = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs=field_size), label='Empfänger')

    iban = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='IBAN')

    bic = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='BIC')

    credit_institution = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs=field_size), label='Kreditinstitut')

    purpose = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs=field_size), label='Zweck')

    persons = forms.CharField(
        max_length=200, widget=forms.Textarea(attrs={"cols": "40", "rows": "6"}), label='Personen')

    location = forms.CharField(
        max_length=35, widget=forms.TextInput(attrs={'size': 35}), label='Ort')


class SaleContractAdminForm(forms.ModelForm):
    class Meta:
        model = SaleContract
        fields = '__all__'

    field_size = {'size': 90}

    customer = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs=field_size), label='Kunde')

    address = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs=field_size), label='Adresse')

    object = forms.CharField(
        max_length=70, widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label='Objekt')

    land_register = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Grundbuch', required=False)

    location = forms.CharField(
        max_length=35, widget=forms.TextInput(attrs={'size': 35}), label='Ort')


class SaleContractAlleinauftragAdminForm(forms.ModelForm):
    class Meta:
        model = SaleContractAlleinauftrag
        fields = '__all__'

    field_size = {'size': 90}

    customer = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs=field_size), label='Kunde')

    address = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs=field_size), label='Adresse')

    object = forms.CharField(
        max_length=70, widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label='Objekt')

    land_register = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Grundbuch', required=False)

    location = forms.CharField(
        max_length=35, widget=forms.TextInput(attrs={'size': 35}), label='Ort')


class BrokerSearchAdminForm(forms.ModelForm):
    class Meta:
        model = BrokerSearch
        fields = '__all__'

    customer = forms.CharField(
        max_length=90, widget=forms.TextInput(attrs={'size': 90}), label='Kunde')

    location = forms.CharField(
        max_length=35, widget=forms.TextInput(attrs={'size': 35}), label='Ort')


class SearchContractAdminForm(forms.ModelForm):
    class Meta:
        model = SearchContract
        fields = '__all__'

    field_size = {'size': 60}
    customer = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs=field_size), label='Eigentümer')

    address_customer = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs=field_size), label='Adresse des Eigentümers')

    address = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs=field_size), label='Adresse')

    purchase_contract = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Kaufvertrag', required=False)

    land_register = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Grundbuchauszug', required=False)
