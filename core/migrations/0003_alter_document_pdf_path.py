# Generated by Django 4.2.11 on 2025-01-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_document_pdf_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="pdf_path",
            field=models.CharField(default="default/path/to/pdf", max_length=500),
            preserve_default=False,
        ),
    ]
