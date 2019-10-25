from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
import paho.mqtt.subscribe as subscribe

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def subscribe_once(mac_address):
    hostname = "192.168.10.198"
    msg = subscribe.simple(
        topics=f'monitoramento/{mac_address}', 
        retained=True, 
        hostname=hostname,
        port=1883, 
        keepalive=60, 
        auth={
            'username': 'iot-autodoc',
            'password': 'IOTautodoc19!'
            }
        )
    print(msg)

    return msg.payload.decode('utf-8')
