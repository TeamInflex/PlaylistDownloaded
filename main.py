import os
from pytube import Playlist
from telegram import Bot
from telegram import InputFileCaption

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
        for video in playlist.videos:
            video.streams.filter(res="1080p").first().download(download_dir)

        # Send each video file to the user with the video title as caption
        for video in playlist.videos:
            video_title = video.title
            video_file_path = os.path.join(download_dir, f"{video_title}.mp4")

            with open(video_file_path, 'rb') as video_file:
                caption = f"Title: {video_title}"
                bot.send_document(chat_id, document=InputFileCaption(video_file, caption))

        # Optional: Clean up downloaded files after sending
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            os.remove(file_path)

        os.rmdir(download_dir)

        return True

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # Replace with your Telegram bot token
    TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
    
    # Replace with the chat_id of the user who sends the playlist link
    user_chat_id = 'user_chat_id'

    # Example playlist URL sent by the user
    user_playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"

    # Download playlist videos in full HD quality and send to the user
    download_and_send_playlist(user_chat_id, user_playlist_url)
