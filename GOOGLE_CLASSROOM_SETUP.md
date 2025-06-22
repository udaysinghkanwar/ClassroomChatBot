# Google Classroom API Setup Guide

This guide will help you set up authentication for the Google Classroom API to use with the `get_announcements()` function.

## Prerequisites

1. A Google Cloud Project
2. Google Classroom API enabled
3. Python environment with the required dependencies

## Step 1: Enable Google Classroom API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to "APIs & Services" > "Library"
4. Search for "Google Classroom API"
5. Click on it and press "Enable"

## Step 2: Create Credentials

### Option A: Service Account (Recommended for automated systems)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `classroom-announcements`
   - Description: `Service account for fetching Classroom announcements`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"
6. Click on the created service account
7. Go to the "Keys" tab
8. Click "Add Key" > "Create New Key"
9. Choose "JSON" format and download the file
10. Save the JSON file securely (e.g., as `service-account-key.json`)

### Option B: OAuth 2.0 (For user-specific access)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" or "Web application" based on your use case
4. Fill in the required information
5. Download the client configuration file

## Step 3: Set Up Environment Variables

Create a `.env` file in your project root and add:

```bash
# For Service Account (Option A)
GOOGLE_SERVICE_ACCOUNT_PATH=./service-account-key.json

# For OAuth 2.0 (Option B) - after running the auth flow
GOOGLE_TOKEN_PATH=./token.json
```

## Step 4: Grant Permissions (Service Account)

If using a service account, you need to add it to your Google Classroom courses:

1. Go to your Google Classroom course
2. Click on "People" tab
3. Click the "+" button to add people
4. Add the service account email (found in the JSON file under `client_email`)
5. Assign appropriate role (Teacher or Student)

## Step 5: Test the Setup

Install the dependencies and test:

```bash
pip install -r requirements.txt
python -c "from system_root_agent.subagents.announcement_agent.tools import get_announcements; print(get_announcements())"
```

## Troubleshooting

### Common Issues:

1. **"Failed to initialize Google Classroom API service"**
   - Check that your credentials file exists and is valid
   - Verify the API is enabled in your Google Cloud project

2. **"No courses found"**
   - Ensure the service account/user has access to Google Classroom courses
   - Check that courses are not archived

3. **Permission Denied errors**
   - Verify the service account has been added to the courses
   - Check that the OAuth scope includes `classroom.announcements.readonly`

### Required OAuth Scopes:

- `https://www.googleapis.com/auth/classroom.announcements.readonly` (for reading announcements)
- `https://www.googleapis.com/auth/classroom.courses.readonly` (for reading courses)

## Security Notes

- Never commit credential files to version control
- Use environment variables for sensitive information
- Regularly rotate service account keys
- Follow the principle of least privilege when assigning permissions 