# Generated by Django 3.1.3 on 2020-12-01 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='description',
            field=models.TextField(default='Hello, I am a happy young user who wish to browse the temple of ideas on shaready.fr.', max_length=125),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image_profile',
            field=models.ImageField(default='user-default.svg.png', upload_to=''),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receiving_follow', to=settings.AUTH_USER_MODEL)),
                ('usersFollow', models.ManyToManyField(related_name='users_giving_follow', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]