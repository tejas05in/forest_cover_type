import io
import sys
from src.forest.constants.database import *
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from src.forest.logger import logging
from src.forest.exception import CustomException
from src.forest.configuration import GDriveClient


class ForestData:
    def __init__(self):
        try:
            self.file_id = file_id
            self.gdrive_client = GDriveClient()
            self.gdrive_client.authenticate()
            logging.info("Forest Data initialized successfully")
        except Exception as e:
            logging.error(f"Error in initializing Forest Data: {e}")
            raise CustomException(e, sys)

    def upload_file(self, file_path: str, file_name: str) -> str:
        try:
            service = self.gdrive_client.authenticate()
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, resumable=True)
            uploaded_file = service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
            print(
                f"File uploaded successfully. File ID: {uploaded_file.get('id')}")
            logging.info(
                f"File uploaded successfully. File ID: {uploaded_file.get('id')}")
            return uploaded_file.get('id')
        except Exception as e:
            logging.error(f"Error in uploading file: {e}")
            raise CustomException(e, sys)

    def download_file(self, destination_path: str):
        try:
            service = self.gdrive_client.authenticate()
            request = service.files().get_media(fileId=self.file_id)

            with io.FileIO(destination_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%.")
            logging.info(f"File downloaded successfully at {destination_path}")
        except Exception as e:
            logging.error(f"Error in downloading file: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    forest_data = ForestData()
    forest_data.download_file('downloaded_myfile.csv')
