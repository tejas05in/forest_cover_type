import os
import sys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from forest.logger import logging
from forest.exception import CustomException
from forest.constants.database import *


class GDriveClient:
    def __init__(self):
        self.SCOPES = SCOPES
        self.token_name = token_name
        self.credentials_name = credentials_name
        self.file_id = file_id

    # Authenticate and create the Drive service
    def authenticate(self):
        try:
            creds = None
            if os.path.exists(self.token_name):
                creds = Credentials.from_authorized_user_file(
                    self.token_name, self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_name, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self.token_name, 'w') as token:
                    token.write(creds.to_json())
            logging.info("GDrive Authenticated successfully")
            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            logging.error(f"Error in GDrive authentication: {e}")
            raise CustomException(e, sys)
