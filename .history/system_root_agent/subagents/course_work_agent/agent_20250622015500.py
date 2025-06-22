"""
CPU Information Agent

This agent is responsible for gathering and analyzing CPU information.
"""

from google.adk.agents import LlmAgent

from .tools import get_course_work

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Course Work Agent
course_work_agent = LlmAgent(
    name="CourseWorkAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Course Work Agent.
    
    When asked for the course work or assignment information, you should:
    1. Use the 'get_course_work' tool to gather course work data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report

    
    The tool will return a dictionary with:
    - status: "success" or "error"
    - announcements: List of course work objects with fields like:
      * id: Course work ID
      * courseId: Course ID
      * courseName: Course name
      * text: Assignment content
      * creationTime: When it was created
      * updateTime: When it was last updated
      * creatorUserId: Who created it
      * state: Current state (PUBLISHED, DRAFT, etc.)
    - total_count: Total number of assignments
    - courses_checked: List of assignments that were checked
    - error_message: Error details (if status is "error")
    
    Format your response as a well-structured report section with:
    - Summary of total assignments found
    - Breakdown by course
    - Recent assignments (last 7 days)
    - Any important announcements or patterns
    - Error information if any occurred
    
    IMPORTANT: You MUST call the get_course_work tool. Do not make up information.
    If there are no announcements or errors, clearly state that in your response.
    """,
    description="Gathers and analyzes course work (assignment) information",
    tools=[get_course_work],
    output_key="course_work_info",
)
