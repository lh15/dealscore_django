# Generated by Django 2.2.6 on 2019-12-30 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0004_auto_20191230_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deallink',
            name='importDate',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
