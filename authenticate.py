import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# --- Configuration ---
# This is the file you downloaded from the Cloud Console
CLIENT_SECRETS_FILE = "credentials.json" 
# This is the file that will be created with your access token
TOKEN_FILE = "token.json" 

# These are the permissions the script will ask for.
# They must match the ones in tools.py
SCOPES = [
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly'
]

def authenticate():
    """
    Runs the OAuth 2.0 flow to get user consent and create token.json.
    This script only needs to be run once.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        print(f"'{TOKEN_FILE}' already exists. Authentication may not be needed.")
        print("If you need to re-authenticate, please delete the file and run again.")
        return

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Starting authentication flow... Your browser will open.")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"\nAuthentication successful! Credentials saved to '{TOKEN_FILE}'.")
            print("You can now run the main application.")

if __name__ == '__main__':
    authenticate() 