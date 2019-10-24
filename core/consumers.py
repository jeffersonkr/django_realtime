from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import paho.mqtt.subscribe as subscribe

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))



class MonitoringConsumer(WebsocketConsumer):
    def connect(self):
        self.mac_address = self.scope['url_route']['kwargs']['mac_address']
        self.monitoring_group_name = 'monitoring_%s' % "-".join(self.mac_address.split(':'))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.monitoring_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.monitoring_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        hostname = '192.168.10.165'
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

        async_to_sync(self.channel_layer.group_send)(
            self.monitoring_group_name,
            {
                'type': 'chat_message',
                'message': msg.payload.decode('utf-8')
            }
        )

    # Receive message from WebSocket
    def receive1(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.monitoring_group_name,
            {
                'type': 'monitoring_message',
                'message': message
            }
        )

    # Receive message from room group
    def monitoring_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))