import re
import os
import ffmpeg
import random
import string
import yt_dlp
import asyncio
import discord
import datetime
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
from config import alert_channel_ids, newest_message_ids, LOG_CHANNEL_ID, SAUCE_ID 
#!-------------------------------------------------------------------------------------------------------------------------------------!#

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Define intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Define the bot with command prefix and intents
bot = commands.Bot(command_prefix=['d', '!', '?'], intents=intents)

# Folder where downloaded videos will be saved temporarily
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

#!-------------------------------------------------------------------------------------------------------------------------------------!#

def only_prefix(prefix):
    def predicate(ctx):
        return ctx.prefix == prefix
    return commands.check(predicate)


#!-------------------------------------------------------------------------------------------------------------------------------------!#

#Command on Stautup            
@bot.event
async def on_ready():
    print(f'💚 Logged in as {bot.user}')
    await send_log_message(f'💚 **Arise:** {bot.user} is now awake')

    activity = discord.Game(name="Your Mom")
    await bot.change_presence(activity=activity)

    # Send a message to each channel and store its ID
    for channel_id in alert_channel_ids:
        alert_channel = bot.get_channel(channel_id)
        if alert_channel:
            message = await alert_channel.send(f"**Oomfie is online and doomscrolling** 💚")
            newest_message_ids[channel_id] = message.id  # Store the message ID for each channel
            print(f"🌟 Newest message ID stored for channel {channel_id}: {newest_message_ids[channel_id]}")

    # Delete past messages containing the specific text
    await delete_past_messages()

#!-------------------------------------------------------------------------------------------------------------------------------------!#

# Function to send logs to a Discord channel (in decoy server)
async def send_log_message(log_message):
    """Send a log message to a specific channel in the server."""
    await bot.wait_until_ready()  # Ensure the bot is ready
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(log_message)
    else:
        print(f"⚠️ Could not find log channel with ID {LOG_CHANNEL_ID}")

#!-------------------------------------------------------------------------------------------------------------------------------------!#

# Generate a random file name to prevent conflicts
def get_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

#!-------------------------------------------------------------------------------------------------------------------------------------!#



def sanitize_filename(name):
    # Remove characters not allowed in file names
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    return name


def get_unique_filename(folder, base_name, extension):
    # Try incrementing number if filename exists
    count = 0
    new_filename = f"{base_name}.{extension}"
    while os.path.exists(os.path.join(folder, new_filename)):
        count += 1
        new_filename = f"{base_name} ({count}).{extension}"
    return new_filename


#!-------------------------------------------------------------------------------------------------------------------------------------!#



