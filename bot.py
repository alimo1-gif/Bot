
import telebot
import os
from pytube import YouTube

# Replace with your actual bot token
BOT_TOKEN = "7036178118:AAGCGkRbYdCclSaTVGzPJpUI3s_yuhSQpbc"
bot = telebot.TeleBot(BOT_TOKEN)

# Define a function to download YouTube video as MP3
def download_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_path = audio_stream.download(output_path="downloads/")
        base, ext = os.path.splitext(file_path)
        new_file = base + ".mp3"
        os.rename(file_path, new_file)
        return new_file
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handle messages that contain a YouTube link
@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def handle_youtube_link(message):
    url = message.text
    bot.reply_to(message, "Downloading the audio... Please wait.")

    file_path = download_audio(url)
    if file_path:
        with open(file_path, "rb") as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(file_path)  # Clean up after sending
    else:
        bot.reply_to(message, "Failed to download the audio. Please try again.")

# Start the bot
print("Bot is running...")
bot.polling()
