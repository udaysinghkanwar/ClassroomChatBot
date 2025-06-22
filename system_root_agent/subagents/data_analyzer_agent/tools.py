from __future__ import print_function
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Any, Dict, List, Optional

# If modifying scopes, delete the token.json file.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]


def add_to_calendar(event_title: str, due_date: str) -> dict:
    """
    Adds an all-day event to Google Calendar.
    Args:
        event_title (str): The event title.
        due_date (str): The event date in YYYY-MM-DD format.
    Returns:
        dict: Status and message.
    """

    print("\n\n\nADD TO CALENDER GOT CALLED: " + due_date)

    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
    # Load credentials (adjust as needed for your project)
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.events'])

    service = build('calendar', 'v3', credentials=creds)
    event = {
        "summary": event_title,
        "start": {"date": due_date},
        "end": {"date": due_date},  # Google Calendar expects end date to be exclusive, so you may want to add 1 day
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return {"status": "success", "eventId": created_event.get("id")}



#     add_to_calender("my_cool_event", "2025-06-23")