# Generated by Django 4.2.5 on 2023-10-24 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_friend_request_groups_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='groups_name',
            field=models.CharField(default='NONE', max_length=50),
        ),
    ]
