import os
import requests

from dotenv import load_dotenv

load_dotenv()

def send_telegram_message( message: str) -> None:
    """
    Send a Telegram message
    
    Args:
        token: Telegram bot token
        chat_id: Chat ID to send the message to
        message: Message to send
    """
    
    token = os.getenv("BOT_TOKEN")
    chat_id = int(os.getenv("CHAT_ID"))
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    requests.post(url, data=payload)
    
