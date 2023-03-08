# Generated by Django 2.2.17 on 2021-07-27 12:59

from django.db import migrations, models


def copy_title_to_page_title(apps, _schema_editor):
    BlogArticlePage = apps.get_model("blog", "BlogArticlePage")

    BlogArticlePage.objects.all().update(
        page_title=models.Subquery(BlogArticlePage.objects.filter(pk=models.OuterRef("pk")).values("title")[:1])
    )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20210324_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticlepage',
            name='page_title',
            field=models.CharField(default='Article title', help_text="The page title as you'd like it to be seen by the public ", max_length=1000),
            preserve_default=False,
        ),
        migrations.RunPython(copy_title_to_page_title),
    ]