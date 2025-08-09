"""
Bot settings and configuration constants.
"""

import discord

# Bot Configuration
BOT_NAME = "Avatar Realms Collide Bot"
BOT_VERSION = "1.8.0"
BOT_DESCRIPTION = "Unofficial community bot for Avatar Realms Collide"

# Discord Links
DISCORD_SERVER_LINK = "https://discord.gg/a3tGyAwVRc"
BOT_INVITE_LINK = "https://discord.com/oauth2/authorize?client_id=1242988284347420673&permissions=274877910016&scope=bot%20applications.commands"
DEVELOPMENT_SERVER_LINK = "https://discord.gg/a3tGyAwVRc"  # Development server for contributions

# Command Configuration
COMMAND_PREFIX = "!"
DEFAULT_COOLDOWN = 3.0  # seconds

# Embed Colors
EMBED_COLORS = {
    "success": discord.Color.green(),
    "error": discord.Color.red(),
    "warning": discord.Color.orange(),
    "info": discord.Color.blue(),
    "primary": discord.Color.purple(),
    "secondary": discord.Color.dark_blue()
}

# Game Information
GAME_NAME = "Avatar Realms Collide"
GAME_DESCRIPTION = "A fantasy RPG game with unique characters and abilities"

# Disclaimer
DISCLAIMER = (
    "⚠️ **Disclaimer**: This is an unofficial, fan-made Discord bot and is "
    "not affiliated with, endorsed by, or sponsored by the developers of "
    "Avatar Realms Collide. All game data used is from publicly available "
    "sources or mock data for demonstration purposes."
)

# File Paths
DATA_DIR = "data"
CHARACTERS_DIR = f"{DATA_DIR}/characters"
EVENTS_DIR = f"{DATA_DIR}/events"
IMAGES_DIR = "images"
CHARACTER_IMAGES_DIR = f"{IMAGES_DIR}/characters"
SKILL_IMAGES_DIR = f"{IMAGES_DIR}/skills"
TALENT_IMAGES_DIR = f"{IMAGES_DIR}/talents"

# Pagination
ITEMS_PER_PAGE = 10

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "bot.log"

# Error Messages
ERROR_MESSAGES = {
    "character_not_found": "Character not found. Use `!characters` to see available characters.",
    "skill_not_found": "Skill not found for this character.",
    "talent_not_found": "Talent tree not found for this character.",
    "event_not_found": "Event not found. Use `!events` to see available events.",
    "permission_denied": "You don't have permission to use this command.",
    "invalid_argument": "Invalid argument provided.",
    "data_error": "Error loading data. Please try again later."
}

# Success Messages
SUCCESS_MESSAGES = {
    "command_executed": "Command executed successfully!",
    "data_loaded": "Data loaded successfully!",
    "settings_updated": "Settings updated successfully!"
} 