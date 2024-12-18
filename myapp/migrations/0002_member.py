# Generated by Django 5.1.3 on 2024-12-05 10:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('membership_type', models.CharField(max_length=50)),
                ('profile_image', models.ImageField(upload_to='profile_images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
            ],
        ),
    ]
