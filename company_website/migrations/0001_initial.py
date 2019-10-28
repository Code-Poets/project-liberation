# Generated by Django 2.2.6 on 2019-10-28 15:59

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('front_image', sorl.thumbnail.fields.ImageField(blank=True, default=None, upload_to='company_employees_storage')),
                ('back_image', sorl.thumbnail.fields.ImageField(blank=True, default=None, upload_to='company_employees_storage')),
                ('boss', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(blank=True, unique=True)),
            ],
        ),
    ]
