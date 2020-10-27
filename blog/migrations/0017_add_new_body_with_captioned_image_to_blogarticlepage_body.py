from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_remove_blogarticlepage_intro"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogarticlepage",
            name="new_body",
            field=wagtail.core.fields.StreamField([("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")), ("header", wagtail.core.blocks.CharBlock()), ("paragraph", wagtail.core.blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "h1", "h2", "h3", "h4", "h5", "h6", "code", "superscript", "subscript", "strikethrough", "blockquote"])), ("table", wagtail.contrib.table_block.blocks.TableBlock()), ("image", wagtail.core.blocks.StructBlock([("image", wagtail.images.blocks.ImageChooserBlock()), ("caption", wagtail.core.blocks.CharBlock(max_length=128, required=False))]))], blank=True),
        ),
    ]
