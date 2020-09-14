# Generated by Django 2.2.14 on 2020-08-04 18:28

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200625_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticlepage',
            name='recommended_articles',
            field=wagtail.core.fields.StreamField([('page', wagtail.core.blocks.PageChooserBlock(can_choose_root=False, page_type=['blog.BlogArticlePage']))], blank=True, null=True),
        ),
    ]