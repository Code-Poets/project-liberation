# Generated by Django 2.2.17 on 2020-12-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_website', '0011_auto_20201202_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='bio',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
