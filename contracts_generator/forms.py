from django import forms

from contracts_generator.models import RentContract, SaleContract, BrokerSearch, SearchContract


class RentContractAdminForm(forms.ModelForm):
    class Meta:
        model = RentContract
        fields = '__all__'

    field_size = {'size': 50}

    landlord = forms.CharField(
        max_length=40, widget=forms.TextInput(attrs=field_size), label='Vermieter')

    renter = forms.CharField(
        max_length=40, widget=forms.TextInput(attrs=field_size), label='Mieter')

    resident = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs=field_size), label='Wohnhaft')

    address = forms.CharField(
        max_length=35, widget=forms.TextInput(attrs=field_size), label='Adresse')

    persons = forms.CharField(
        max_length=200, widget=forms.Textarea(attrs={"cols": "40", "rows": "6"}), label='Personen')

    location = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'size': 30}), label='Ort')


class SaleContractAdminForm(forms.ModelForm):
    class Meta:
        model = SaleContract
        fields = '__all__'

    field_size = {'size': 60}

    customer = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Kunde')

    address = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Adresse')

    object = forms.CharField(
        max_length=70, widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label='Objekt')

    land_register = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Grundbuch', required=False)

    location = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'size': 30}), label='Ort')


class BrokerSearchAdminForm(forms.ModelForm):
    class Meta:
        model = BrokerSearch
        fields = '__all__'

    customer = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'size': 55}), label='Kunde')

    location = forms.CharField(
        max_length=25, widget=forms.TextInput(attrs={'size': 30}), label='Ort')


class SearchContractAdminForm(forms.ModelForm):
    class Meta:
        model = SearchContract
        fields = '__all__'

    field_size = {'size': 60}
    customer = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Eigentümer')

    address_customer = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Adresse des Eigentümers')

    address = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Adresse')

    purchase_contract = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Kaufvertrag', required=False)

    land_register = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs=field_size), label='Grundbuchauszug', required=False)
