# Generated by Django 5.1.3 on 2024-11-16 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0003_enrollment_instructor'),
        ('students', '0004_alter_student_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('D', 'Done'), ('A', 'Absent'), ('E', 'Excused'), ('L', 'Late')], max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='students.student')),
            ],
        ),
    ]
