# Generated by Django 3.2.6 on 2021-08-21 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_article_img_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='id',
        ),
        migrations.AddField(
            model_name='article',
            name='url_text',
            field=models.CharField(default='oops', max_length=75, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]