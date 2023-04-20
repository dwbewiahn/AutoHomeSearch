import json
import http.client, urllib

class PushoverNotifier:

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read_config_file(self):
        # Open pushover_config file to get the keys for the API
        with open(self.config_file_path) as f:
            return json.load(f)

    def get_app_token(self):
        config = self.read_config_file()   
        return config['app_token']
    
    def get_user_key(self):
        config = self.read_config_file()
        return config['user_key']

    def send_notification(self, message):
        APP_TOKEN = self.get_app_token()
        USER_KEY = self.get_user_key()
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": APP_TOKEN,
            "user": USER_KEY,
            "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
        print()






