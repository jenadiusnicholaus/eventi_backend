# Generated by Django 4.1 on 2023-12-26 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventi_group', '0007_eventigroup_members_eventigroupmembership_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventigroupmembership',
            name='group',
        ),
    ]
