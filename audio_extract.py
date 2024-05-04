from pytube import YouTube
import pandas as pd
import os

audio_folder = "audios"
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

data = pd.read_csv('youtube_links.csv')
data.dropna(axis=0, inplace=True)
list_data = data.values.tolist()
for per_url_list in list_data:
    for per_url_without_list in per_url_list:
        try:
            # Get the YouTube video URL
            text = per_url_without_list

            # Create a YouTube object
            yt = YouTube(text)

            # Extract video title (optional for informative filenames)
            title = yt.title.replace('/', '_')  # Replace slashes for safe filenames

            # Filter for audio streams, ensuring presence and choosing the highest bitrate
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            if not audio_streams:
                print(f"No audio streams found for '{text}'")
                continue  # Skip to the next URL if no audio available

            audio_stream = audio_streams.first()  # Choose the first (highest bitrate)

            # Download the audio stream as WAV, ensuring compatibility
            audio_stream.download(filename=os.path.join(audio_folder, f"{title}.wav"))

            print(f"Downloaded audio from '{title}' successfully (WAV format)!")
        except Exception as e:
            print(f"An error occurred while downloading '{per_url_without_list}': {e}")

print("All audio downloads completed!") 