#dl [link]
@bot.command(name='l')
async def download_fb(ctx, link: str):
    """Download a video from Facebook or Instagram using yt-dlp with cookies"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{ctx.author.name}#{ctx.author.discriminator}"

    # Determine if the link is for Facebook or Instagram
    if "facebook.com" in link:
        cookies_path = os.path.join(BASE_DIR, "fb_cookie.txt")  # Path to your Facebook cookies file
    elif "instagram.com" in link:
        cookies_path = os.path.join(BASE_DIR, "insta_cookie.txt")  # Path to your Instagram cookies file
    else:

        await ctx.send("❌ Invalid link. Please provide a valid Facebook or Instagram link.")
        return

    log_message = (
        f"\n‎ \n‎"
        f"--------------------------------------------\n"
        f"📢 **New Download Request**\n"
        f"👤 **User:** {user_info}\n"
        f"📅 **Time:** {current_time}\n"
        f"🌐 **Link:** {link}\n"
        f"--------------------------------------------"
    )
    print(log_message)
    await send_log_message(log_message)

    await ctx.send('"hmm.. imma check this link that u sent 🤔"')

    # Set the download folder based on the user's ID
    if ctx.author.id == SAUCE_ID:  # Your Discord User ID
        download_folder = os.path.join(BASE_DIR, "sauce_downloads")
    else:
        download_folder = DOWNLOAD_FOLDER

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    random_name = get_random_filename()
    original_file = f"{download_folder}/{random_name} oomfie video.mp4"
    compressed_file = f"{download_folder}/{random_name} oomfie video compressed.mp4"

    try:
        ydl_opts = {
            'outtmpl': original_file,
            'format': 'best',
            'cookiefile': cookies_path,  # Path to the cookies file
            # Use this for Instagram age-restricted content
            'age_limit': 18,  # Allow videos with age restriction
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        if os.path.exists(original_file):
            file_size_mb = os.path.getsize(original_file) / (1024 * 1024)
            print(f"📁 File downloaded: {original_file}")
            print(f"📏 File size: {file_size_mb:.2f} MB")
            await send_log_message(f"📁 **Downloaded:** {original_file}\n📏 **Size:** {file_size_mb:.2f} MB")

            if os.path.getsize(original_file) > 8 * 1024 * 1024:
                await ctx.send('"it\'s too big😭😭😭 must be less than 8 MB"')

                (
                    ffmpeg
                    .input(original_file)
                    .output(compressed_file, vcodec="libx264", crf=28)
                    .run(overwrite_output=True)
                )

                if os.path.exists(compressed_file) and os.path.getsize(compressed_file) < 8 * 1024 * 1024:
                    file_to_send = compressed_file

                    compressed_size_mb = os.path.getsize(compressed_file) / (1024 * 1024)
                    print(f"📁 Compressed file created: {compressed_file}")
                    print(f"📏 Compressed file size: {compressed_size_mb:.2f} MB")
                    await send_log_message(f"📁 **Compressed File:** {compressed_file}\n📏 **Size:** {compressed_size_mb:.2f} MB")

                else:
                    await ctx.send("❌ Compressed file is still too large. Unable to send.")
                    await send_log_message("❌ **Compression Failed:** File still too large.")
                    if os.path.exists(compressed_file):
                        pass
                    return
            else:
                file_to_send = original_file

            await ctx.send(file=discord.File(file_to_send))
            await send_log_message(f"✅ **File Sent:** {file_to_send}")

    except Exception as e:
        error_message = str(e)

        if "Restricted Video: You must be 18 years old or over" in error_message:
            await ctx.send("🚫 This video is **age-restricted** and cannot be downloaded without authentication.")
            await send_log_message("🚫 **Age-Restricted Video Detected:** Unable to download.")
        else:
            await ctx.send("\"doesn't work\"")
            error_message = f"⚠️ **Error:** {error_message}"
            print(error_message)
            await send_log_message(error_message)

    finally:
        await ctx.send(":3")


#!-------------------------------------------------------------------------------------------------------------------------------------!#

#dlyt [link]
@bot.command(name='lyt')
async def download_youtube_video(ctx, link: str):
    """Download a YouTube video and save/send it if under 8MB."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{ctx.author.name}#{ctx.author.discriminator}"

    log_message = (
        f"\n‎ \n‎"
        f"--------------------------------------------\n"
        f"📢 **New Download Request**\n"
        f"👤 **User:** {user_info}\n"
        f"📅 **Time:** {current_time}\n"
        f"🌐 **Link:** {link}\n"
        f"--------------------------------------------"
    )
    print(log_message)
    await send_log_message(log_message)

    await ctx.send("hhmmm... 👀")

    yt_video_folder = os.path.join(BASE_DIR, "YT_video_folder")
    if not os.path.exists(yt_video_folder):
        os.makedirs(yt_video_folder)

    try:
        info = await asyncio.to_thread(lambda: yt_dlp.YoutubeDL().extract_info(link, download=False))
        original_title = sanitize_filename(info['title'])
        unique_filename = get_unique_filename(yt_video_folder, original_title, "mp4")
        video_file = os.path.join(yt_video_folder, unique_filename)

        ydl_opts = {
            'outtmpl': video_file,
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [link])

        if os.path.exists(video_file):
            file_size_mb = os.path.getsize(video_file) / (1024 * 1024)
            print(f"📁 File downloaded: {video_file}")
            print(f"📏 File size: {file_size_mb:.2f} MB")
            await send_log_message(f"📁 **Downloaded:** {video_file}\n📏 **Size:** {file_size_mb:.2f} MB")

            if file_size_mb <= 8.0:
                await ctx.send(file=discord.File(video_file))
            else:
                await ctx.send(f"✅ Successfully downloaded \nSize: {file_size_mb:.2f} MB (Too large to send on Discord)")

    except Exception as e:
        error_message = str(e)
        await ctx.send(f"❌ There was an error downloading the video: {error_message}")
        error_message = f"⚠️ **Error:** {error_message}"
        print(error_message)
        await send_log_message(error_message)



#!-------------------------------------------------------------------------------------------------------------------------------------!#


