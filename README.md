<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Video Downloader Discord Bot</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f4f4f9;
      color: #333;
    }
    .container {
      max-width: 800px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    h1, h2 {
      text-align: center;
      color: #4a4e69;
    }
    h1 {
      margin-bottom: 0;
    }
    p, li {
      line-height: 1.6;
    }
    .note {
      background-color: #fff3cd;
      border-left: 6px solid #ffc107;
      padding: 10px 15px;
      margin: 20px 0;
      border-radius: 5px;
    }
    .section {
      margin-bottom: 30px;
    }
    ul {
      padding-left: 20px;
    }
    a {
      color: #0077cc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    code {
      background-color: #f1f1f1;
      padding: 2px 5px;
      border-radius: 3px;
    }
    pre {
      background-color: #f1f1f1;
      padding: 15px;
      border-radius: 8px;
      overflow-x: auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🍵 YouTube/Facebook/Instagram Video Downloader Discord Bot 🍵</h1>

    <p>I made this Python-based code that lets you download videos from <strong>Facebook Reels</strong>, <strong>Instagram Reels</strong>, and <strong>YouTube Shorts</strong> using your own Discord bot. Just send a video link in your Discord channel and the bot will fetch and send the downloaded video directly for you.</p>

    <p>It's super handy for sharing reels with friends on Discord—no need to deal with ad-heavy websites!</p>

    <div class="note">
      ⚠️ This was created for personal and educational purposes, so it may not be fully optimized.
    </div>

    <div class="section">
      <h2>✅ Features</h2>
      <ul>
        <li>Downloads Facebook videos</li>
        <li>Downloads Instagram videos</li>
        <li>Downloads YouTube videos</li>
        <li>Converts YouTube videos to MP3</li>
      </ul>
    </div>

    <div class="section">
      <h2>❗ Limits</h2>
      <ul>
        <li>Maximum file size is <strong>8MB</strong> (Discord file upload limit for bots)</li>
      </ul>
    </div>

    <div class="section">
      <h2>🤖 Invite the Bot</h2>
      <p>Want to try it out?</p>
      <p><a href="https://discord.com/oauth2/authorize?client_id=1352919755023188021&permissions=1689934340029504&integration_type=0&scope=bot+applications.commands" target="_blank">Click here to invite the bot to your server</a></p>
      <div class="note">
        Make sure the bot has permission to read messages and send files in your Discord channel. <br>
        Note: This bot was made by me and is not online 24/7. It runs locally on my computer since I don’t have the financial means to host it continuously.
      </div>
    </div>

    <div class="section">
      <h2>🔧 How to Use</h2>
      <p>These are the bot commands:</p>
      <pre><code># 🤖 BOT COMMANDS
--------------------------------------------------------------------------------
?commands            → Show all available commands
!sleep               → Shut down the bot (admin only)
dl [FB/IG link]      → Download media from Facebook or Instagram [8mb limit]
dlyt [YouTube link]  → Download YouTube video (MP4) [8mb limit]
dlmp3 [YouTube link] → Download YouTube audio (MP3) [8mb limit]
--------------------------------------------------------------------------------</code></pre>
    </div>

    <div class="section">
      <h2>🛠️ Create Your Own Bot</h2>

      <h3>✅ Requirements</h3>
      <ul>
        <li>Windows OS</li>
        <li>Visual Studio Code</li>
      </ul>

      <h3>🔧 Instructions</h3>
      <ol>
        <li><strong>Create a Discord Bot</strong><br>
          Go to the <a href="https://discord.com/developers/applications" target="_blank">Discord Developer Portal</a> and create your bot. Save the token for later.
        </li>
        <li><strong>Install Python 3.10+</strong><br>
          <a href="https://www.python.org/downloads/" target="_blank">Download Python here</a>.  
          Make sure to check <code>Add Python to PATH</code> during installation.
        </li>
        <li><strong>Install FFmpeg</strong><br>
          Download FFmpeg 7.1 (Windows 64-bit).  
          <ul>
            <li>Extract the ZIP file</li>
            <li>Copy the path to the <code>bin</code> folder (e.g., <code>C:\ffmpeg\bin</code>)</li>
            <li>Go to <strong>System Properties > Environment Variables</strong></li>
            <li>Under System variables, select <strong>Path > Edit > New</strong>, then paste the path</li>
            <li>Click OK to save</li>
            <li>Need help? <a href="https://www.youtube.com/watch?v=JR36oH35Fgg" target="_blank">Watch this video</a></li>
          </ul>
        </li>
        <li><strong>Install pip (if not installed)</strong><br>
          Check with: <code>pip --version</code><br>
          Not installed? <a href="https://pip.pypa.io/en/stable/installation/" target="_blank">Follow this guide</a>.
        </li>
        <li><strong>Install Python Dependencies</strong><br>
          Run the following commands:
          <pre><code>pip install ffmpeg-python  
pip install yt-dlp  
pip install discord.py  
pip install python-dotenv</code></pre>
        </li>
      </ol>
    </div>

    <div class="section">
      <h2>📁 Required Files</h2>
      <ul>
        <li><code>.env</code> – Store your Discord bot token and sensitive info</li>
        <li><code>cookies.txt</code> – Store Facebook/Instagram cookies (for some reels)</li>
        <li><code>config.py</code> – Add your Discord user ID, channel ID, and settings</li>
      </ul>
    </div>
  </div>
</body>
</html>
