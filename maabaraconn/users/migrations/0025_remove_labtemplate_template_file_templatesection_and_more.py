# Generated by Django 5.0.3 on 2024-04-01 09:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_labtemplate_laboratory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labtemplate',
            name='template_file',
        ),
        migrations.CreateModel(
            name='TemplateSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', models.IntegerField(help_text='The order in which the section appears in the template')),
                ('lab_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='users.labtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='StudentResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='users.templatesection')),
            ],
        ),
    ]
