import os
import time
import requests
import sys
import platform
import socket
import shlex
import subprocess
from telegram_notifier import TelegramNotifier
from teams_notifier import TeamsNotifier 
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

def run_task(command_with_args, notifier):
    start_time = time.time()
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    escaped_cmd = escape_markdown(command_with_args)

    message = (
        f"`{escaped_cmd}` completed: {status_message} {emoji}\n"
        f"``` {escaped_cmd} ```"
        f"*Status*: `{status_message}`\n"
        f"*Command:* `{escaped_cmd}`\n"
        f"*Started at:* `{started_at}`\n"
        f"*Duration:* `{duration:.2f}` seconds\n"
        f"*Machine:* `{hostname}`\n"
        f"*OS:* `{escape_markdown(os_info)}`"
    )

    notifier.send(message)

def check_for_updates():
    try:
        subprocess.run(["git", "fetch"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        local = subprocess.check_output(["git", "rev-parse", "@"]).strip()
        remote = subprocess.check_output(["git", "rev-parse", "@{u}"]).strip()

        if local != remote:
            print("⚠️  Updates are available in the remote repository. Consider running `git pull`.")
    except subprocess.CalledProcessError:
        # Fail silently if not in a Git repo or upstream not set
        pass
    except Exception as e:
        print("Error checking for updates:", e)

if __name__ == "__main__":
    check_for_updates()

    if len(sys.argv) < 2:
        print("Please provide the task/command to run.")
        sys.exit(1)

    task_command = ' '.join(shlex.quote(arg) for arg in sys.argv[1:])
    notifier = TeamsNotifier()
    run_task(task_command, notifier)

