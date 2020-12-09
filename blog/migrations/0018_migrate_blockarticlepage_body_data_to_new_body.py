import json

from django.core import serializers
from django.db import migrations


def move_existing_body_data_to_new_body(apps, _schema_editor):
    BlogArticlePage = apps.get_model("blog", "BlogArticlePage")
    json_articles_data = json.loads(serializers.serialize("json", BlogArticlePage.objects.all()))
    for article_data in json_articles_data:
        article_body = article_data["fields"]["body"]
        new_body_data = [_change_image_data_to_captioned_image_data(block) if block["type"] == "image" else block for block in json.loads(article_body)]
        article = BlogArticlePage.objects.get(pk=article_data["pk"])
        article.new_body.stream_data = new_body_data
        article.save()


def _change_image_data_to_captioned_image_data(block_data):
    image = block_data["value"]
    block_data["value"] = {"image": image, "caption": ""}
    block_data["type"] = "image"
    return block_data


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0017_add_new_body_with_captioned_image_to_blogarticlepage_body"),
    ]

    operations = [
        migrations.RunPython(move_existing_body_data_to_new_body),
    ]
