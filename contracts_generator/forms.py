from django import forms

from contracts_generator.models import (
    RentContract,
    SaleContract,
    SaleContractAlleinauftrag,
    BrokerSearch,
    SearchContract,
    WGBestaetigung,
    WohnungsuebergabeProtokollArenda,
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


class WGBestaetigungAdminForm(forms.ModelForm):
    class Meta:
        model = WGBestaetigung
        exclude = ('persons', 'pdf_document')
        widgets = {
            'move_date': forms.DateInput(attrs={'type': 'date'}),
        }

    for row in range(1, 11):
        locals()[f'person_{row}_family_name'] = forms.CharField(
            max_length=80,
            required=row == 1,
            label=f'{row}. Familienname',
        )
        locals()[f'person_{row}_first_name'] = forms.CharField(
            max_length=80,
            required=row == 1,
            label=f'{row}. Vorname',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            for row, person in enumerate(self.instance.persons[:10], start=1):
                self.fields[f'person_{row}_family_name'].initial = person.get('family_name', '')
                self.fields[f'person_{row}_first_name'].initial = person.get('first_name', '')

    def clean(self):
        cleaned = super().clean()
        persons = []
        for row in range(1, 11):
            family = (cleaned.get(f'person_{row}_family_name') or '').strip()
            first = (cleaned.get(f'person_{row}_first_name') or '').strip()
            if bool(family) != bool(first):
                self.add_error(
                    f'person_{row}_first_name' if family else f'person_{row}_family_name',
                    'Familienname und Vorname müssen zusammen ausgefüllt werden.',
                )
            if family and first:
                persons.append({'family_name': family, 'first_name': first})
        cleaned['persons'] = persons
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.persons = self.cleaned_data['persons']
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class WohnungsuebergabeProtokollArendaAdminForm(forms.ModelForm):
    ROOM_NAMES = (
        'Diele/Flur', 'Küche', 'Bad/WC', 'Wohnzimmer', 'Balkon',
        'Schlafzimmer', 'Kinderzimmer', 'Keller', 'Weitere Räume', 'Garage',
    )

    class Meta:
        model = WohnungsuebergabeProtokollArenda
        exclude = ('inspection_rows', 'pdf_document')
        widgets = {
            'handover_date': forms.DateInput(attrs={'type': 'date'}),
            'landlord_date': forms.DateInput(attrs={'type': 'date'}),
            'tenant_date': forms.DateInput(attrs={'type': 'date'}),
        }

    for row, room_name in enumerate(ROOM_NAMES, start=1):
        locals()[f'room_{row}_ok'] = forms.BooleanField(required=False, label=f'{room_name}: in Ordnung')
        locals()[f'room_{row}_defects'] = forms.CharField(
            required=False, max_length=180, label='Folgende Mängel wurden festgestellt',
        )
        locals()[f'room_{row}_remarks'] = forms.CharField(
            required=False, max_length=120, label='Bemerkungen',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            for row, item in enumerate(self.instance.inspection_rows[:10], start=1):
                self.fields[f'room_{row}_ok'].initial = item.get('ok', False)
                self.fields[f'room_{row}_defects'].initial = item.get('defects', '')
                self.fields[f'room_{row}_remarks'].initial = item.get('remarks', '')

    def clean(self):
        cleaned = super().clean()
        cleaned['inspection_rows'] = [
            {
                'ok': bool(cleaned.get(f'room_{row}_ok')),
                'defects': (cleaned.get(f'room_{row}_defects') or '').strip(),
                'remarks': (cleaned.get(f'room_{row}_remarks') or '').strip(),
            }
            for row in range(1, 11)
        ]
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.inspection_rows = self.cleaned_data['inspection_rows']
        if commit:
            instance.save()
            self.save_m2m()
        return instance
