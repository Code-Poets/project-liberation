from django.conf import settings
from django.db import migrations
from django.db.models import ForeignKey
from django.db.models.deletion import SET_NULL


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0017_customimage_customrendition"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogarticlepage",
            name="new_article_photo",
            field=ForeignKey(blank=True, null=True, on_delete=SET_NULL, related_name="+", to="blog.CustomImage"),
        ),
        migrations.AddField(
            model_name="blogarticlepage",
            name="new_cover_photo",
            field=ForeignKey(blank=True, null=True, on_delete=SET_NULL, related_name="+", to="blog.CustomImage"),
        ),
    ]
