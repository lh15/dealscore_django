# Generated by Django 2.2.6 on 2020-01-08 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0012_dealsite_color_hex'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(blank=True, max_length=30, null=True)),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]