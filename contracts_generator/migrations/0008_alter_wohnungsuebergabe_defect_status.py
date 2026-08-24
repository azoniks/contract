from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts_generator', '0007_wohnungsuebergabeprotokollarenda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wohnungsuebergabeprotokollarenda',
            name='defect_status',
            field=models.CharField(
                blank=True,
                choices=[('NONE', 'keine Mängel'), ('DEFECTS', 'folgende Mängel')],
                max_length=7,
                verbose_name='Mängel festgestellt',
            ),
        ),
    ]
