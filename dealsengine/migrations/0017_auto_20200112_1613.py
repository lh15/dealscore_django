# Generated by Django 2.2.6 on 2020-01-13 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0016_deallink_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deallink',
            name='link_post_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deallink',
            name='primary_category',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='deallink',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dealsengine.DealSite'),
        ),
        migrations.AlterField(
            model_name='deallink',
            name='sub_title',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
