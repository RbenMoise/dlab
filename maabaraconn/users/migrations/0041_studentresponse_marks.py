# Generated by Django 5.0.4 on 2024-05-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_remove_labtemplate_enrolled_students_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresponse',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
