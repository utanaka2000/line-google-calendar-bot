import os
import textwrap

import dotenv

from src.google_calendar.fetch_calendar_events import fetch_tomorrow_events
from src.line.send_message import send_test_message

dotenv.load_dotenv()


def main(request):
    events = fetch_tomorrow_events()
    if not events:
        return "No events found", 200

    message = textwrap.dedent(f"""\
    あすの予定
    
    {'\n'.join(events)}
    """)

    send_test_message(os.environ["LINE_USER_ID"], message)

    return "OK", 200

if __name__ == "__main__":
    main(None)