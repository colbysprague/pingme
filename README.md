pingme

pingme is a lightweight Python utility that runs any shell command and sends a notification to your Telegram account when it completes — with success or failure status, runtime duration, and system info.

Useful for long-running scripts, background jobs, or just keeping tabs on your terminal tasks.

Features

- Sends a Telegram message when your task completes
- Shows an emoji if the task fails (with exit code)
- Includes how long the task took
- Shows the machine name and operating system
- Simple Bash-friendly interface: pingme <your command>

Setup

1. Clone the repo and install dependencies

git clone https://github.com/yourusername/pingme.git
cd pingme
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Set up your .env file

Copy the .env.template to .env and fill in your credentials:

cp .env.template .env

.env file example:

# Your Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Your chat ID (usually your user ID)
TELEGRAM_CHAT_ID=your_chat_id_here

3. Get Your Telegram Bot Token and Chat ID

Bot Token
- Open Telegram
- Search for @BotFather
- Create a new bot: /newbot
- Follow the prompts and copy the token it gives you

Chat ID
- Start a chat with your bot
- Send any message
- Go to this URL in your browser:  
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
- Find "chat":{"id":YOUR_CHAT_ID} in the JSON

Usage

Run a command and get notified:

python pingme.py sleep 5

Or create a Bash alias for convenience:

Add this to your ~/.bashrc or ~/.zshrc:

alias pingme='python /full/path/to/pingme.py'

Now you can run:

pingme sleep 5
