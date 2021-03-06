# Generated by Django 3.2.6 on 2021-08-24 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_twitchuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitchuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='twitchuser',
            name='chat_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='twitchuser',
            name='name_text',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
        ),
    ]
