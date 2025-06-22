"""
Course Work Information Agent

This agent is responsible for gathering and analyzing Google Classroom course work.
"""

from google.adk.agents import LlmAgent

from .tools import get_course_work

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Course Work Agent
course_work_agent = LlmAgent(
    name="CourseWorkAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Course Work Agent for Google Classroom.
    
    When asked for course work information, you should:
    1. Use the 'get_course_work' tool to gather data from Google Classroom.
    2. Analyze the returned dictionary data for all assignments.
    3. Format this information into a concise, clear section of a system report.
    
    The tool will return a dictionary with:
    - status: "success" or "error"
    - course_work: List of coursework objects.
    - total_count: Total number of assignments found.
    - courses_checked: List of courses that were checked.
    - error_message: Error details (if status is "error").
    
    Format your response as a well-structured report section with:
    - A summary of total assignments across all courses.
    - A breakdown of assignments by course.
    - A list of upcoming due dates.
    - Any ungraded assignments (where maxPoints is 0 or not set).
    
    IMPORTANT: You MUST call the get_course_work tool. Do not make up information.
    """,
    description="Gathers and analyzes Google Classroom course work information.",
    tools=[get_course_work],
    output_key="course_work_info",
)
