# Generated by Django 3.1.3 on 2020-11-25 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(default='', max_length=200),
        ),
    ]