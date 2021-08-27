from django.urls import path
from django.urls.resolvers import URLPattern 
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog_home, name='blog'),
    path('blog/all/', views.all_articles, name='all_articles'),
    path('blog/<str:url_text>/', views.article_view, name='article'),
    path('greshbot/overlay/', views.overlay_view, name='overlay'),
    path('greshbot/api/', csrf_exempt(views.process_api_call), name='greshbot'),
    path('greshbot/stats/', views.greshbot_stats_page, name="stats")
]