import os
import time
import requests
import sys
import platform
import socket
import shlex
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env in the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def escape_markdown(text):
    # Escape MarkdownV2 reserved characters
    for char in r"_*[]()~`>#+-=|{}.!" :
        text = text.replace(char, f"\\{char}")
    return text

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "MarkdownV2"
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()

def get_machine_info():
    hostname = socket.gethostname()
    os_info = platform.system() + " " + platform.release()
    return hostname, os_info

def run_task(command_with_args):
    start_time = time.time()
    started_at = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    exit_code = os.system(command_with_args)
    duration = time.time() - start_time

    # Emoji and status message
    if exit_code == 0:
        emoji = "✅"
        status_message = "Success"
    else:
        emoji = "❌"
        status_message = f"Failed \\(exit code {exit_code}\\)"

    hostname, os_info = get_machine_info()

    # Format and escape command string
    escaped_cmd = escape_markdown(command_with_args)

    message = (
        f"{escaped_cmd} completed w status: {status_message} {emoji}\n"
        f"``` {escaped_cmd} ```"
        f"*Status*: `{status_message}`\n"
        f"*Command:* `{escaped_cmd}`\n"
        f"*Started at:* `{started_at}`\n"
        f"*Duration:* `{duration:.2f}` seconds\n"
        f"*Machine:* `{hostname}`\n"
        f"*OS:* `{escape_markdown(os_info)}`"
    )

    send_telegram_message(message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the task/command to run.")
        sys.exit(1)

    task_command = ' '.join(shlex.quote(arg) for arg in sys.argv[1:])
    run_task(task_command)
