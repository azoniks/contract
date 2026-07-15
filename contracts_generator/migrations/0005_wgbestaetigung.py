from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts_generator', '0004_salecontractalleinauftrag'),
    ]

    operations = [
        migrations.CreateModel(
            name='WGBestaetigung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=120, verbose_name='Familienname, Vorname bzw. Bezeichnung der juristischen Person')),
                ('provider_street', models.CharField(max_length=100, verbose_name='Straße, Haus-Nr.')),
                ('provider_postal_code', models.CharField(max_length=10, verbose_name='PLZ')),
                ('provider_city', models.CharField(max_length=80, verbose_name='Ort')),
                ('owner_name', models.CharField(blank=True, max_length=120, verbose_name='Familienname, Vorname bzw. Bezeichnung der juristischen Person')),
                ('owner_street', models.CharField(blank=True, max_length=100, verbose_name='Straße, Haus-Nr.')),
                ('owner_postal_code', models.CharField(blank=True, max_length=10, verbose_name='PLZ')),
                ('owner_city', models.CharField(blank=True, max_length=80, verbose_name='Ort')),
                ('move_type', models.CharField(choices=[('EINZUG', 'Einzug'), ('AUSZUG', 'Auszug')], max_length=7, verbose_name='Einzug / Auszug')),
                ('move_date', models.DateField(verbose_name='Datum')),
                ('apartment_street', models.CharField(max_length=100, verbose_name='Straße, Haus-Nr.')),
                ('apartment_additional', models.CharField(blank=True, max_length=120, verbose_name='Zusatzangaben (z. B. Wohnungsnummer, Wohnungs-ID)')),
                ('apartment_postal_code', models.CharField(max_length=10, verbose_name='PLZ')),
                ('apartment_city', models.CharField(max_length=80, verbose_name='Ort')),
                ('persons', models.JSONField(default=list, verbose_name='Person/en')),
                ('pdf_document', models.FileField(upload_to='pdf_documents')),
            ],
            options={
                'verbose_name': 'Wohnungsgeberbestätigung',
                'verbose_name_plural': 'Wohnungsgeberbestätigungen',
            },
        ),
    ]
