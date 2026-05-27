# Generated for CialloChat deployment-safe uploaded images.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moments", "0004_comment_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="status",
            name="uploaded_image_data_url",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
    ]
