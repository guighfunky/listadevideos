import csv
from googleapiclient.discovery import build

api_key = 'YOUR_API_KEY'
channel_id = 'CHANNEL_ID'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_uploads_playlist_id(youtube, channel_id):
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )
    
    while request is not None:
        response = request.execute()
        
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_date = item['contentDetails']['videoPublishedAt']
            videos.append((video_id, video_date))
        
        request = youtube.playlistItems().list_next(request, response)
    
    return videos

uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
videos = get_videos_from_playlist(youtube, uploads_playlist_id)

with open('youtube_videos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Video ID', 'Published Date'])
    for video in videos:
        writer.writerow(video)

print(f"CSV file 'youtube_videos.csv' created successfully with {len(videos)} videos.")
