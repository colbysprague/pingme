import os
import json
import requests
from dotenv import load_dotenv
from notifier import Notifier

class TeamsNotifier(Notifier):
    def __init__(self):
        # Load environment variables from a .env file in the current directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)

        self.webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("Missing TEAMS_WEBHOOK_URL in .env")

    def send(self, message):
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "PingMe Notification",
            "themeColor": "0076D7",
            "sections": [
                {
                    "activityTitle": "📣 PingMe Task Notification",
                    "text": message
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
