import time
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Accounts, Cards
import threading


# Create your views here.

def login_ana(phone, password):
    url1 = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    headers1 = {
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "x-agent-operatingsystem": "M526BRXXU1CVJ7",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "m52xq",
        "x-agent-version": "2022.2.1.2",
        "x-agent-build": "503",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "139",
        "Host": "mobile.vodafone.com.eg",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.1"
    }
    data1 = {
        "username": phone,
        "password": password,
        "grant_type": "password",
        "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        "client_id": "my-vodafone-app"
    }
    req1 = requests.post(url1, headers=headers1, data=data1)
    token = req1.json()['access_token']
    print (token)
    return True, token


def my_task():
    while True:
        print('hello')
        time.sleep(120)
        users = Accounts.objects.all()
        for user in users:
            num = user.username
            passw = user.password
            check, token = login_ana(num, passw)
            url2 = f'https://web.vodafone.com.eg/services/dxl/ramadanpromo/promotion?@type=RamadanHub&channel=website&msisdn={num}'

            headers2 = {
                "Host": "web.vodafone.com.eg",
                "Connection": "keep-alive",
                "msisdn": num,
                "api-host": "PromotionHost",
                "Accept-Language": "AR",
                "Authorization": f"Bearer {token}",
                'Content-Type': 'application/json',
                'x-dtreferer': 'https://web.vodafone.com.eg/spa/portal/hub',
                'Accept': 'application/json',
                'clientId': 'WebsiteConsumer',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; CPH2083) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.94 Mobile Safari/537.36',
                'channel': 'WEB',
                'Referer': 'https://web.vodafone.com.eg/spa/portal/hub',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            req2 = requests.get(url2, headers=headers2).json()
            # print(req2)

            for x in req2:
                try:
                    pattern = x['pattern']
                    # print(pattern)
                    for y in pattern:
                        action = y['action']
                        # print(action)
                        for k in action:
                            characteristics = k['characteristics']
                            # print(characteristics)
                            value1 = (characteristics[0]['value'])
                            # print(value1)
                            value2 = (characteristics[1]['value'])
                            # print(value2)
                            value3 = (characteristics[2]['value'])
                            # print(value3)
                            value4 = (characteristics[3]['value'])
                            # print(value3)
                            if int(value4) in range(199, 9999999999999999):
                                if not Cards.objects.filter(card_number=value4).exists():
                                    Cards.objects.create(card_number=value4, card_value=value2, card_still=value3,
                                                         price=value1)
                except:
                    pass


def login(request):
    if request.method == 'POST':
        number = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            if Accounts.objects.filter(username=number).exists():
                return redirect('cards')
            check, token = login_ana(number, password)
            if check:
                return redirect('cards')
            else:
                messages.error(request, 'Invalid password or number')
                return redirect('login')
        except:
            messages.error(request, 'Invalid password or number')
            return redirect('login')

    return render(request, 'login.html')


def display_cards(request):
    cards = Cards.objects.all().order_by('-card_value','-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(cards, 20)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)

    return render(request, 'display_cards.html', {'cards': cards})

@login_required
def start(request):
    t = threading.Thread(target=my_task)
    t.start()
    return redirect('cards')
