# Generated by Django 4.2.5 on 2023-09-25 07:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="about_me",
            field=models.TextField(
                default="There is no Personal Signature here yet. You can add it through settings"
            ),
        ),
    ]