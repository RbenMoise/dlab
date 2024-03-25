# Generated by Django 5.0.3 on 2024-03-24 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_enrolled_students_course_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labreport',
            old_name='submittion_file',
            new_name='document',
        ),
        migrations.AddField(
            model_name='labreport',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lab_reports', to='users.course'),
        ),
        migrations.AddField(
            model_name='labreport',
            name='description',
            field=models.TextField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='labreport',
            name='title',
            field=models.CharField(default='Default description', max_length=255),
            preserve_default=False,
        ),
    ]
