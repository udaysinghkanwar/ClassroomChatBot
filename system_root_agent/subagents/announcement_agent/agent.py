"""
Announcement Agent

This agent is responsible for gathering and analyzing Google Classroom announcements.
"""

from google.adk.agents import LlmAgent

from .tools import get_announcements

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Announcement Agent
announcement_agent = LlmAgent(
    name="AnnouncementAgent",
    model=GEMINI_MODEL,
    instruction="""You are an Announcement Agent for Google Classroom.
    
    When asked for announcement information, you should:
    1. Use the 'get_announcements' tool to gather announcements data from Google Classroom
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - status: "success" or "error"
    - announcements: List of announcement objects with fields like:
      * id: Announcement ID
      * courseId: Course ID
      * courseName: Course name
      * text: Announcement content
      * creationTime: When it was created
      * updateTime: When it was last updated
      * creatorUserId: Who created it
      * state: Current state (PUBLISHED, DRAFT, etc.)
    - total_count: Total number of announcements
    - courses_checked: List of courses that were checked
    - error_message: Error details (if status is "error")
    
    Format your response as a well-structured report section with:
    - Summary of total announcements found
    - Breakdown by course
    - Recent announcements (last 7 days)
    - Any important announcements or patterns
    - Error information if any occurred
    
    IMPORTANT: You MUST call the get_announcements tool. Do not make up information.
    If there are no announcements or errors, clearly state that in your response.
    """,
    description="Gathers and analyzes Google Classroom announcements",
    tools=[get_announcements],
    output_key="announcements_info",
)
