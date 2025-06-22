"""
Announcement Agent

This agent is responsible for gathering and analyzing announcements information.
"""

from google.adk.agents import LlmAgent

from .tools import get_announcements

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Announcement Agent (in the future will add sequential agent to gather more information)
announcement_agent = LlmAgent(
    name="AnnouncementAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Announcement Agent.
    
    When asked for system information, you should:
    1. Use the 'get_announcements' tool to gather announcements data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core disk information including partitions
    - stats: Key statistical data about storage usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - Partition information
    - Storage capacity and usage
    - Any storage concerns (high usage > 85%)
    
    IMPORTANT: You MUST call the get_announcements tool. Do not make up information.
    """,
    description="Gathers and analyzes announcements information",
    tools=[get_announcements],
    output_key="announcements_info",
)
