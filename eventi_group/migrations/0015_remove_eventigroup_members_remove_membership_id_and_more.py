# Generated by Django 4.1 on 2023-12-26 09:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventi_group', '0014_alter_eventigroup_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventigroup',
            name='members',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='id',
        ),
        migrations.AddField(
            model_name='membership',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='EventiGroupMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='eventi_group.eventigroup')),
                ('members', models.ManyToManyField(related_name='members', to='eventi_group.membership')),
            ],
            options={
                'verbose_name': 'Eventi Group Members',
                'verbose_name_plural': 'Eventi Group Members',
                'db_table': 'EVT_group_members',
            },
        ),
    ]