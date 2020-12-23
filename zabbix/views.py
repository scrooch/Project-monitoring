import requests
from django.shortcuts import render
from django.http import HttpResponse
from pyzabbix import ZabbixAPI, ZabbixAPIException

def index(request):
    #ZABBIX API
    url = 'http://192.168.0.28/zabbix'
    def Get_host(id):
        result = zapi.item.get(itemids=id)
        for data in result:
            speed = int(data['lastvalue'])/1000000
            return "%.2f" % speed

    def Get_item(id):
        results = zapi.item.get(itemids=id)
        for datas in results:
            temp = datas['lastvalue']
            return temp

    zapi = ZabbixAPI(url)  # addr serwera
    zapi.login("Admin", "zabbix")
    zapi.session.verify = False  # nie spr popr cert
    try:
        speed_dawid = Get_host(32110)
        speed_scrooch = Get_host(31768)
        temperatura_dom = float(Get_item(31632))
        wilgotnosc_dom = float(Get_item(31653))
    except Exception as e:
        print(e)
    zapi.user.logout()

    #WEATHER API
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6d8281cc6c1e64651911ca9034726dea"
    city = 'Luzino, PL'

    r = requests.get(url.format(city)).json()
    pogoda_api = {
        'miasto': city,
        'opis': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'temperatura': r['main']['temp'],
        'wilgotnosc': r['main']['humidity'],
        'jakub': speed_scrooch,
        'dawid': speed_dawid,
        'dom_temp': temperatura_dom,
        'dom_wil': wilgotnosc_dom
    }
    content = {'pogoda_api': pogoda_api}

    return render(request, 'pogoda/weather.html', content)
