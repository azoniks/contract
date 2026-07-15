from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts_generator', '0006_alter_wgbestaetigung_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='WohnungsuebergabeProtokollArenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_name', models.CharField(max_length=160, verbose_name='Name der/des Mieter(s)')),
                ('apartment_address', models.CharField(max_length=160, verbose_name='Straße und Hausnummer')),
                ('handover_date', models.DateField(verbose_name='Datum der Übergabe')),
                ('defect_status', models.CharField(choices=[('NONE', 'keine Mängel'), ('DEFECTS', 'folgende Mängel')], max_length=7, verbose_name='Mängel festgestellt')),
                ('inspection_rows', models.JSONField(default=list, verbose_name='Wohnungszustand')),
                ('electricity_meter_number', models.CharField(blank=True, max_length=50, verbose_name='Strom - Zählernummer')),
                ('electricity_reading', models.CharField(blank=True, max_length=50, verbose_name='Strom - Stand')),
                ('gas_meter_number', models.CharField(blank=True, max_length=50, verbose_name='Gas - Zählernummer')),
                ('gas_reading', models.CharField(blank=True, max_length=50, verbose_name='Gas - Stand')),
                ('water_meter_number_1', models.CharField(blank=True, max_length=50, verbose_name='Wasser 1 - Zählernummer')),
                ('water_reading_1', models.CharField(blank=True, max_length=50, verbose_name='Wasser 1 - Stand')),
                ('water_meter_number_2', models.CharField(blank=True, max_length=50, verbose_name='Wasser 2 - Zählernummer')),
                ('water_reading_2', models.CharField(blank=True, max_length=50, verbose_name='Wasser 2 - Stand')),
                ('keys_handed_over', models.CharField(blank=True, max_length=240, verbose_name='Übergebene Schlüssel')),
                ('keys_pending', models.CharField(blank=True, max_length=240, verbose_name='Noch zu übergebende Schlüssel')),
                ('notes', models.CharField(blank=True, max_length=240, verbose_name='Sonstige Anmerkungen / Notizen')),
                ('landlord_date', models.DateField(verbose_name='Datum Vermieter')),
                ('tenant_date', models.DateField(verbose_name='Datum Mieter')),
                ('pdf_document', models.FileField(upload_to='pdf_documents')),
            ],
            options={
                'verbose_name': 'Wohnungsübergabe Protokoll ARENDA',
                'verbose_name_plural': 'Wohnungsübergabe Protokoll ARENDA',
            },
        ),
    ]
