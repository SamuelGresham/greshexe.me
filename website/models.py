from django.db import models
import datetime
from django.utils import *

class Article(models.Model):
    url_text = models.CharField(max_length=75, primary_key=True)
    title_text = models.CharField(max_length=100)
    subtitle_text = models.CharField(max_length=50)
    content_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    category = models.CharField(max_length=50)
    img_url = models.CharField(max_length=100, default="")
    def __str__ (self):
        return self.title_text

    def recent(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

class TwitchUser(models.Model):
    user_id = models.CharField(max_length=30, primary_key = True)
    name_text = models.CharField(max_length=25)
    chat_count = models.IntegerField(default=0)

class Message(models.Model):
    user_id = models.CharField(max_length=30)
    content_text = models.TextField()
    message_time = models.DateTimeField()
    user = models.TextField()

class Project(models.Model):
    name_text = models.TextField(primary_key = True)
    description_text = models.TextField()
    technologies_text = models.TextField()