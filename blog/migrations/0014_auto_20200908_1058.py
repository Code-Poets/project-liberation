# Generated by Django 2.2.14 on 2020-09-08 10:58

from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_blogarticlepage_recommended_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticlepage',
            name='table_of_contents',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blogarticlepage',
            name='body',
            field=wagtail.core.fields.StreamField([('markdown', wagtailmarkdown.blocks.MarkdownBlock(icon='code')), ('header', wagtail.core.blocks.CharBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())]),
        ),
    ]
