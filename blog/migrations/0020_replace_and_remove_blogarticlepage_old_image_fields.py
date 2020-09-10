from django.conf import settings
from django.db import migrations


def remove_wagtail_images(apps, _schema_editor):
    WagtailImage = apps.get_model("wagtailimages", "image")
    for image in WagtailImage.objects.all():
        image.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0019_migrate_image_data_to_custom_image_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogarticlepage",
            name="article_photo",
        ),
        migrations.RemoveField(
            model_name="blogarticlepage",
            name="cover_photo",
        ),
        migrations.RenameField(
            model_name="blogarticlepage",
            old_name="new_article_photo",
            new_name="article_photo",
        ),
        migrations.RenameField(
            model_name="blogarticlepage",
            old_name="new_cover_photo",
            new_name="cover_photo",
        ),
        migrations.RunPython(remove_wagtail_images),
    ]
