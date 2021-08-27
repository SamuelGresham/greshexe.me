from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import datetime
from .models import Article, TwitchUser, Message, Project
import os 
from twitchAPI.twitch import Twitch
from twitchAPI.webhook import TwitchWebHook
from pprint import pprint
import requests

data = {
    'SECRET': "REMOVED",
    'CLIENT_ID': "REMOVED",
    "TOKEN": 'REMOVED'
}

twitch = Twitch(data["CLIENT_ID"], data["SECRET"])


# The key for API access. Currently set as a development key during development.
key = "dev_key"

def valid_key(recieved_key):
    if (key == recieved_key):
        return True
    else:
        return False

def index(request):
    return render(request, 'website/home.html')

def blog_home(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:3]
    
    if (latest_article_list.count()  >= 3):
        context = {
            'article1': latest_article_list[0],
            'article2': latest_article_list[1],
            'article3': latest_article_list[2],
            }
    elif (latest_article_list.count() == 2): 
        context = {
            'article1': latest_article_list[0],
            'article2': latest_article_list[1],
            'article3': False,
            }
    elif (latest_article_list.count()  == 1): 
        context = {
            'article1': latest_article_list[0],
            'article2': False,
            'article3': False,
            }
    else: 
        context = {
            'article1': False,
            'article2': False,
            'article3': False,
        }
    return render(request, 'website/blog.html', context)

def article_view (request, url_text):
    latest_article_list = Article.objects.order_by('-pub_date')[:3]
    article = get_object_or_404(Article, pk=url_text)
    if (latest_article_list.count()  >= 3):
        context = {
            'article1': latest_article_list[0],
            'article2': latest_article_list[1],
            'article3': latest_article_list[2],
            'article': article
            }
    elif (latest_article_list.count() == 2): 
        context = {
            'article1': latest_article_list[0],
            'article2': latest_article_list[1],
            'article3': False,
            'article': article
            }
    elif (latest_article_list.count()  == 1): 
        context = {
            'article1': latest_article_list[0],
            'article2': False,
            'article3': False,
            'article': article
            }
    else: 
        context = {
            'article1': False,
            'article2': False,
            'article3': False,
            'article': article
        }

    return render(request, 'website/article.html', context)

def all_articles (request):
    context = {
        'articles': Article.objects.all()
    }

    # TODO add a response once i have made the template 
    return HttpResponse("This feature is not yet complete.")

# Hendle API calls and do the things
# NOTE: Despite this function being exempt from CSRF protection, it is still protected by the private key
@csrf_exempt
def process_api_call(request):
    if (valid_key(request.POST.get("key", ""))):
        request_type = request.POST.get("type", "")
        if (request_type == "message"):
            return greshbot_accept_data(request)
        elif (request_type == "fetch_stats"):
            return greshbot_fetch_stats(request)
        elif (request_type == "fetch_project"):
            return greshbot_fetch_project(request)
        elif (request_type == "fetch_leaderboard"):
            return HttpResponse("1. " + str(greshbot_fetch_leaderboard()[0]) + " 2. " + str(greshbot_fetch_leaderboard()[1]) + " 3. " + str(greshbot_fetch_leaderboard()[2]))
        else:
            return HttpResponseBadRequest("Request type invalid.")
    else:
        return HttpResponseForbidden("Access token invalid.")


# Accepts a request which is sent every time the bot recieves a new chat message
@csrf_exempt
def greshbot_accept_data(request):
    user_name = request.POST.get("name", "")
    message_content = request.POST.get("content", "")
    uid = request.POST.get("uid", "")
    # print(f'Recieved a message from {user_name} saying: {message_content}')

    if (not user_name or not message_content):
        return HttpResponseBadRequest("Missing values")
    
    try:
        user_obj = TwitchUser.objects.get(pk = uid)
    except TwitchUser.DoesNotExist: 
        print("Making user")
        user = TwitchUser(name_text=user_name, chat_count=0, user_id=uid)
        user.save()
        user_obj = TwitchUser.objects.get(pk = uid)

    message = Message(content_text = message_content, message_time = timezone.now(), user=user_name, user_id = uid)
    message.save()

    print(f'Fetched from the database: {user_obj.name_text} and {user_obj.chat_count}')
    
    user_obj.chat_count += 1
    user_obj.save()

    return HttpResponse("Recieved")


