# Generated by Django 2.2.6 on 2019-12-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deallink',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
