"""
Google Classroom Announcements Tool

This module provides a tool for gathering announcements from Google Classroom.
"""

import os
import time
from typing import Any, Dict, List, Optional
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import the new OAuth configuration
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from oauth_web_config import get_classroom_service, get_user_id


def get_announcements() -> Dict[str, Any]:
    """
    Fetches all announcements from Google Classroom courses.
    
    Returns:
        Dict containing announcements data with structure:
        {
            "status": "success" | "error",
            "announcements": [...],
            "total_count": int,
            "courses_checked": [...],
            "error_message": str (if status is error)
        }
    """
    try:
        # Get user ID and service
        user_id = get_user_id()
        service = get_classroom_service(user_id)
        
        if not service:
            return {
                "status": "error",
                "error_message": "Failed to initialize Google Classroom API service. Please authenticate with Google Classroom.",
                "announcements": [],
                "total_count": 0,
                "courses_checked": []
            }
        
        # Get all courses
        courses = _get_courses(service)
        if not courses:
            return {
                "status": "success",
                "announcements": [],
                "total_count": 0,
                "courses_checked": [],
                "message": "No courses found or no access to courses."
            }
        
        # Get announcements from all courses
        all_announcements = []
        courses_checked = []
        
        for course in courses:
            course_id = course['id']
            course_name = course.get('name', 'Unknown Course')
            courses_checked.append({
                'id': course_id,
                'name': course_name
            })
            
            try:
                # Get announcements for this course
                announcements = _get_course_announcements(service, course_id)
                
                # Add course context to each announcement
                for announcement in announcements:
                    announcement['courseId'] = course_id
                    announcement['courseName'] = course_name
                
                all_announcements.extend(announcements)
                
            except HttpError as e:
                # Log error but continue with other courses
                print(f"Error fetching announcements for course {course_id}: {e}")
                continue
        
        return {
            "status": "success",
            "announcements": all_announcements,
            "total_count": len(all_announcements),
            "courses_checked": courses_checked,
            "message": f"Successfully fetched {len(all_announcements)} announcements from {len(courses_checked)} courses."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}",
            "announcements": [],
            "total_count": 0,
            "courses_checked": []
        }


def _get_courses(service) -> List[Dict[str, Any]]:
    """Get all courses the user has access to."""
    try:
        courses = []
        page_token = None
        
        while True:
            response = service.courses().list(
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken')
            
            if not page_token:
                break
        
        return courses
        
    except HttpError as e:
        print(f"Error fetching courses: {e}")
        return []


def _get_course_announcements(service, course_id: str) -> List[Dict[str, Any]]:
    """Get all announcements for a specific course."""
    try:
        announcements = []
        page_token = None
        
        while True:
            response = service.courses().announcements().list(
                courseId=course_id,
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            announcements.extend(response.get('announcements', []))
            page_token = response.get('nextPageToken')
            
            if not page_token:
                break
        
        return announcements
        
    except HttpError as e:
        print(f"Error fetching announcements for course {course_id}: {e}")
        return []
