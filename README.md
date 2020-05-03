# Cathode

Cathode is a simple and modular Discord bot that powers [ShugaBot](https://shuga.co/discord/).

### Configuration

1. Install any dependencies.

```bash
sudo apt update
sudo apt install -y python3.6  # Installs Python 3.6. It may already be installed.
sudo apt install -y libopus-dev libssl-dev libffi-dev build-essential git ffmpeg unzip
sudo pip3 install -r requirements.txt
```

2. Set up the bot account.

- Go to the [Discord developer portal](https://discordapp.com/developers/applications)
- Create a new application, and enable it as a bot.
- Copy the token of the bot. It should be a long string of random letters and numbers.
- Consider repeating these steps a second time to create a "testing" bot.

3. Configure the `config.json` file

```bash
cp config.json.example config.json
```

```json
{
    "admins": [NON_OWNER_DISCORD_ID, ANOTHER_TRUSTED_DISCORD_ID],
    "version": "3.0.0",
    "betaToken": "BOT_TOKEN_WHEN_IN_DEV",
    "token": "BOT_TOKEN_WHEN_IN_PROD",
    "prefix": "/",
    "gamePlaying": "open-source software!",
    "color": "0x27A4EB",
    "url": "https://example.com/",
    "about": "Cathode is a simple and modular Discord bot.",
    "verified": "False"
}
```

- `admins`: A list of numerical Discord user IDs of non-owners to give owners. To get a user ID, please read [this tutorial from Discord](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-).
    - This does not include your user ID. Cathode trusts this automatically.
    - Is exposed as `Bot.trustedUsers`
- `version`: The version of the bot. Is exposed as `Bot.cathodeVersion`.
- `token`: Your Discord bot token from step 2.
- `betaToken`: A bot token to use when `__debugMode__` is set to `True` in `index.py`. This can be the same as the above token or a separate account altogether.
- `prefix`: The prefix for your bot's commands.
- `gamePlaying`: The bot's "Playing" status. Is exposed as `Bot.gamePlaying`.
- `color`: The default color for embeds. Is exposed as `Bot.color`
- `url`: A link for your name. Used in the `about` command.
- `about`: A summary of your bot. Used in the `help` command.
- `verified`: If your bot is verified by Discord. Setting to `True` surpresses server cap notifications.

4. Write commands!

You can either use the provided example cogs or write your own. Please check the [DiscordPy](https://discordpy.readthedocs.io/en/latest/) docs on how to write commands.

Feel free to use the cogs provided to help write your own.

*Note: Cathode is NOT compatibile with Red-DiscordBot cogs out of the box. They should be relatively easy to adapt though.*

5. Start the bot.

```bash
python3 index.py
```

*Note: Consider running this in the backround for the best results. I quite like [`pm2`](https://github.com/Unitech/pm2); it's easy to use and manage processes with.*