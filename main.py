import os
from pytube import Playlist
from telegram import Bot
from telegram import InputFile
import sys

# Telegram bot token - replace with your bot token
TELEGRAM_BOT_TOKEN = '6609599978:AAHSJhmTlW3QZGcpD_a1EgwOjQe4Cnz3-58'

# Create a Telegram bot
bot = Bot(TELEGRAM_BOT_TOKEN)

def download_and_send_playlist(chat_id, playlist_url):
    try:
        # Download playlist videos in full HD quality
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title()

        # Create a directory to save downloaded videos
        download_dir = f'{playlist_title}_videos'
        os.makedirs(download_dir, exist_ok=True)

        # Download each video in the playlist in full HD quality
        for index, video in enumerate(playlist.videos, start=1):
            video.streams.filter(res="1080p").first().download(download_dir)
            print(f"Video {index} downloaded.")

        # Send each video file to the user without captions
        for index, video in enumerate(playlist.videos, start=1):
            video_title = video.title
            video_file_path = os.path.join(download_dir, f"{video_title}.mp4")

            with open(video_file_path, 'rb') as vid_file:
                bot.send_document(chat_id, document=InputFile(vid_file))
                print(f"Video {index} sent.")

        print("Download and sending completed successfully.")
        
        # Clean up downloaded files after sending
        for file_name in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file_name)
            os.remove(file_path)

        os.rmdir(download_dir)

        # Exit the script after completion
        sys.exit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit()

if __name__ == "__main__":
    # Replace with the chat_id of the user who sends the playlist link
    user_chat_id = '5747402681'

    # Example playlist URL sent by the user
    user_playlist_url = "https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg"

    print("Bot is starting...")
    
    # Download playlist videos in full HD quality and send to the user
    download_and_send_playlist(user_chat_id, user_playlist_url)
