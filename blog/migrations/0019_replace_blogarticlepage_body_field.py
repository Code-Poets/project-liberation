from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0018_migrate_blockarticlepage_body_data_to_new_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogarticlepage",
            name="body",
        ),
        migrations.RenameField(
            model_name="blogarticlepage",
            old_name="new_body",
            new_name="body"
        ),
        migrations.AlterField(
            model_name="blogarticlepage",
            name="body",
            field=wagtail.core.fields.StreamField([("markdown", wagtailmarkdown.blocks.MarkdownBlock(icon="code")), ("header", wagtail.core.blocks.CharBlock()), ("paragraph", wagtail.core.blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "hr", "link", "document-link", "image", "embed", "h1", "h2", "h3", "h4", "h5", "h6", "code", "superscript", "subscript", "strikethrough", "blockquote"])), ("table", wagtail.contrib.table_block.blocks.TableBlock()), ("image", wagtail.core.blocks.StructBlock([("image", wagtail.images.blocks.ImageChooserBlock()), ("caption", wagtail.core.blocks.CharBlock(max_length=128, required=False))]))], blank=False),
        )
    ]
