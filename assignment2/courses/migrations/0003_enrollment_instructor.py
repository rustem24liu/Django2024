# Generated by Django 5.1.3 on 2024-11-16 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_course_students_alter_course_instructor_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='instructor',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Teacher'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enrollments', to=settings.AUTH_USER_MODEL),
        ),
    ]
