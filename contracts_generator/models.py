from django.db import models


# Mietvertrag Stallschreiberstr contract.
class RentContract(models.Model):
    WITH_FURNITURE = 'voll möbliert', 'voll möbliert'
    PARTIALLY_FURNITURE = 'teilmöbliert', 'teilmöbliert'
    WITHOUT_FURNITURE = 'ohne möbel', 'ohne möbel'

    FURNITURE = (WITH_FURNITURE, PARTIALLY_FURNITURE, WITHOUT_FURNITURE)

    landlord = models.CharField(max_length=90, verbose_name='Vermieter')
    renter = models.CharField(max_length=90, verbose_name='Mieter')
    resident = models.CharField(max_length=50, verbose_name='Wohnhaft')
    passport = models.CharField(max_length=30, verbose_name='Passport')
    date_of_expiry = models.DateField(verbose_name='Gültig bis')
    address = models.CharField(max_length=50, verbose_name='Adresse')
    floor = models.CharField(max_length=30, verbose_name='Etage')
    rooms = models.SmallIntegerField(verbose_name='Zimmer')
    kitchen = models.SmallIntegerField(verbose_name='Küche')
    corridor = models.IntegerField(verbose_name='Korridor')
    balcony = models.SmallIntegerField(verbose_name='Balkon')
    bathroom = models.SmallIntegerField(verbose_name='Badezimmer')
    utility_room = models.SmallIntegerField(verbose_name='Keller')
    area = models.FloatField(verbose_name='Wohnungsbereich')
    furniture = models.CharField(max_length=50, choices=FURNITURE)
    start_date = models.DateField(verbose_name='Beginnt')
    stop_date = models.DateField(verbose_name='Endet')
    rent_stop_date = models.DateField(verbose_name='Kündigungsdatum der Miete')
    recipient = models.CharField(max_length=90, verbose_name='Empfänger')
    iban = models.CharField(max_length=50, verbose_name='IBAN')
    bic = models.CharField(max_length=50, verbose_name='BIC')
    credit_institution = models.CharField(max_length=70, verbose_name='Kreditinstitut')
    purpose = models.CharField(max_length=70, verbose_name='Zweck')
    monthly_rent = models.IntegerField(verbose_name='Monatliche Grundmiete')
    extra_costs = models.IntegerField(verbose_name='Nebenkosten')
    deposit = models.IntegerField(verbose_name='Kaution')
    persons = models.CharField(max_length=200, verbose_name='Personen')
    location = models.CharField(max_length=35, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Mietvertrag'
        verbose_name_plural = 'Mietvertrag'

    def __str__(self):
        return self.landlord


# Maklervertrag Verkauf contract.
class SaleContract(models.Model):
    customer = models.CharField(max_length=90, verbose_name='Kunde')
    address = models.CharField(max_length=60, verbose_name='Adresse')
    object = models.CharField(max_length=70, verbose_name='Objekt')
    land_register = models.CharField(max_length=50, blank=True, verbose_name='Grundbuch')
    length_of_time = models.IntegerField(verbose_name='Dauer')
    location = models.CharField(max_length=35, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Maklervertrag Verkauf'
        verbose_name_plural = 'Maklervertrag Verkauf'

    def __str__(self):
        return self.customer


# Maklervertrag Verkauf Alleinauftrag contract.
class SaleContractAlleinauftrag(models.Model):
    customer = models.CharField(max_length=90, verbose_name='Kunde')
    address = models.CharField(max_length=60, verbose_name='Adresse')
    object = models.CharField(max_length=70, verbose_name='Objekt')
    land_register = models.CharField(max_length=50, blank=True, verbose_name='Grundbuch')
    length_of_time = models.IntegerField(verbose_name='Dauer')
    location = models.CharField(max_length=35, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Maklervertrag Verkauf Alleinauftrag'
        verbose_name_plural = 'Maklervertrag Verkauf Alleinauftrag'

    def __str__(self):
        return self.customer


class WGBestaetigung(models.Model):
    EINZUG = 'EINZUG', 'Einzug'
    AUSZUG = 'AUSZUG', 'Auszug'
    MOVE_TYPES = (EINZUG, AUSZUG)

    provider_name = models.CharField(
        max_length=120,
        verbose_name='Familienname, Vorname bzw. Bezeichnung der juristischen Person',
    )
    provider_street = models.CharField(max_length=100, verbose_name='Straße, Haus-Nr.')
    provider_postal_code = models.CharField(max_length=10, verbose_name='PLZ')
    provider_city = models.CharField(max_length=80, verbose_name='Ort')

    owner_name = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Familienname, Vorname bzw. Bezeichnung der juristischen Person',
    )
    owner_street = models.CharField(max_length=100, blank=True, verbose_name='Straße, Haus-Nr.')
    owner_postal_code = models.CharField(max_length=10, blank=True, verbose_name='PLZ')
    owner_city = models.CharField(max_length=80, blank=True, verbose_name='Ort')

    move_type = models.CharField(max_length=7, choices=MOVE_TYPES, verbose_name='Einzug / Auszug')
    move_date = models.DateField(verbose_name='Datum')
    apartment_street = models.CharField(max_length=100, verbose_name='Straße, Haus-Nr.')
    apartment_additional = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Zusatzangaben (z. B. Wohnungsnummer, Wohnungs-ID)',
    )
    apartment_postal_code = models.CharField(max_length=10, verbose_name='PLZ')
    apartment_city = models.CharField(max_length=80, verbose_name='Ort')

    persons = models.JSONField(default=list, verbose_name='Person/en')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'WG Bestätigung'
        verbose_name_plural = 'WG Bestätigung'

    def __str__(self):
        return f'{self.provider_name} - {self.move_date:%d.%m.%Y}'


class WohnungsuebergabeProtokollArenda(models.Model):
    NO_DEFECTS = 'NONE', 'keine Mängel'
    DEFECTS = 'DEFECTS', 'folgende Mängel'
    DEFECT_CHOICES = (NO_DEFECTS, DEFECTS)

    tenant_name = models.CharField(max_length=160, verbose_name='Name der/des Mieter(s)')
    apartment_address = models.CharField(max_length=160, verbose_name='Straße und Hausnummer')
    handover_date = models.DateField(verbose_name='Datum der Übergabe')
    defect_status = models.CharField(max_length=7, choices=DEFECT_CHOICES, verbose_name='Mängel festgestellt')
    inspection_rows = models.JSONField(default=list, verbose_name='Wohnungszustand')
    electricity_meter_number = models.CharField(max_length=50, blank=True, verbose_name='Strom - Zählernummer')
    electricity_reading = models.CharField(max_length=50, blank=True, verbose_name='Strom - Stand')
    gas_meter_number = models.CharField(max_length=50, blank=True, verbose_name='Gas - Zählernummer')
    gas_reading = models.CharField(max_length=50, blank=True, verbose_name='Gas - Stand')
    water_meter_number_1 = models.CharField(max_length=50, blank=True, verbose_name='Wasser 1 - Zählernummer')
    water_reading_1 = models.CharField(max_length=50, blank=True, verbose_name='Wasser 1 - Stand')
    water_meter_number_2 = models.CharField(max_length=50, blank=True, verbose_name='Wasser 2 - Zählernummer')
    water_reading_2 = models.CharField(max_length=50, blank=True, verbose_name='Wasser 2 - Stand')
    keys_handed_over = models.CharField(max_length=240, blank=True, verbose_name='Übergebene Schlüssel')
    keys_pending = models.CharField(max_length=240, blank=True, verbose_name='Noch zu übergebende Schlüssel')
    notes = models.CharField(max_length=240, blank=True, verbose_name='Sonstige Anmerkungen / Notizen')
    landlord_date = models.DateField(verbose_name='Datum Vermieter')
    tenant_date = models.DateField(verbose_name='Datum Mieter')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Wohnungsübergabe Protokoll ARENDA'
        verbose_name_plural = 'Wohnungsübergabe Protokoll ARENDA'

    def __str__(self):
        return f'{self.tenant_name} - {self.handover_date:%d.%m.%Y}'


# Makler Suchauftrag Vorlage contract.
class BrokerSearch(models.Model):
    customer = models.CharField(max_length=90, verbose_name='Kunde')
    location = models.CharField(max_length=35, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Makler Suchauftrag Vorlage'
        verbose_name_plural = 'Makler Suchauftrag Vorlage'

    def __str__(self):
        return self.customer


# Mietersuche Vertrag contract.
class SearchContract(models.Model):

    WITH_FURNITURE = 'voll möbliert$с мебелью', 'voll möbliert'
    PARTIALLY_FURNITURE = 'teilmöbliert$частично меблированная', 'teilmöbliert'
    WITHOUT_FURNITURE = 'ohne möbel$без мебели', 'ohne möbel'

    FURNITURE = (WITH_FURNITURE, PARTIALLY_FURNITURE, WITHOUT_FURNITURE)

    customer = models.CharField(max_length=90, verbose_name='Eigentümer')
    address_customer = models.CharField(max_length=60, verbose_name='Adresse des Eigentümers')
    address = models.CharField(max_length=60, verbose_name='Adresse')
    floor = models.CharField(max_length=30, verbose_name='Etage')
    rooms = models.IntegerField(verbose_name='Zimmer')
    corridor = models.IntegerField(verbose_name='Korridor')
    balcony = models.IntegerField(verbose_name='Balkon')
    bathroom = models.SmallIntegerField(verbose_name='Badezimmer')
    furniture = models.CharField(max_length=50, choices=FURNITURE)
    area = models.FloatField(verbose_name='Gesamtfläche')
    deposit = models.IntegerField(verbose_name='Kaltmiete')
    purchase_contract = models.CharField(max_length=50, blank=True, verbose_name='Kaufvertrag')
    land_register = models.CharField(max_length=50, blank=True, verbose_name='Grundbuchauszug')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Mietersuche Vertrag'
        verbose_name_plural = 'Mietersuche Vertrag'

    def __str__(self):
        return self.customer
