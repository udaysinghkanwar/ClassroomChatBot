"""
System Monitor Agent Package

This package provides a system monitoring agent that gathers system information
and produces a comprehensive system health report.
"""

from dotenv import load_dotenv

from .agent import root_agent

# Load environment variables from .env file
load_dotenv()