# Accepts a request with type "fetch_stats" and returns the stats for a given user
@csrf_exempt
def greshbot_fetch_stats (request): 
    user_name = request.POST.get("name", "")
    uid = request.POST.get("uid", "")

    if (not user_name or not uid):
        return HttpResponseBadRequest("Missing values")

    try:
        count = TwitchUser.objects.get(pk = uid).chat_count
    except TwitchUser.DoesNotExist:
        count = 0

    messages = Message.objects.filter(user_id=uid)

    count_hour = 0

    for message in messages: 
        if (message.message_time >= timezone.now() - datetime.timedelta(hours=1)):
            count_hour += 1
    
    # TODO generalise the response for backend use as well 
    return HttpResponse(f'{user_name} has sent a total of {count} messages. {count_hour} of those have been in the last hour.')

# Accepts a request with type "fetch_project" and returns the current project description
@csrf_exempt
def greshbot_fetch_project (request): 
    project_name = request.POST.get("name", "")

    if (not project_name):
        return HttpResponseBadRequest("Missing values")

    try:
        project_obj = Project.objects.get(pk = project_name)
    except TwitchUser.DoesNotExist: 
        return HttpResponse("Whoops, something isn't configured right. Gresh!!!")

    return HttpResponse(project_obj.description_text)

# Accepts a request with type "fetch_leaderboard" and returns the top 3 twitch chatters
@csrf_exempt
def greshbot_fetch_leaderboard (): 
    names = []
    messages = []
    for user in TwitchUser.objects.all():
        count = 0
        for message in Message.objects.all().filter(user = user.name_text):
            if (message.message_time >= timezone.now() - datetime.timedelta(hours=1)):
                count += 1
        names.append(user.name_text)
        messages.append(count)
    list_of_tuples = sorted(zip(messages, names), reverse=True)[:5]

    chatters = []

    for item in list_of_tuples:
        (num, name) = item
        chatters.append(name)

    return chatters

@csrf_exempt
def greshbot_fetch_leaderboard_alltime ():
    top_chatters = TwitchUser.objects.order_by('-chat_count')[:5]

    response = []

    for chatter in top_chatters:
        response.append(chatter.name_text)

    return response

def overlay_view(request):
    user_dict = twitch.get_users(logins=['greshexe'])["data"]
    uid = user_dict[0]["id"]


    context = {
        'top_chatter': greshbot_fetch_leaderboard()[0],
        'second_chatter': greshbot_fetch_leaderboard()[1],
        'third_chatter': greshbot_fetch_leaderboard()[2],  
    }

    return render(request, 'website/overlay.html', context)

def greshbot_stats_page (request):
    context = {
        'chatter1': greshbot_fetch_leaderboard()[0],
        'chatter2': greshbot_fetch_leaderboard()[1],
        'chatter3': greshbot_fetch_leaderboard()[2],
        'chatter4': greshbot_fetch_leaderboard()[3],
        'chatter5': greshbot_fetch_leaderboard()[4],
        'atchatter1': greshbot_fetch_leaderboard_alltime()[0],
        'atchatter2': greshbot_fetch_leaderboard_alltime()[1],
        'atchatter3': greshbot_fetch_leaderboard_alltime()[2],
        'atchatter4': greshbot_fetch_leaderboard_alltime()[3],
        'atchatter5': greshbot_fetch_leaderboard_alltime()[4],

    }

    return render(request, 'website/stats.html', context)