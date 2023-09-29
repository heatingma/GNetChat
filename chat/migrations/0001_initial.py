# Generated by Django 4.2.5 on 2023-09-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=128)),
                (
                    "about_post",
                    models.CharField(
                        default="The author did not set an introduction to the topic",
                        max_length=128,
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="post_image"),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="Profile",
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
                (
                    "about_me",
                    models.TextField(
                        default="There is no Personal Signature here yet. You can add it through settings"
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="profile_image"),
                ),
                ("location", models.CharField(default="Unkown", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Room",
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
                ("name", models.CharField(max_length=128, unique=True)),
                ("owner_name", models.CharField(max_length=128)),
                (
                    "about_room",
                    models.CharField(default="welcome to my chatroom", max_length=128),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="room_image"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name="RoomMessage",
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
                ("content", models.CharField(max_length=512)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "belong_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.post"
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.room"
                    ),
                ),
            ],
        ),
    ]
