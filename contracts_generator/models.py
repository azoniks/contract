from django.db import models


# Mietvertrag Stallschreiberstr contract.
class RentContract(models.Model):
    landlord = models.CharField(max_length=100, verbose_name='Vermieter')
    renter = models.CharField(max_length=100, verbose_name='Mieter')
    resident = models.CharField(max_length=30, verbose_name='Wohnhaft')
    passport = models.CharField(max_length=20, verbose_name='Passport')
    date_of_expiry = models.DateField(verbose_name='Gültig bis')
    address = models.CharField(max_length=100, verbose_name='Adresse')
    floor = models.CharField(max_length=100, verbose_name='Etage')
    rooms = models.SmallIntegerField(verbose_name='Zimmer')
    balcony = models.SmallIntegerField(verbose_name='Balkon')
    area = models.FloatField(verbose_name='Wohnungsbereich')
    start_date = models.DateField(verbose_name='Beginnt')
    stop_date = models.DateField(verbose_name='Endet')
    iban = models.CharField(max_length=50, verbose_name='IBAN')
    bic = models.CharField(max_length=50, verbose_name='BIC')
    credit_institution = models.CharField(max_length=50, verbose_name='Kreditinstitut')
    purpose = models.CharField(max_length=20, verbose_name='Zweck')
    monthly_rent = models.IntegerField(verbose_name='Monatliche Grundmiete')
    extra_costs = models.IntegerField(verbose_name='Nebenkosten')
    deposit = models.IntegerField(verbose_name='Kaution')
    persons = models.CharField(max_length=500, verbose_name='Personen')
    location = models.CharField(max_length=50, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Mietvertrag Stallschreiberstr'
        verbose_name_plural = 'Mietvertrag Stallschreiberstr'

    def __str__(self):
        return self.landlord


# Maklervertrag Verkauf contract.
class SaleContract(models.Model):
    customer = models.CharField(max_length=100, verbose_name='Kunde')
    object = models.CharField(max_length=100, verbose_name='Objekt')
    land_register = models.CharField(max_length=100, verbose_name='Grundbuch')
    length_of_time = models.IntegerField(verbose_name='Dauer')
    address = models.CharField(max_length=50, verbose_name='Adresse')
    position = models.CharField(max_length=100, verbose_name='Lage')
    location = models.CharField(max_length=50, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Maklervertrag Verkauf'
        verbose_name_plural = 'Maklervertrag Verkauf'

    def __str__(self):
        return self.customer


# Makler Suchauftrag Vorlage contract.
class BrokerSearch(models.Model):
    customer = models.CharField(max_length=100, verbose_name='Kunde')
    location = models.CharField(max_length=50, verbose_name='Ort')
    contract_date = models.DateField(verbose_name='Datum')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Makler Suchauftrag Vorlage'
        verbose_name_plural = 'Makler Suchauftrag Vorlage'

    def __str__(self):
        return self.customer


# Mietersuche Vertrag contract.
class SearchContract(models.Model):
    customer = models.CharField(max_length=100, verbose_name='Eigentümer')
    address_customer = models.CharField(max_length=50, verbose_name='Adresse des Eigentümers')
    address = models.CharField(max_length=50, verbose_name='Adresse')
    floor = models.CharField(max_length=30, verbose_name='Etage')
    rooms = models.IntegerField(verbose_name='Zimmer')
    balcony = models.IntegerField(verbose_name='Balkon')
    area = models.FloatField(verbose_name='Hausbereich')
    deposit = models.IntegerField(verbose_name='Einzahlung')
    purchase_contract = models.CharField(max_length=50, verbose_name='Kaufvertrag')
    land_register = models.CharField(max_length=50, verbose_name='Grundbuchauszug')
    pdf_document = models.FileField(upload_to='pdf_documents')

    class Meta:
        verbose_name = 'Mietersuche Vertrag'
        verbose_name_plural = 'Mietersuche Vertrag'

    def __str__(self):
        return self.customer
