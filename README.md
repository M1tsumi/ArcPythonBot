# Avatar Realms Collide Discord Bot

[![Beta Version](https://img.shields.io/badge/version-Beta-orange)](https://github.com/yourusername/ArcPythonBot)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-blue?logo=discord)](https://discord.gg/a3tGyAwVRc)

An unofficial Discord bot for the Avatar Realms Collide game, providing comprehensive information about characters, skills, talent trees, and game events.

> **⚠️ Beta Version**: This bot is currently in beta. Features may be added, removed, or changed without notice. Please report any issues or suggestions to help improve the bot.

## Features

- **Character Information**: Detailed character profiles with stats and abilities
- **Skill Details**: Comprehensive skill information with cooldowns and levels
- **Talent Trees**: Complete talent tree visualization with images and type information
- **Event Tracking**: Current and past event information
- **Search Functionality**: Search characters by name or description
- **User Profiles**: Personal favorite characters and preferences

## Commands

### Character Commands
- `!characters` - List all available characters
- `!character <name>` - Get detailed character information
- `!character_skills <name>` - Show character skills
- `!character_talent <name>` - Show character talent tree with images
- `!talent_trees` - List all available talent trees by type
- `!talent <character> <talent>` - Get detailed talent information
- `!search <term>` - Search for characters

### User Profile Commands
- `!myprofile` - Show your user profile
- `!setfavorite <character>` - Set your favorite character
- `!clearfavorite` - Clear your favorite character
- `!setpreference <key> <value>` - Set a preference
- `!clearpreference <key>` - Clear a preference

### Game Information
- `!events` - List current events
- `!leaderboard [type]` - Show leaderboards
- `!stats` - Show your statistics
- `!compare <char1> <char2>` - Compare two characters

## Talent Tree System

The bot includes a comprehensive talent tree system with:

### Talent Tree Types
- **Normal PvP Based Tree**: Standard combat-focused talent trees
- **Garrison Based Tree**: Defensive and garrison-focused talents
- **Siege Based Tree**: Siege and attack-focused talents
- **Shattered Skulls Based Tree**: Specialized combat talents
- **Gathering Based Tree**: Resource gathering and utility talents

### Talent Tree Features
- **Visual Talent Trees**: High-quality talent tree images for all 26 characters
- **Talent Type Information**: Each character's talent tree type and focus
- **Dual Purpose Design**: Trees may have multiple focuses for versatility
- **89 Total Points**: Maximum talent points for fully developed heroes
- **Visual Indicators**: Gold/blue for activated talents, red X for crossed-out talents

### Available Characters with Talent Trees
- **Normal PvP**: Kyoshi, Bumi, Korra, Toph, Azula, Iroh, Asami, Sokka, Suki, Zuko, Katara, Aang, Amon, King Bumi, Yangchen, Katara (Painted Lady), Unalaq, Roku, Lin Beifong
- **Garrison**: Tenzin
- **Siege**: Teo
- **Shattered Skulls**: Borte
- **Gathering**: Kuei, Meelo, Piandao, Yue

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your bot token in the environment
4. Run the bot: `python main.py`

## File Structure

```
ArcPythonBot/
├── cogs/                 # Discord bot command modules
├── config/              # Bot configuration and settings
├── data/                # Game data (characters, events)
├── HeroTalentImages/    # Talent tree images for all characters
├── images/              # Character and skill images
├── utils/               # Utility functions and data parsing
├── main.py              # Bot entry point
└── requirements.txt     # Python dependencies
```

## Talent Tree Images

The `HeroTalentImages/` directory contains talent tree images for all 26 characters:
- Each character has two talent tree versions (-1 and -2)
- Images are in WebP format for optimal quality and size
- Talent trees show the complete progression path with visual indicators
- Special handling for characters like "Katara (Painted Lady)" and "King Bumi"

## Community & Support

- **Discord Server**: [Join our community!](https://discord.gg/a3tGyAwVRc)
- **Issues**: Report bugs or request features on GitHub
- **Contributions**: Pull requests are welcome!

## Contributing

This is an unofficial fan-made bot. Contributions are welcome for:
- Adding new character data
- Improving talent tree visualizations
- Enhancing bot functionality
- Bug fixes and improvements

## Disclaimer

This is an unofficial, fan-made Discord bot and is not affiliated with, endorsed by, or sponsored by the developers of Avatar Realms Collide. All game data used is from publicly available sources or mock data for demonstration purposes. 