# Generated by Django 5.0.4 on 2024-05-23 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0043_remove_studentresponse_awarded_marks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresponse',
            name='marks_awarded',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
