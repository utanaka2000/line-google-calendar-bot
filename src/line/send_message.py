import os

from dotenv import load_dotenv
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

load_dotenv()

configuration = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

def send_test_message(to, message):
    # Create an instance of the API client
    api_client = ApiClient(configuration=configuration)
    messaging_api = MessagingApi(api_client)

    # Define the message to be sent
    message = TextMessage(text=message)

    # Create a request to send the message
    request = PushMessageRequest(
        to=to,
        messages=[message]
    )

    # Send the message
    messaging_api.push_message(request)

if __name__ == "__main__":
    send_test_message(os.environ["LINE_USER_ID"], "Hello, this is a test message!")
