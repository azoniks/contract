from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts_generator', '0005_wgbestaetigung'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wgbestaetigung',
            options={
                'verbose_name': 'WG Bestätigung',
                'verbose_name_plural': 'WG Bestätigung',
            },
        ),
    ]
