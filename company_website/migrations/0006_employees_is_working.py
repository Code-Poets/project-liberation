# Generated by Django 2.2.8 on 2019-12-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_website', '0005_pageseo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='is_working',
            field=models.BooleanField(default=True),
        ),
    ]
