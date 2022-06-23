from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(10):
            self.send(json.dumps({'message': randint(100, 100000)}))
            sleep(4)

