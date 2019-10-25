from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.conf import settings
import json
import firebase_admin
import paho.mqtt.subscribe as subscribe
from firebase_admin import db
from firebase_admin import credentials



_CREDENTIAL = credentials.Certificate(settings.FIREBASE_CONFIG)
_OPTIONS = {
    'databaseURL': 'https://gdfor-prod.firebaseio.com/',
    'httpTimeout': 10
    }
firebase_admin.initialize_app(_CREDENTIAL, _OPTIONS)
_LIST_MAC_ADDRESS = db.reference('catraca-obra').get(shallow=True).keys()

def index(request):
    context = {
        'list_mac_address': _LIST_MAC_ADDRESS
    }

    if request.POST:
        mac_address = request.POST.get('mac_address_select')

        return redirect('monitoramento', mac_address)

    return render(request, 'index.html', context)

def room(request, mac_address):
    context = {
        'mac_address': mac_address
    }
    return render(request, 'room.html', context)
