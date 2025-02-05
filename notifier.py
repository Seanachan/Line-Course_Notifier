import schedule
import time
import scraper  # Import course scraper
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, TextMessage

# LINE API Credentials
configuration = Configuration(access_token="DPklpmYWMt3heA0Gg3jex4AmJ1795pf2hWrPI8yJUyIDRyfeauXnaSlmH4egBv82/AHQ9KiiZGtjDxj8rgyjstc6q9rJdHPWU8eKbMx2NULL2Re/sh3wwXCepeFC+hUg0oYFZ1coodFVq1HE77AN6QdB04t89/1O/w1cDnyilFU=")

# User's LINE ID (Manually get from a message event)
USER_ID = "U22e3d87372c89fc333615090b9114ae5"

def notify_course_opening():
    course_code = "HIST001"  # Change this to your target course
    available_slots = scraper.check_course_availability(course_code)

    if available_slots and available_slots > 0:
        message = f"🚀 Course {course_code} has {available_slots} slots open! Enroll now!"
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message(
                to=USER_ID, messages=[TextMessage(text=message)]
            )
        print(f"Notification sent: {message}")

# Schedule to check every 10 minutes
schedule.every(10).minutes.do(notify_course_opening)

# Keep script running
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)


