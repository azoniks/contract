from django import forms

from contracts_generator.models import RentContract, SaleContract, BrokerSearch, SearchContract


class RentContractAdminForm(forms.ModelForm):
    class Meta:
        model = RentContract
        fields = '__all__'

    field_size = {'size': 60}

    landlord = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Vermieter')

    renter = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Mieter')

    resident = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Wohnhaft')

    address = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Adresse')

    persons = forms.CharField(
        max_length=100, widget=forms.Textarea(attrs={"cols": "40", "rows": "6"}), label='Personen')


class SaleContractAdminForm(forms.ModelForm):
    class Meta:
        model = SaleContract
        fields = '__all__'

    field_size = {'size': 60}

    customer = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Kunde')

    object = forms.CharField(
        max_length=100, widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label='Objekt')

    land_register = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Grundbuch')

    address = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Adresse')

    position = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Lage')


class BrokerSearchAdminForm(forms.ModelForm):
    class Meta:
        model = BrokerSearch
        fields = '__all__'

    customer = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'size': 60}), label='Kunde')


class SearchContractAdminForm(forms.ModelForm):
    class Meta:
        model = SearchContract
        fields = '__all__'

    field_size = {'size': 60}
    customer = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Eigentümer')

    address_customer = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Adresse des Eigentümers')

    address = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Adresse')

    purchase_contract = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Kaufvertrag')

    land_register = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs=field_size), label='Grundbuchauszug')
