
# 🍵 YouTube/Facebook/Instagram Video Downloader Discord Bot 🍵

I made this Python-based code that lets you download videos from **Facebook Reels**, **Instagram Reels**, and **YouTube Shorts** using your own Discord bot. Just send a video link in your Discord channel and the bot will fetch and send the downloaded video directly for you.

It's super handy for sharing reels with friends on Discord—no need to deal with ad-heavy websites!

> ⚠️ **This was created for personal and educational purposes, so it may not be fully optimized.**

---

## ✅ Features

- Downloads Facebook videos  
- Downloads Instagram videos  
- Downloads YouTube videos  
- Converts YouTube videos to MP3  

---

## ❗ Limits

- Maximum file size is **8MB** (Discord file upload limit for bots)

---

## 🤖 Invite the Bot

Want to try it out?

👉 [Click here to invite the bot to your server](https://discord.com/oauth2/authorize?client_id=1352919755023188021&permissions=1689934340029504&integration_type=0&scope=bot+applications.commands)

> 📝 **Note:** This bot was made by me and is not online 24/7. It runs locally on my computer since I don’t have the financial means to host it continuously.

---

## 🔧 How to Use

These are the bot commands:

![Bot Command Screenshot](assets/commands.png)  


---

## 🛠️ Create Your Own Bot

### ✅ Requirements

- Windows OS  
- Visual Studio Code  

---

### 🔧 Instructions

1. **Create a Discord Bot**  
   Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create your bot. Save the token for later.

2. **Install Python 3.10+**  
   👉 [Download Python here](https://www.python.org/downloads/)  
   ✅ Make sure to check **"Add Python to PATH"** during installation.

3. **Install FFmpeg**  
   👉 [Download FFmpeg 7.1 (Windows 64-bit)](https://www.gyan.dev/ffmpeg/builds/)  
   Steps:
   - Extract the ZIP file
   - Copy the path to the `bin` folder (e.g., `C:\ffmpeg\bin`)
   - Open **System Properties > Environment Variables**
   - Under **System variables**, click **Path > Edit > New**, then paste the path
   - Click **OK** to save  
   📹 Need help? [Watch this video](https://www.youtube.com/watch?v=JR36oH35Fgg)

4. **Install pip (if not already installed)**  
   Check with:
   ```bash
   pip --version


## Not Installed?  
👉 [Follow this guide](https://pip.pypa.io/en/stable/installation/)  

---

5. **Install Python Dependencies**
Run the following commands:
  ```bash
  pip install ffmpeg-python
  pip install yt-dlp
  pip install discord.py
  pip install python-dotenv

---

## 📁 Required Files
Make sure these files are set up before running the bot:

.env – Store your Discord bot token and sensitive info

cookies.txt – Store Facebook/Instagram cookies (needed for some reels)

config.py – Add your Discord user ID, channel ID, and settings
