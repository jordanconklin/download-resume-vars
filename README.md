# Resume Formatter

## Description
Resume Formatter is a Python script that automates the process of updating and downloading different versions of your resume from Google Docs. It uses the Google Drive and Google Docs APIs to modify the resume content and download PDF versions.

## Features
- Automatically updates the expected graduation date in your resume
- Downloads both the original and updated versions of your resume as PDFs
- Deletes existing resume files from your Downloads folder before creating new ones
- Uses environment variables for secure credential management

## Prerequisites
- Python 3.7+
- Google Cloud Platform account with Google Drive and Google Docs APIs enabled
- OAuth 2.0 credentials for Google APIs

## Google Cloud Setup

Before using this script, you need to set up a Google Cloud project and enable the necessary APIs. Follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Drive API and Google Docs API for your project.
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the client configuration file
5. Use the Google OAuth 2.0 Playground to get your refresh token:
   - Go to [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
   - Click the gear icon in the top right and check "Use your own OAuth credentials"
   - Enter your Client ID and Client Secret from the downloaded client configuration
   - Select the necessary scopes: 
     - https://www.googleapis.com/auth/documents
     - https://www.googleapis.com/auth/drive
   - Click "Authorize APIs" and follow the prompts
   - On the next screen, click "Exchange authorization code for tokens"
   - Copy the refresh token

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/resume-formatter.git
   cd resume-formatter
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with your Google API credentials:
   ```
   REFRESH_TOKEN=your_refresh_token
   ACCESS_TOKEN=your_access_token
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```

## Configuration

- Update the `DOCUMENT_ID` in the script with your Google Doc ID. You can find this in the URL of your Google Doc:
  ```
  https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit
  ```

- Modify the `files_to_delete` list in the `delete_existing_resumes()` function if you want to change the filenames of the resumes to be deleted:

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
