# Discord Python Bot
## How To Run

1. Download the latest version of [Python](https://www.python.org/downloads/).
2. [Ensure](https://pip.pypa.io/en/stable/installation/) pip package installer is properly installed.
3. pip install required packages.
4. Create a [Discord Bot](https://discord.com/developers/docs/intro) and update '[discord_bot_token.txt](discord_bot_token.txt)' with the new token.
5. If using audio features, install [FFmpeg](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/). Otherwise, disable audio commands in [app.py](app.py).
6. Run app.py.

### Install Packages

Python packages required to run:

1. [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)
2. [PyNaCl](https://pypi.org/project/PyNaCl/)

Install packages using pip package manager. Open a terminal/cmd window and enter the following commands.
```
pip install discord.py
pip install PyNaCl
```
## Where To Find Bot Token

The bot token is located under 'Public Key', as shown below. Copy this into '[discord_bot_token.txt](discord_bot_token.txt)' to link the python script with your bot. Alternatively, place your bot token directly into [app.py](app.py) (For reasons of security, this is not recommended).

![discorBot](https://user-images.githubusercontent.com/31321037/174897006-d3b54e75-32da-433a-bc53-53152a921c6b.png)
 
