"""
Course Work Information Tool

This module provides a tool for gathering course work from Google Classroom.
"""
import os
from typing import Any, Dict, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_course_work() -> Dict[str, Any]:
    """
    Fetches all course work from Google Classroom courses.
    """
    try:
        service = _get_classroom_service()
        if not service:
            return {
                "status": "error",
                "error_message": "Failed to initialize Google Classroom API service.",
                "course_work": [],
                "total_count": 0,
                "courses_checked": [],
            }

        courses = _get_courses(service)
        if not courses:
            return {
                "status": "success",
                "course_work": [],
                "total_count": 0,
                "courses_checked": [],
                "message": "No courses found or no access to courses.",
            }

        all_course_work = []
        courses_checked = []
        for course in courses:
            course_id = course["id"]
            course_name = course.get("name", "Unknown Course")
            courses_checked.append({"id": course_id, "name": course_name})

            try:
                course_work_items = _get_course_coursework(service, course_id)
                all_course_work.extend(course_work_items)
            except HttpError as e:
                print(f"Error fetching course work for course {course_id}: {e}")
                continue

        return {
            "status": "success",
            "course_work": all_course_work,
            "total_count": len(all_course_work),
            "courses_checked": courses_checked,
            "message": f"Successfully fetched {len(all_course_work)} course work items from {len(courses_checked)} courses.",
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}",
            "course_work": [],
            "total_count": 0,
            "courses_checked": [],
        }


def _get_classroom_service():
    """Initializes and returns the Google Classroom API service."""
    creds = None
    token_path = "token.json"
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path, 
            scopes=[
                'https://www.googleapis.com/auth/classroom.announcements.readonly',
                'https://www.googleapis.com/auth/classroom.courses.readonly',
                'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
            ]
        )
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This indicates that the user needs to run authenticate.py
            return None
    
    try:
        service = build("classroom", "v1", credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Classroom service: {e}")
        return None


def _get_courses(service) -> List[Dict[str, Any]]:
    """Fetches all courses."""
    courses = []
    page_token = None
    while True:
        response = service.courses().list(pageToken=page_token, pageSize=100).execute()
        courses.extend(response.get("courses", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return courses


def _get_course_coursework(service, course_id: str) -> List[Dict[str, Any]]:
    """Fetches all course work for a specific course."""
    course_work = []
    page_token = None
    while True:
        response = (
            service.courses()
            .courseWork()
            .list(courseId=course_id, pageToken=page_token, pageSize=100)
            .execute()
        )
        course_work.extend(response.get("courseWork", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return course_work