@bot.command(name='lmp3')
async def download_youtube_audio(ctx, link: str):
    """Download a YouTube video and extract the audio as MP3."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{ctx.author.name}#{ctx.author.discriminator}"

    log_message = (
        f"\n‎ \n‎"
        f"--------------------------------------------\n"
        f"🎵 **New Audio Download Request**\n"
        f"👤 **User:** {user_info}\n"
        f"📅 **Time:** {current_time}\n"
        f"🌐 **Link:** {link}\n"
        f"--------------------------------------------"
    )
    print(log_message)
    await send_log_message(log_message)

    await ctx.send("give me a minute... 🎶")

    # Folder to save the MP3 files
    yt_audio_folder = os.path.join(BASE_DIR, "YT_audio_folder")
    if not os.path.exists(yt_audio_folder):
        os.makedirs(yt_audio_folder)

    try:
        # Extract video metadata
        info = await asyncio.to_thread(lambda: yt_dlp.YoutubeDL().extract_info(link, download=False))
        original_title = sanitize_filename(info['title'])
        unique_filename = get_unique_filename(yt_audio_folder, original_title, "mp3")
        output_path = os.path.join(yt_audio_folder, unique_filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': r'C:/ffmpeg',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [link])

        if os.path.exists(output_path):
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"🎧 MP3 downloaded: {output_path}")
            print(f"📏 File size: {file_size_mb:.2f} MB")
            await send_log_message(f"🎧 **Audio Saved:** {output_path}\n📏 **Size:** {file_size_mb:.2f} MB")

            if file_size_mb <= 8.0:
                await ctx.send("✅ Success!", file=discord.File(output_path))
            else:
                await ctx.send(f"✅ Successfully downloaded and converted to MP3! Size: {file_size_mb:.2f} MB (Too large to send in Discord)")

    except Exception as e:
        error_message = str(e)
        await ctx.send(f"❌ There was an error downloading the audio: {error_message}")
        error_message = f"⚠️ **Audio Download Error:** {error_message}"
        print(error_message)
        await send_log_message(error_message)


#!-------------------------------------------------------------------------------------------------------------------------------------!#

#dsleep
@bot.command(name='sleep')
@only_prefix('!')
async def shutdown(ctx):
    """Shutdown the bot"""
    if ctx.author.id == SAUCE_ID:  # Replace with your Discord user ID to restrict access to only you
        await ctx.message.add_reaction("😴")
        print("Shutdown command triggered by:", ctx.author.name)  # Logs when the command is called
    
        # Send the alert to each channel in the list
        for channel_id in alert_channel_ids:
            alert_channel = bot.get_channel(channel_id)
            if alert_channel:
                await alert_channel.send("Oomfie is sleeping... 😴")
        
        await bot.close()  # This will stop the bo
    else:
        await ctx.message.add_reaction("❌")
        await ctx.send("I dont want to.")
        print("Shutdown command attempted by:", ctx.author.name)  # Logs unauthorized attempts
 
#!-------------------------------------------------------------------------------------------------------------------------------------!#

async def delete_past_messages():
    """Delete past messages containing the specific words, with rate limit handling."""
    for channel_id in alert_channel_ids:
        alert_channel = bot.get_channel(channel_id)
        if alert_channel:
            try:
                async for message in alert_channel.history(limit=200):
                    # Skip the newest message for this channel
                    if message.id == newest_message_ids.get(channel_id):
                        continue  # Skip the newest message for this channel

                    if "**Oomfie is online and doomscrolling** 💚" in message.content or "Oomfie is sleeping... 😴" in message.content:
                        await delete_message_with_rate_limit(alert_channel, message)
            except discord.Forbidden:
                print(f"⚠️ No permission to read or delete messages in {alert_channel.name}")
            except discord.HTTPException as e:
                print(f"⚠️ Failed to delete message in {alert_channel.name}: {e}")

#!-------------------------------------------------------------------------------------------------------------------------------------!#

async def delete_message_with_rate_limit(channel, message):
    """Delete a message with rate-limit handling."""
    try:
        await message.delete()
        print(f"Deleted message in {channel.name} from {message.author.name}")
    except discord.errors.HTTPException as e:
        # If the bot is rate-limited, Discord returns a 429 HTTP error
        if e.status == 429:
            retry_after = e.retry_after
            print(f"⚠️ Rate limited. Retrying after {retry_after} seconds...")
            await asyncio.sleep(retry_after)  # Wait for the retry time
            await message.delete()  # Retry deleting the message
            print(f"Deleted message in {channel.name} from {message.author.name} after rate limit.")
        else:
            raise e  # Raise other HTTP exceptions to be handled normally
        
#!-------------------------------------------------------------------------------------------------------------------------------------!#


@bot.command(name='commands')
@only_prefix('?')
async def commandhelp(ctx):
    await ctx.send(
                    "```\n"
                    "# 🤖 BOT COMMANDS\n"
                    "--------------------------------------------------------------------------------\n"
                    "?commands            → Show all available commands\n"
                    "!sleep               → Shut down the bot (admin only)\n"
                    "dl [FB/IG link]      → Download media from Facebook or Instagram [8mb limit]\n"
                    "dlyt [YouTube link]  → Download YouTube video (MP4) [8mb limit]\n"
                    "dlmp3 [YouTube link] → Download YouTube audio (MP3) [8mb limit]\n"
                    "--------------------------------------------------------------------------------\n"
                    "```"
                   )


    
    


    


bot.run(os.getenv("DISCORD_TOKEN"))
