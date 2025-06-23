"""
Course Work Information Tool
Google Classroom Coursework Tool

This module provides a tool for gathering coursework (assignments) from Google Classroom.
"""

import sys
import os
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) )

import time
from typing import Any, Dict, List, Optional
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth_web_config import get_classroom_service, get_user_id


def get_course_work() -> Dict[str, Any]:
    """
    Fetches all coursework (assignments) from Google Classroom courses, including the current user's grade for each assignment.
    
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
        # Get user ID and service
        user_id = get_user_id()
        service = get_classroom_service(user_id)
        
        if not service:
            return {
                "status": "error",
                "error_message": "Failed to initialize Google Classroom API service. Please authenticate with Google Classroom.",
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
                    
                    # --- Fetch the current user's submission and grade ---
                    submission = _get_my_submission_for_assignment(service, course_id, item['id'])
                    if submission:
                        item['mySubmission'] = {
                            'state': submission.get('state'),
                            'assignedGrade': submission.get('assignedGrade'),
                            'draftGrade': submission.get('draftGrade'),
                            'late': submission.get('late'),
                            'alternateLink': submission.get('alternateLink'),
                        }
                    else:
                        item['mySubmission'] = None
                
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


def _get_my_submission_for_assignment(service, course_id: str, course_work_id: str) -> Optional[Dict[str, Any]]:
    """Get the current user's submission for a specific assignment."""
    try:
        # Get the current user's profile to get their ID
        profile = service.userProfiles().get(userId='me').execute()
        user_id = profile['id']
        
        # Get the user's submission for this assignment
        response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=course_work_id,
            userId=user_id
        ).execute()
        
        submissions = response.get('studentSubmissions', [])
        if submissions:
            return submissions[0]  # Return the first (and should be only) submission
        
        return None
        
    except HttpError as e:
        print(f"Error fetching submission for assignment {course_work_id}: {e}")
        return None
