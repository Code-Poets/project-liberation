# Generated by Django 2.2.6 on 2019-10-29 19:50

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company_website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('position', models.CharField(max_length=64)),
                ('quote', models.CharField(max_length=300)),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, default=None, upload_to='testimonials/customers-profile-pictures')),
            ],
        ),
    ]
