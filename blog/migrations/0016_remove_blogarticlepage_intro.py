# Generated by Django 2.2.14 on 2020-09-22 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20200920_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogarticlepage',
            name='intro',
        ),
    ]