# Generated by Django 4.1 on 2023-12-26 09:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventi_group', '0016_alter_eventigroup_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventigroupmembers',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
