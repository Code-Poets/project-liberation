from django.conf import settings
from django.db import migrations


def move_existing_image_data_to_custom_model(apps, _schema_editor):
    WagtailImage = apps.get_model("wagtailimages", "image")
    CustomImage = apps.get_model("blog", "customimage")
    CustomImage.objects.bulk_create([
        CustomImage(
            title=image.title,
            file=image.file,
            width=image.width,
            height=image.height,
            created_at=image.created_at,
            uploaded_by_user=image.uploaded_by_user,
            tags=image.tags,
            focal_point_x=image.focal_point_x,
            focal_point_y=image.focal_point_y,
            focal_point_width=image.focal_point_width,
            focal_point_height=image.focal_point_height,
            file_size=image.file_size,
            file_hash=image.file_hash,
        ) for image in WagtailImage.objects.all().order_by("pk")
    ])


def assign_new_images_to_articles(apps, _schema_editor):
    CustomImage = apps.get_model("blog", "customimage")
    BlogArticlePage = apps.get_model("blog", "blogarticlepage")
    for blog_article_page in BlogArticlePage.objects.all():
        blog_article_page.new_cover_photo = CustomImage.objects.get(pk=blog_article_page.cover_photo.pk)
        blog_article_page.new_article_photo = CustomImage.objects.get(pk=blog_article_page.article_photo.pk)
        blog_article_page.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0018_add_blogarticlepage_new_image_fields"),
    ]

    operations = [
        migrations.RunPython(move_existing_image_data_to_custom_model),
        migrations.RunPython(assign_new_images_to_articles),
    ]
