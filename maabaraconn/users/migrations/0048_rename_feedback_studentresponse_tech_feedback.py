# Generated by Django 5.0.4 on 2024-06-27 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_studentresponse_student_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentresponse',
            old_name='feedback',
            new_name='tech_feedback',
        ),
    ]
