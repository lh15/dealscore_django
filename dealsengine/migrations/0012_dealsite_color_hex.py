# Generated by Django 2.2.6 on 2020-01-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0011_auto_20200102_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealsite',
            name='color_hex',
            field=models.CharField(default='2C65AF', max_length=6),
            preserve_default=False,
        ),
    ]
