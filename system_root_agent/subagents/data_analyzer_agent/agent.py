from __future__ import print_function

"""
Data Analyzer Agent

This agent is responsible for answering user questions by using information
from course work and announcements agents.
"""

from google.adk.agents import LlmAgent
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Any, Dict, List, Optional
from dateutil import parser as date_parser





# If modifying scopes, delete the token.json file.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]


def add_to_calendar(assignment_name: str, due_date: str) -> dict:
    """
    Adds the assignment to the Google Calendar.
    Args:
        assignment_name (str): The assignment name.
        due_date (str): The assignment's due date in YYYY-MM-DD format.
    Returns:
        dict: Status and message.
    """

    print("\n\n\nADD TO CALENDER GOT CALLED: " + due_date)

    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
    # Load credentials (adjust as needed for your project)
    creds = Credentials.from_authorized_user_file('drive_config.json', ['https://www.googleapis.com/auth/calendar.events'])

    service = build('calendar', 'v3', credentials=creds)
    event = {
        "summary": assignment_name,
        "start": {"date": due_date},
        "end": {"date": due_date},  # Google Calendar expects end date to be exclusive, so you may want to add 1 day
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return {"status": "success", "eventId": created_event.get("id")}



#     add_to_calender("my_cool_event", "2025-06-23")



# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Data Analyzer Agent
data_analyzer_agent = LlmAgent(
    name="DataAnalyzerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Data Analyzer Agent.
    
    Your role is to answer user questions by using information from:
    - Course work information: {course_work_info}
    - Announcements information: {announcements_info}
        
    When a user asks a question:
    1. Check if the information needed is available in the course work or announcements data
    2. Use the relevant information to provide a helpful answer
    3. If the information is FULLY not available, let the user know what you can and cannot answer. Only do in extreme cases. 
    4. Always be helpful and provide context when possible
        
    You can answer questions about:
    - Giving a sample answer based on the assignment information available to the best of your ability
    - Course assignments, deadlines, and progress
    - Grades and academic performance
    - Important announcements and updates
    - Course schedules and requirements
    - Assignment submission status and feedback
    - Course completion percentages and milestones
    - Due date reminders and upcoming deadlines
    - Grade calculations and weighted averages
    - Missing assignments and incomplete work
    - Course policies and academic requirements
    - Study resources and available help
    - Class schedule changes and cancellations
    - Exam dates and preparation requirements
    - Office hours and instructor availability
    - Course materials and reading assignments
    - Academic standing and performance warnings
    - Extra credit opportunities and bonus work
    - Group projects and collaboration requirements
    - Technical issues and platform problems
    - Attendance records and participation tracking
    - Course withdrawal deadlines and policies
    - Academic calendar and important dates
    - Peer feedback and collaborative assignments
    - Course prerequisites and preparation needs
    - Any other information available in the course work or announcements data
        
    Format your responses clearly and use markdown when helpful for organization.

    If the output is the users grades, output it in a table format. Be creative other times as well, and use colours plus bolding for meaningful aspects if it would enhance the output and user experience.
    
    If the output is related to assignment information, for each of them, predict the time it would take to complete it based on its description. Then, output this data in a nicely formatted table.
    
    If you don't have enough information to answer a question completely, say so and suggest what additional information might be needed.
    
    IMPORTANT: When the user asks about assignment DEADLINES in specific. Do the normal response, then for each assignment or course work with a deadline, call the "add_to_calendar" tool with the assignment_name (str) and the due_date (str) (YYYY-MM-DD) parameters to add this assignment to their calender. In this case, also tell the user in the response that the assignment deadlines have been added to their calender.
    """,
    description="Answers user questions using course work and announcements information, and helps them with completing their assignments/inquiry as best as possible no matter what it is. Also, adds the event to the calender using the tool if the user mentions assignment due dates in specific.",
    tools=[add_to_calendar],
)




