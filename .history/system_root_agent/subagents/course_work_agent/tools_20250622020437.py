"""
Google Classroom Coursework Tool

This module provides a tool for gathering coursework (assignments) from Google Classroom.
"""

import os
import time
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_course_work() -> Dict[str, Any]:
    """
    Fetches all coursework (assignments) from Google Classroom courses.
    
    Returns:
        Dict containing coursework data with structure:
        {
            "status": "success" | "error",
            "coursework": [...],
            "total_count": int,
            "courses_checked": [...],
            "error_message": str (if status is error)
        }
    """
    try:
        # Initialize the Classroom API service
        service = _get_classroom_service()
        if not service:
            return {
                "status": "error",
                "error_message": "Failed to initialize Google Classroom API service. Check authentication setup.",
                "coursework": [],
                "total_count": 0,
                "courses_checked": []
            }
        
        # Get all courses
        courses = _get_courses(service)
        if not courses:
            return {
                "status": "success",
                "coursework": [],
                "total_count": 0,
                "courses_checked": [],
                "message": "No courses found or no access to courses."
            }
        
        # Get coursework from all courses
        all_coursework = []
        courses_checked = []
        
        for course in courses:
            course_id = course['id']
            course_name = course.get('name', 'Unknown Course')
            courses_checked.append({
                'id': course_id,
                'name': course_name
            })
            
            try:
                # Get coursework for this course
                coursework = _get_course_coursework(service, course_id)
                
                # Add course context to each coursework item
                for item in coursework:
                    item['courseId'] = course_id
                    item['courseName'] = course_name
                
                all_coursework.extend(coursework)
                
            except HttpError as e:
                # Log error but continue with other courses
                print(f"Error fetching coursework for course {course_id}: {e}")
                continue
        
        return {
            "status": "success",
            "coursework": all_coursework,
            "total_count": len(all_coursework),
            "courses_checked": courses_checked,
            "message": f"Successfully fetched {len(all_coursework)} coursework items from {len(courses_checked)} courses."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}",
            "coursework": [],
            "total_count": 0,
            "courses_checked": []
        }


def _get_classroom_service():
    """Initialize and return the Google Classroom API service."""
    try:
        # Try service account authentication first
        service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
        if service_account_path and os.path.exists(service_account_path):
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=[
                    'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
                    'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
                    'https://www.googleapis.com/auth/classroom.courses.readonly'
                ]
            )
        else:
            # Try OAuth2 credentials
            creds = None
            token_path = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
            
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, 
                    [
                        'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
                        'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
                        'https://www.googleapis.com/auth/classroom.courses.readonly'
                    ])
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    return None
            
            credentials = creds
        
        service = build('classroom', 'v1', credentials=credentials)
        return service
        
    except Exception as e:
        print(f"Error initializing Classroom service: {e}")
        return None


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


def _get_course_coursework(service, course_id: str) -> List[Dict[str, Any]]:
    """Get all coursework (assignments) for a specific course."""
    try:
        coursework = []
        page_token = None
        
        while True:
            response = service.courses().courseWork().list(
                courseId=course_id,
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            coursework.extend(response.get('courseWork', []))
            page_token = response.get('nextPageToken')
            
            if not page_token:
                break
        
        return coursework
        
    except HttpError as e:
        print(f"Error fetching coursework for course {course_id}: {e}")
        return []
