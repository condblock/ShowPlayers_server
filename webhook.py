import requests

def send_webhook(webhook_url, message, logger):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        logger.info(f"Message sent successfully!\nmessage:\n{message}")
    else:
        logger.error(f"Failed to send message with status code {response.status_code}")
        

