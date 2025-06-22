"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.course_work_agent import course_work_agent
from .subagents.announcement_agent import announcement_agent
from .subagents.data_analyzer_agent import data_analyzer_agent

# --- 1. Create Parallel Agent to gather information concurrently ---
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    sub_agents=[course_work_agent, announcement_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="system_root_agent",
    sub_agents=[system_info_gatherer, data_analyzer_agent],
)
