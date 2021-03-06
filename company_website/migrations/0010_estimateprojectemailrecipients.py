# Generated by Django 2.2.16 on 2020-10-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_website', '0009_auto_20201019_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimateProjectEmailRecipients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Estimate Project Email Recipients',
                'verbose_name_plural': 'Estimate Project Email Recipients',
            },
        ),
    ]
