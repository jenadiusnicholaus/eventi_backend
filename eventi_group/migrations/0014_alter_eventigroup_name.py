# Generated by Django 4.1 on 2023-12-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventi_group', '0013_alter_eventigroup_options_alter_eventigroup_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventigroup',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]