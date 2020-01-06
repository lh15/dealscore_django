# Generated by Django 2.2.6 on 2019-12-30 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dealsengine', '0003_auto_20191229_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siteName', models.CharField(max_length=100)),
                ('primaryCrawlUrl', models.CharField(max_length=100)),
                ('crawlIntervalMins', models.IntegerField(default=15)),
            ],
        ),
        migrations.AddField(
            model_name='deallink',
            name='importDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='deallink',
            name='linkPostDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='deallink',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deallink',
            name='siteId',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='dealsengine.DealSite'),
        ),
        migrations.AlterUniqueTogether(
            name='deallink',
            unique_together={('siteId', 'offerId')},
        ),
        migrations.RemoveField(
            model_name='deallink',
            name='siteName',
        ),
    ]