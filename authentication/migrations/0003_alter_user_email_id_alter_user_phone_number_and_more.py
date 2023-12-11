# Generated by Django 4.1 on 2023-12-02 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_id',
            field=models.EmailField(max_length=254, verbose_name='Email ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=25),
        ),
    ]