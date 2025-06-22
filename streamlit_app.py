"""
Streamlit Chat Interface for Classroom ChatBot

This app provides a stateful chat interface for interacting with the Google Classroom agents using ADK.
"""

import streamlit as st
import asyncio
import json
from typing import Dict, Any
import sys
import os
from datetime import datetime

# Add the system_root_agent to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'system_root_agent'))

# Import ADK components
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import the main system root agent
from system_root_agent.agent import root_agent

# Page configuration
st.set_page_config(
    page_title="Classroom ChatBot",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        border-left: 4px solid #ff4b4b;
    }
    .chat-message.assistant {
        background-color: #262730;
        border-left: 4px solid #00ff88;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
    }
    .state-display {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #333;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if "runner" not in st.session_state:
    st.session_state.runner = Runner(
        agent=root_agent,
        app_name="Classroom ChatBot",
        session_service=st.session_state.session_service,
    )

if "user_id" not in st.session_state:
    st.session_state.user_id = "default_user"

if "session_id" not in st.session_state:
    # Create initial session
    initial_state = {
        "user_name": "Classroom User",
        "courses_accessed": [],
        "interaction_history": [],
        "last_announcement_check": None,
        "last_coursework_check": None,
    }
    
    new_session = st.session_state.session_service.create_session(
        app_name="Classroom ChatBot",
        user_id=st.session_state.user_id,
        state=initial_state,
    )
    st.session_state.session_id = new_session.id

if "messages" not in st.session_state:
    st.session_state.messages = []

def update_interaction_history(entry):
    """Add an entry to the interaction history in state."""
    try:
        # Get current session
        session = st.session_state.session_service.get_session(
            app_name="Classroom ChatBot",
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id
        )

        # Get current interaction history
        interaction_history = session.state.get("interaction_history", [])

        # Add timestamp if not already present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the entry to interaction history
        interaction_history.append(entry)

        # Create updated state
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history

        # Create a new session with updated state
        st.session_state.session_service.create_session(
            app_name="Classroom ChatBot",
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id,
            state=updated_state,
        )
    except Exception as e:
        st.error(f"Error updating interaction history: {e}")

def add_user_query_to_history(query):
    """Add a user query to the interaction history."""
    update_interaction_history({
        "action": "user_query",
        "query": query,
    })

def add_agent_response_to_history(agent_name, response):
    """Add an agent response to the interaction history."""
    update_interaction_history({
        "action": "agent_response",
        "agent": agent_name,
        "response": response,
    })

def display_current_state():
    """Display the current session state."""
    try:
        session = st.session_state.session_service.get_session(
            app_name="Classroom ChatBot",
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id
        )

        with st.expander("🔍 Current Session State", expanded=False):
            st.json(session.state)
            
            # Show interaction count
            interaction_history = session.state.get("interaction_history", [])
            st.info(f"Total interactions: {len(interaction_history)}")
            
            # Show last checks
            last_announcement = session.state.get("last_announcement_check")
            last_coursework = session.state.get("last_coursework_check")
            
            if last_announcement:
                st.write(f"📢 Last announcement check: {last_announcement}")
            if last_coursework:
                st.write(f"📚 Last coursework check: {last_coursework}")

    except Exception as e:
        st.error(f"Error displaying state: {e}")

async def call_agent_async(query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # Add user query to history
    add_user_query_to_history(query)
    
    final_response_text = None
    agent_name = None

    try:
        async for event in st.session_state.runner.run_async(
            user_id=st.session_state.user_id,
            session_id=st.session_state.session_id,
            new_message=content
        ):
            # Capture the agent name from the event if available
            if event.author:
                agent_name = event.author

            # Process the event
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text and not part.text.isspace():
                        final_response_text = part.text.strip()
                        break

    except Exception as e:
        st.error(f"Error during agent run: {e}")
        return f"❌ Error: {str(e)}"

    # Add the agent response to interaction history if we got a final response
    if final_response_text and agent_name:
        add_agent_response_to_history(agent_name, final_response_text)

    return final_response_text

def get_agent_response_sync(query):
    """Synchronous wrapper for the async agent call."""
    try:
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(call_agent_async(query))
        loop.close()
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main Streamlit app function."""
    
    # Header
    st.title("🎓 Classroom ChatBot")
    st.markdown("Your AI assistant for Google Classroom - Powered by ADK & Gemini LLM")
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 Agent System")
        st.markdown("""
        - **🎯 Root Agent**: Orchestrates all subagents
        - **📢 Announcement Agent**: Analyzes announcements
        - **📚 Course Work Agent**: Analyzes assignments
        """)
        
        st.header("💡 Quick Actions")
        if st.button("📢 Get Announcements"):
            st.session_state.messages.append({"role": "user", "content": "Show me the latest announcements"})
            response = get_agent_response_sync("Show me the latest announcements")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📚 Get Assignments"):
            st.session_state.messages.append({"role": "user", "content": "What assignments are due?"})
            response = get_agent_response_sync("What assignments are due?")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔄 New Session"):
            # Create a new session
            initial_state = {
                "user_name": "Classroom User",
                "courses_accessed": [],
                "interaction_history": [],
                "last_announcement_check": None,
                "last_coursework_check": None,
            }
            
            new_session = st.session_state.session_service.create_session(
                app_name="Classroom ChatBot",
                user_id=st.session_state.user_id,
                state=initial_state,
            )
            st.session_state.session_id = new_session.id
            st.session_state.messages = []
            st.rerun()
        
        st.header("🔧 Session Info")
        st.info(f"Session ID: {st.session_state.session_id[:8]}...")
        st.info(f"User ID: {st.session_state.user_id}")
        
        # Display current state
        display_current_state()
    
    # Chat interface
    st.header("💬 Chat with AI Agents")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your Google Classroom..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response from LLM agents
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI Agent is thinking..."):
                response = get_agent_response_sync(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 