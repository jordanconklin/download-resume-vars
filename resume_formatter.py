from __future__ import print_function
import os
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
from dotenv import load_dotenv

load_dotenv()   

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_credentials():
    print(f"Creating credentials with scopes: {SCOPES}")
    creds = Credentials(
        token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES
    )
    print(f"Credentials created. Valid: {creds.valid}, Expired: {creds.expired}")
    if creds.expired:
        print("Token has expired. Attempting to refresh...")
        try:
            creds.refresh(Request())
            print("Token refreshed successfully")
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None
    elif not creds.valid:
        print("Credentials are invalid")
        return None
    return creds

def update_resume(service, document_id, old_text, new_text):
    document = service.documents().get(documentId=document_id).execute()

    requests = []
    found = False
    for element in document['body']['content']:
        if 'paragraph' in element:
            for run in element['paragraph']['elements']:
                if 'textRun' in run:
                    if old_text in run['textRun']['content']:
                        found = True
                        requests.append({
                            'replaceAllText': {
                                'containsText': {
                                    'text': old_text,
                                    'matchCase': True
                                },
                                'replaceText': new_text
                            }
                        })
                        requests.append({
                            'updateTextStyle': {
                                'range': {
                                    'startIndex': run['startIndex'],
                                    'endIndex': run['endIndex']
                                },
                                'textStyle': {
                                    'bold': True
                                },
                                'fields': 'bold'
                            }
                        })

    if not found:
        print(f"Warning: '{old_text}' not found in the document.")
        return

    if requests:
        result = service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()
        print(f"Document updated successfully: {old_text} -> {new_text}")
    else:
        print("No updates were necessary")

def download_file(service, file_id, filename):
    downloads_folder = os.path.expanduser("~/Downloads")
    full_path = os.path.join(downloads_folder, filename)
    
    request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    
    fh.seek(0)
    with open(full_path, 'wb') as f:
        f.write(fh.read())
        print(f"File downloaded as {full_path}")

def delete_existing_resumes():
    downloads_folder = os.path.expanduser("~/Downloads")
    files_to_delete = [
        'Jordan-Conklin-Software-Engineer-Resume.pdf',
        'Jordan-Conklin-SoftwareEngineer-Resume.pdf'
    ]
    for file in files_to_delete:
        file_path = os.path.join(downloads_folder, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted existing file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {str(e)}")
        else:
            print(f"File not found: {file}")

def main():
    try:
        # Delete existing resume files
        delete_existing_resumes()

        creds = get_credentials()
        if not creds:
            print("Failed to obtain valid credentials. Please check your tokens and try again.")
            return
        
        print("Building drive service...")
        try:
            drive_service = build('drive', 'v3', credentials=creds)
            print("Drive service built successfully.")
        except Exception as e:
            print(f"Error building drive service: {str(e)}")
            return

        print("Building docs service...")
        try:
            docs_service = build('docs', 'v1', credentials=creds)
            print("Docs service built successfully.")
        except Exception as e:
            print(f"Error building docs service: {str(e)}")
            return

        # Replace with your Google Doc ID
        DOCUMENT_ID = '1t3d7m8YV3oZ5rAAb7fMK7cHGiQk0_QWir728nPtPXvA'

        # Download original document
        download_file(drive_service, DOCUMENT_ID, 'Jordan-Conklin-Software-Engineer-Resume.pdf')

        # Update to June 2025
        update_resume(docs_service, DOCUMENT_ID, 'Expected December 2024', 'Expected June 2025')
        
        # Download updated document
        download_file(drive_service, DOCUMENT_ID, 'Jordan-Conklin-SoftwareEngineer-Resume.pdf')

        # Revert back to December 2024
        update_resume(docs_service, DOCUMENT_ID, 'Expected June 2025', 'Expected December 2024')

        print("Process completed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if hasattr(e, 'content'):
            print(f"Error content: {e.content}")

if __name__ == '__main__':
    main()