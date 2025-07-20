import http.client
import json
import urllib.parse
from config import Config

class TelegramAPI:
    BASE_URL = "api.telegram.org"
    
    def __init__(self, bot_token):
        self.bot_token = bot_token
        
    def _make_request(self, method, params=None):
        conn = http.client.HTTPSConnection(self.BASE_URL)
        params = params or {}
        params = urllib.parse.urlencode(params)
        url = f"/bot{self.bot_token}/{method}?{params}"
        
        conn.request("GET", url)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        
        return json.loads(data)
    
    def get_updates(self, offset=None):
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        return self._make_request("getUpdates", params)
    
    def send_message(self, chat_id, text):
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        return self._make_request("sendMessage", params)
    
    def forward_message(self, chat_id, from_chat_id, message_id):
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        return self._make_request("forwardMessage", params)
    
    def get_chat_administrators(self, chat_id):
        params = {"chat_id": chat_id}
        return self._make_request("getChatAdministrators", params)
