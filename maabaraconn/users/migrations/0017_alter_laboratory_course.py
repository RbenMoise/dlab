# Generated by Django 5.0.3 on 2024-03-27 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_laboratory_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratory',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laboratories', to='users.course'),
        ),
    ]
