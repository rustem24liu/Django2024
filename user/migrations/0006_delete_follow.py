# Generated by Django 5.1.1 on 2024-10-10 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_follow_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
