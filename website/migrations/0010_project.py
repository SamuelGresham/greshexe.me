# Generated by Django 3.2.6 on 2021-08-24 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_alter_message_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.TextField()),
                ('description_text', models.TextField()),
                ('technologies_text', models.TextField()),
            ],
        ),
    ]
