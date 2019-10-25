from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import paho.mqtt.subscribe as subscribe

class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mac_address = self.scope['url_route']['kwargs']['mac_address']
        self.monitoring_group_name = 'monitoring_%s' % "-".join(self.mac_address.split(':'))

        # Join room group
        await self.channel_layer.group_add(
            self.monitoring_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.monitoring_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        hostname = '192.168.10.198'
        msg = subscribe.simple(
            topics=f'monitoramento/{self.mac_address}', 
            qos=0,
            retained=False, 
            hostname=hostname,
            port=1883, 
            keepalive=60, 
            auth={
                'username': 'iot-autodoc',
                'password': 'IOTautodoc19!'
                }
            )

        await self.channel_layer.group_send(
            self.monitoring_group_name,
            {
                'type': 'monitoring_message',
                'message': msg.payload.decode('utf-8')
            }
        )

    # Receive message from room group
    async def monitoring_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))