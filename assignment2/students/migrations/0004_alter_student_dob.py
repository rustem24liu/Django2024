# Generated by Django 5.1.3 on 2024-11-14 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateTimeField(null=True),
        ),
    ]