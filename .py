import os
import pickle
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request  # Import this

# Authenticate with Google API for YouTube
def authenticate_youtube():
    # Define the scopes for the YouTube API
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    creds = None

    # Check if token.json exists for credentials
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, prompt for authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Use the Request module to refresh the credentials
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    
    youtube = build("youtube", "v3", credentials=creds)
    return youtube

# Function to upload the video to YouTube
def upload_video(youtube, video_path, title, description, category_id, privacy_status):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'auto-upload', 'python', 'SEO', 'trending'],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media_file
    )

    # Start upload process and check response
    print(f"Starting upload for video: {title}...")
    response = request.execute()

    if 'id' in response:
        print(f"Upload successful! Video ID: {response['id']}")
        print(f"Video URL: https://www.youtube.com/watch?v={response['id']}")
    else:
        print("Upload failed. Please check the details.")

# Function to run the upload task
def main():
    video_path = "1105.mp4"  # Your video file
    title = "Your Video Title"  # Change this to your video title
    description = "Your video description"  # Change this to your video description
    category_id = "22"  # Example: "22" for People & Blogs category
    privacy_status = "public"  # Options: "public", "private", "unlisted"

    youtube = authenticate_youtube()  # Authenticate YouTube
    upload_video(youtube, video_path, title, description, category_id, privacy_status)

if __name__ == "__main__":
    main()
