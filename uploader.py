import os, sys, time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from tkinter import messagebox
from chunk_files import ChunkedFileReader

class Authentication:
    # If modifying these SCOPES, delete the file token.json
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def get_resource_path(self, relative_path):
        """Get absolute path for PyInstaller bundled files."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def get_token_path(self):
        return os.path.join(os.path.expanduser("~"), ".gdrive_uploader", "token.json")
    
    def check_authentication(self):
        if not os.path.exists(self.get_token_path()):
            messagebox.showwarning("Token Missing", "The token.json file is missing.\nYou will now be redirected to the browser to authorize your app.\nYou have to complete the login within 1 minute or less.")
            return False

    def authenticate(self):
        try:
            creds = None
            token_path = self.get_token_path()
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.get_resource_path('credentials.json'), self.SCOPES)
                    creds = flow.run_local_server(port=0, timeout_seconds=60)

                # Save the credentials for next run
                os.makedirs(os.path.dirname(token_path), exist_ok=True)

                with open(self.get_token_path(), 'w') as token:
                    token.write(creds.to_json())

            return creds
        except Exception as e:
            print(f"❌ Authentication failed or cancelled: {e}")
            return False

class UploadToDrive(Authentication):
    MB = 1048576
    
    def upload_or_replace_file(self, filepath, mimetype='application/octet-stream', progress_callback=None):
        from googleapiclient.http import MediaIoBaseUpload
        import os
        self.service = build('drive', 'v3', credentials=self.authenticate())

        file_name = os.path.basename(filepath)
        results = self.service.files().list(
            q=f"name='{file_name}' and trashed = false",
            spaces='drive',
            fields="files(id, name)"
        ).execute()

        files = results.get('files', [])

        file_reader = ChunkedFileReader(filepath)
        media = MediaIoBaseUpload(file_reader, mimetype=mimetype, chunksize=1024 * 1024, resumable=True)

        if files:
            file_id = files[0]['id']
            request = self.service.files().update(fileId=file_id, media_body=media)
            alert_text = "File updated successfully"
        else:
            file_metadata = {'name': file_name}
            request = self.service.files().create(body=file_metadata, media_body=media)
            alert_text = "File uploaded successfully"

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status and progress_callback:
                progress_callback(status.progress())
            elif response and progress_callback:
                # 100% when done
                progress_callback(1.0)

        file_reader.close()
        return alert_text



class ManageFiles(Authentication):
    def __init__(self):
        self.service = build('drive', 'v3', credentials=self.authenticate())
    
    def list_files(self, page_size=20):
        try:
            results = self.service.files().list(
                pageSize=page_size,
                fields="files(id, name, mimeType, size, modifiedTime)"
            ).execute()
            return results.get('files', [])

        except Exception as e:
            print(f"❌ Failed to list files: {e}")
            return []
        
    def download_file(self, file_id, save_path):
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io

            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(save_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            return True, save_path
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False, None
        
    def delete_file(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False

