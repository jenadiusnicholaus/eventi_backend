# Generated by Django 4.1 on 2023-12-18 04:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventi_group', '0003_eventigroupplages_plaged_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventigroupplages',
            options={'verbose_name': 'Eventi Group Plages', 'verbose_name_plural': 'Eventi Group Plages'},
        ),
        migrations.AlterUniqueTogether(
            name='eventigroupplages',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='eventigroupplages',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='group_plages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='eventigroupplages',
            name='member',
        ),
    ]
