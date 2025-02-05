from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import scraper  # Import scraper.py

app = Flask(__name__)

# LINE API credentials
configuration = Configuration(access_token="DPklpmYWMt3heA0Gg3jex4AmJ1795pf2hWrPI8yJUyIDRyfeauXnaSlmH4egBv82/AHQ9KiiZGtjDxj8rgyjstc6q9rJdHPWU8eKbMx2NULL2Re/sh3wwXCepeFC+hUg0oYFZ1coodFVq1HE77AN6QdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("7644da47c0c178fc8f34adea5e94af13")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature.")
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message.startswith("Check "):
        course_code = user_message.split("Check ")[1]
        available_slots = scraper.check_course_availability(course_code)
        print(available_slots)
        reply_text = (
            f"Course {course_code} has {available_slots} available slots!"
            if available_slots and available_slots > 0
            else f"Course {course_code} is full or unavailable."
        )
    else:
        reply_text = "Send 'Check COURSE_CODE' to check availability."

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

if __name__ == "__main__":
    app.run(port=5000)

