from django.contrib import admin

from .models import Article, Message, Project, TwitchUser

# Register your models here.
admin.site.register(Article)
admin.site.register(Project)
admin.site.register(Message)
admin.site.register(TwitchUser)