# Generated by Django 4.1.3 on 2022-11-24 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0003_alter_item_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="List",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="item",
            name="list",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="lists.list",
            ),
        ),
    ]
