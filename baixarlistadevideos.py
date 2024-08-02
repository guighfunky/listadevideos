import os
import subprocess
import pandas as pd

# Carregar o arquivo CSV
file_path = 'C:/caminho/para/o/csv/youtube_videos.csv'
youtube_videos_df = pd.read_csv(file_path)

# Selecionar intervalo de vídeos por linhas do CSV
selected_videos = youtube_videos_df.iloc[1:100] # Exemplo, linhas 1 a 100

# Diretório de destino
download_path = "C:/destino/dos/videos"
os.makedirs(download_path, exist_ok=True)

# Função para baixar vídeo do YouTube
def download_video(video_id, published_date, download_path):
    url = f"https://www.youtube.com/watch?v={video_id}"
    formatted_date = pd.to_datetime(published_date).strftime('%Y-%m-%d')
    output_template = os.path.join(download_path, f"{formatted_date}-%(title)s.%(ext)s")
    command = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "-o", output_template,
        url
    ]
    subprocess.run(command)

for index, row in selected_videos.iterrows():
    download_video(row['Video ID'], row['Published Date'], download_path)

print("Download concluído.")