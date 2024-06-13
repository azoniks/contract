from django.db import models


# Mietvertrag Stallschreiberstr contract.
class RentContract(models.Model):
    WITH_FURNITURE = 'voll möbliert', 'voll möbliert'
    PARTIALLY_FURNITURE = 'teilmöbliert', 'teilmöbliert'
    WITHOUT_FURNITURE = 'ohne möbel', 'ohne möbel'

    FURNITURE = (WITH_FURNITURE, PARTIALLY_FURNITURE, WITHOUT_FURNITURE)

    landlord = models.CharField(max_length=40, verbose_name='Vermieter')
    renter = models.CharField(max_length=40, verbose_name='Mieter')
    resident = models.CharField(max_length=30, verbose_name='Wohnhaft')
    passport = models.CharField(max_length=20, verbose_name='Passport')
    date_of_expiry = models.DateField(verbose_name='Gültig bis')
    address = models.CharField(max_length=35, verbose_name='Adresse')
    floor = models.CharField(max_length=20, verbose_name='Etage')
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
    iban = models.CharField(max_length=30, verbose_name='IBAN')
    bic = models.CharField(max_length=30, verbose_name='BIC')
    credit_institution = models.CharField(max_length=30, verbose_name='Kreditinstitut')
    purpose = models.CharField(max_length=20, verbose_name='Zweck')
    monthly_rent = models.IntegerField(verbose_name='Monatliche Grundmiete')
    extra_costs = models.IntegerField(verbose_name='Nebenkosten')
    deposit = models.IntegerField(verbose_name='Kaution')
    persons = models.CharField(max_length=200, verbose_name='Personen')
    location = models.CharField(max_length=25, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Mietvertrag'
        verbose_name_plural = 'Mietvertrag'

    def __str__(self):
        return self.landlord


# Maklervertrag Verkauf contract.
class SaleContract(models.Model):
    customer = models.CharField(max_length=50, verbose_name='Kunde')
    address = models.CharField(max_length=50, verbose_name='Adresse')
    object = models.CharField(max_length=70, verbose_name='Objekt')
    land_register = models.CharField(max_length=50, blank=True, verbose_name='Grundbuch')
    length_of_time = models.IntegerField(verbose_name='Dauer')
    location = models.CharField(max_length=25, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Maklervertrag Verkauf'
        verbose_name_plural = 'Maklervertrag Verkauf'

    def __str__(self):
        return self.customer


# Makler Suchauftrag Vorlage contract.
class BrokerSearch(models.Model):
    customer = models.CharField(max_length=50, verbose_name='Kunde')
    location = models.CharField(max_length=25, verbose_name='Ort')
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

    customer = models.CharField(max_length=50, verbose_name='Eigentümer')
    address_customer = models.CharField(max_length=50, verbose_name='Adresse des Eigentümers')
    address = models.CharField(max_length=50, verbose_name='Adresse')
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
