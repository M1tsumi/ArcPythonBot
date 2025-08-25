# ⚠️ PROJECT STATUS: NO LONGER MAINTAINED

> **Important Notice**: This Discord bot is no longer actively maintained or updated. The code remains available for educational purposes and community use, but no new features, bug fixes, or support will be provided.

<p align="center">
  <strong>🤝 Need a Custom Discord Bot? I'm Here to Help!</strong><br><br>
  <a href="https://www.fiverr.com/s/XLzopGe">
    <img alt="Custom Bot Development on Fiverr" src="https://img.shields.io/badge/Custom%20Bot%20Development-00b22d?style=for-the-badge&logo=fiverr&logoColor=white">
  </a>
  <br><br>
  <strong>🚀 Add the Avatar Realms Collide Bot to Your Server!</strong><br><br>
  <a href="https://discord.com/oauth2/authorize?client_id=1242988284347420673&permissions=274877910016&scope=bot%20applications.commands">
    <img alt="Add Bot to Server" src="https://img.shields.io/badge/Add%20Bot%20to%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  </a>
  <br>
</p>

# 🌟 Avatar Realms Collide Discord Bot

[![Version](https://img.shields.io/badge/version-1.8.1-blue.svg)](https://github.com/M1tsumi/ArcPythonBot)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-purple.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-archived-red.svg)](https://github.com/M1tsumi/ArcPythonBot)

> **🎮 Version 1.8.1 - Avatar Realms Collide Discord Bot**  
> An interactive Discord bot featuring hero progression, elemental skills, PvP duels, character talent trees, leaderboards, rally system, comprehensive game management, and **multi-language support** for the Avatar Realms Collide universe.

## 📋 Table of Contents

- [Project Status](#-project-status-no-longer-maintained)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Commands](#-commands)
- [Character Database](#-character-database)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🌍 **Multi-Language Support** ⭐ NEW in v1.8.1
- **Complete Translation System**: Full support for English, German, and Spanish
  - **169 Translation Keys**: Comprehensive coverage across all bot features
  - **User Language Preferences**: Individual language settings per user
  - **Dynamic Translation**: Real-time language switching with `/language` command
  - **Fallback System**: Automatic fallback to English for missing translations
  - **Variable Interpolation**: Support for dynamic content (e.g., `{username}`, `{count}`)
- **Language Commands**: Easy language management
  - `/language <code>` - Set your preferred language (EN/DE/ES)
  - `/currentlanguage` - Check your current language setting
  - `!language <code>` - Traditional command support
  - `!currentlanguage` - Check language with traditional command

### 🦸 **Hero Progression System** ⭐ NEW in v1.8.0
- **Rarity Advancement**: Progress heroes from Rare → Epic → Legendary
- **Star System**: Upgrade heroes through 6 star levels with stat scaling
- **Element Selection**: Choose from Fire, Water, Earth, and Air elements
- **Resource Management**: Use Hero Shards and Scrolls for upgrades
- **Global Profile Integration**: Track all heroes across servers

### ⚔️ **Elemental Skill Trees** ⭐ NEW in v1.8.0
- **44 Unique Skills**: Master abilities across all 4 elements
- **Tiered Progression**: Unlock skills through Basic → Advanced → Master → Ultimate tiers
- **Skill Point Economy**: Earn and spend skill points strategically
- **Bonus Calculations**: Automatic stat bonuses from unlocked skills
- **Prerequisites System**: Logical skill progression paths

### 🎯 **PvP Duel System** ⭐ NEW in v1.8.0
- **Turn-based Combat**: Strategic battles using hero stats and skills
- **Element Advantages**: Fire > Air > Earth > Water > Fire combat triangle
- **ELO Rating System**: Competitive ranking with Bronze to Grandmaster tiers
- **Battle Statistics**: Track wins, losses, damage dealt, streaks, and more
- **Achievement System**: 18+ unique achievements with rewards
- **Interactive UI**: Real-time battle interface with action choices

### 🏆 **Enhanced Leaderboards** 📈 Updated in v1.8.0
- **Duel Rankings**: Top duelists by rating, wins, and performance
- **Global Profiles**: Cross-server progression tracking
- **Multiple Categories**: Leaders, alliances, duel champions, and more
- **Real-time Updates**: Live ranking adjustments

### 🎯 **Interactive Talent Tree Browser**
- **Element-based Navigation**: Browse characters by Fire, Water, Earth, and Air elements
- **Character Profiles**: Detailed character information with rarity, element, and category
- **Talent Tree Images**: View both talent tree variations for each character
- **Professional UI**: Clean, minimalist embeds with personalized messaging

### 🏆 **Leaderboard System**
- **Two Sources**: Pulls from text files for long-form rankings and internal state for live snapshots
  - Text files: `text files/leader-ranks.txt` and `text files/alliance-ranks.txt`
  - Expected format: first non-empty line as a header (may include date), followed by lines starting with ranked numbers like `1.`
  - Header date is preserved to indicate the day rankings were checked
- **Pagination**: Monospaced, 20-rows-per-page embeds with Prev/Next navigation for long leaderboards
- **Interactive Buttons**: Instant switch between 👑 Leaders and 🤝 Alliances
- **Graceful Errors**: Clear guidance when files are missing or incorrectly formatted
- **Admin Controls**: Pause/resume/clear leaderboards during non-event periods
- **Event-Aware**: Automatic pause when Glorious Victory event is not active

### 🏰 **Rally System**
- **Shattered Skulls Fortress**: Create and join rallies for levels 1-6
- **Time Limits**: Configurable durations (5m, 15m, 30m, 1hr)
- **Point System**: Automatic point tracking and rewards
- **Real-time Updates**: Live player count and status tracking
- **Professional Embeds**: Beautiful rally management interface
- **Creator Restrictions**: Prevent creators from joining own rallies
- **Auto-cleanup**: Automatic expiration and notifications

### 🏆 **TGL System**
- **The Greatest Leader**: Comprehensive event information and tools
- **Event Stages**: Detailed breakdown of all 5 daily stages
- **Point Calculator**: Calculate points for any TGL activity
- **Rewards Guide**: Daily and overall ranking rewards
- **Strategy Tips**: Event optimization and planning tools
- **Single/Cross Server**: Support for both event types

### 🏆 **Glorious Victory System**
- **Event Information**: Complete Glorious Victory event details
- **Point Calculator**: Calculate points for fortress destruction activities
- **Rewards Guide**: Daily and overall ranking rewards
- **Strategy Tips**: Event optimization and planning tools
- **Activity Breakdown**: Detailed point values for all activities
- **Event Stages**: Comprehensive stage-by-stage information

### 🛠️ **Purification Event System**
- **Progressive Challenge**: 30-level progressive event with increasing difficulty
- **Event Information**: Complete Purification event details and mechanics
- **Rewards Guide**: Detailed rewards for each level (1-30)
- **Strategy Tips**: Event optimization and alliance coordination strategies
- **Enemy Types**: 6 different Shattered Skull variants (Fuzhi, Toghrul, Amur, Lushan, Kyro, Chanyu)
- **Alliance Cooperation**: Enhanced rewards through alliance coordination

### 🦸 **Hero Information System**
- **Complete Hero Guide**: Comprehensive information about all heroes
- **Unlock Methods**: Detailed guide on how to obtain hero shards (all heroes require 10 shards to unlock)
- **Rarity Classification**: Legendary, Epic, Rare, and Future heroes
- **Source Tracking**: All unlock sources and methods
- **Hero Search**: Search for specific hero information
- **Unlock Strategies**: Best practices for hero acquisition

### ⏰ **Timer System**
- **Game Activity Timers**: Track Recruiting, Gathering, Build 1, Build 2, Research, and Event activities
- **Custom Duration**: Flexible time input (hours, minutes, seconds)
- **DM Notifications**: Receive private messages when timers complete
- **Timer Management**: View, cancel individual timers, or cancel all timers
- **Notes Support**: Add optional notes to remember what each timer is for
- **Real-time Updates**: Automatic timer checking every 30 seconds

### ⚔️ **Troops System**
- **Interactive Troop Browser**: Complete troops information with `/troops` command
- **Troops Calculator**: Calculate troop recruitment costs with `/troopcalc` command
- **Element Selection**: Choose from Water, Earth, Fire, and Air elements
- **Tier-based Navigation**: Browse troops by tiers T1-T6 with detailed information
- **Professional UI**: Color-coded element buttons with emojis and visual styling
- **Comprehensive Data**: Detailed troop stats, costs, and element-specific descriptions
- **Strategic Information**: Element overviews and troop characteristics
- **Enhanced Navigation**: Interactive tier selection with professional embeds
- **Fixed Data Parsing**: Corrected troop data extraction with dynamic column mapping

### 📊 **Tier List**
- **/tierlist**: Displays the community hero tier list image. Place the image at `assets/images/leaderboards/hero-tierlist.webp` (PNG/JPG also supported).
- **Fixed in 1.7.1**: Command reliability improved; correctly detects and displays the tier list image when present.

### 👥 **Character Database**
- **25+ Characters**: Comprehensive roster from the Avatar universe
- **Element Classification**: Proper categorization by bending elements
- **Rarity System**: Common, Rare, Epic, Legendary, and Mythic tiers
- **Detailed Descriptions**: Rich character backgrounds and lore
- **Unlock Information**: Complete guide to obtaining hero shards

### ⚡ **Performance Optimizations**
### 📅 **Event Calendar Disclaimer** (New)
- Event dates/times are a Work In Progress and may be incorrect. This disclaimer is shown in event listings and details.
- **Embed Caching**: 5-minute cache for frequently used embeds
- **Optimized Operations**: Faster string processing and field generation
- **Enhanced Logging**: Structured output with timing information
- **Memory Management**: Efficient resource usage and cleanup

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Git

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ArcPythonBot.git
   cd ArcPythonBot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Create a .env file
   echo "DISCORD_TOKEN=your_bot_token_here" > .env
   ```

4. **Run the Bot**
   ```bash
   python main.py
   ```

## 📖 Usage

### Discord Commands
#### `/tierlist`
Show the community hero tier list image (if present on disk).

#### `/talent_trees`
Browse character talent trees by element:
- Select from Fire, Water, Earth, or Air elements
- View character profiles with stats and descriptions
- Access talent tree images for each character

#### `/leaderboard`
View top performers in the game:
- **👑 Top 10 Leaders**: Individual player rankings
- **🤝 Top 10 Alliances**: Alliance performance rankings
- **Event Status**: Shows pause status when events are not active

#### `/rally`
Create and manage Shattered Skulls Fortress rallies:
- **Level Selection**: Choose fortress levels 1-6
- **Time Limits**: Set duration (5m, 15m, 30m, 1hr)
- **Player Tracking**: Real-time join/leave management
- **Point Rewards**: Automatic point distribution

#### `/glorious_victory`
Access Glorious Victory event information:
- **Event Overview**: Complete event details and duration
- **Point Calculator**: Calculate points for fortress destruction
- **Rewards Guide**: Daily and overall ranking rewards
- **Strategy Tips**: Event optimization and planning

#### `/hero_info`
Comprehensive hero information system:
- **Hero Overview**: Complete guide to all heroes
- **Rarity Breakdown**: Legendary, Epic, Rare, and Future heroes
- **Unlock Sources**: Detailed guide to obtaining hero shards
- **Hero Search**: Find specific hero information

#### `/timer`
Set timers for game activities:
- **Activity Selection**: Choose from Recruiting, Gathering, Build 1, Build 2, Research, or Event
- **Custom Duration**: Set any duration up to 24 hours (e.g., 2h 30m, 45m, 1h 15m 30s)
- **Optional Notes**: Add notes to remember what each timer is for
- **DM Notifications**: Receive private messages when timers complete

#### `/ping` & `/info`
Bot status and information:
- **Performance Metrics**: Latency and response times
- **Bot Statistics**: Server count, user count, commands
- **Contribution Details**: How to contribute to the project
- **Development Server**: Link to community Discord

#### `/tgl` & `/tgl_calc`
The Greatest Leader event tools:
- **Event Information**: Overview, stages, and rewards
- **Point Calculator**: Calculate points for any activity
- **Strategy Guide**: Tips and optimization strategies
- **Stage Details**: Specific information for each day

## 🎮 Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/hero upgrade` | ⭐ Upgrade your hero's rarity and stars | Hero progression system |
| `/hero info` | ⭐ View detailed hero information | Complete hero stats and abilities |
| `/hero list` | ⭐ List all your heroes and progress | Personal hero collection |
| `/skills tree` | ⭐ Browse elemental skill trees | Interactive skill tree navigation |
| `/skills overview` | ⭐ View your skill progression | Personal skill advancement |
| `/skills upgrade` | ⭐ Unlock new elemental skills | Skill point spending |
| `/duel challenge` | ⚔️ Challenge another player to PvP | Strategic turn-based combat |
| `/duel stats` | ⚔️ View your duel statistics | Personal battle performance |
| `/duel leaderboard` | ⚔️ View top duelists rankings | Global competitive rankings |
| `/duel cancel` | ⚔️ Cancel pending duel challenge | Challenge management |
| `/tierlist` | Show community hero tier list | Sends image embed if file exists |
| `/talent_trees` | Interactive talent tree browser | Select element → Choose character → View trees |
| `/leaderboard` | View top leaders and alliances | Choose leaderboard type → View rankings |
| `/rally` | Create and manage rallies | Level → Time limit → Join/Leave system |
| `/rally_stats` | View personal rally statistics | Personal points and participation |
| `/rally_leaderboard` | View global rally leaderboard | Top players by rally points |
| `/glorious_victory` | Glorious Victory event information | Event details, stages, rewards |
| `/gv_calc` | Calculate Glorious Victory points | Point calculation tool |
| `/hero_info` | Hero information and unlock guide | Hero details, rarity, unlock methods |
| `/hero_search` | Search for specific hero information | Hero name search |
| `/timer` | Set a timer for game activities | Activity → Duration → Optional note |
| `/timers` | View your active timers | List all current timers |
| `/cancel_timer` | Cancel a specific timer | Timer ID → Cancel specific timer |
| `/cancel_all_timers` | Cancel all your timers | Remove all active timers |
| `/timer_help` | Get help with timer commands | Timer system guide |
| `/ping` | Check bot status and latency | Performance metrics and statistics |
| `/info` | Bot information and contribution details | Development server and features |
| `/setup` | Configure rally system (Admin) | Set rally channel for server |
| `/leader` | Admin leaderboard management | Pause/resume/clear leaderboards |
| `!addxp` | Add XP levels to user (Owner only) | Add whole levels to player progression |
| `/addxp` | Add XP levels to user (Owner only) | Add whole levels to player progression |
| `/tgl` | The Greatest Leader event information | Event details, stages, rewards |
| `/tgl_calc` | Calculate TGL points for activities | Point calculation tool |
| `/events` | List current and upcoming events | View all available events (dates/times WIP) |
| `/event_details` | Get detailed information about specific events | Event mechanics, tips, rewards (dates/times WIP) |
| `/upcoming` | Show upcoming events only | Future event information (dates/times WIP) |
| `/event_search` | Search for events by name or description | Find specific events (dates/times WIP) |
| `/event_rewards` | Show rewards for a specific event | Detailed reward breakdown (dates/times WIP) |

## 🔧 Admin Commands

| Command | Description | Usage | Permission |
|---------|-------------|-------|------------|
| `/setup` | Configure rally system | Set rally channel for server | Administrator |
| `/leader` | Leaderboard management | Pause/resume/clear leaderboards | Administrator |
| `!addxp` | Add XP levels to user | Add whole levels to player progression | Owner only |
| `/addxp` | Add XP levels to user | Add whole levels to player progression | Owner only |

### Admin Command Details

#### XP Management (`!addxp` / `/addxp`)
- **Owner-only access**: Only the bot owner can use these commands
- **Whole level progression**: Adds complete levels (not partial XP)
- **Avatar tokens**: Automatically awards tokens for level ups (10 tokens per level)
- **Safety limits**: Maximum 100 levels per command to prevent abuse
- **Detailed feedback**: Shows before/after levels, XP added, and tokens awarded

**Usage Examples:**
```bash
!addxp 5 @username    # Add 5 levels to user
/addxp levels:5 user:@username  # Slash command version
```

## 👥 Character Database

### Fire Element 🔥
- **Zuko** (Epic) - Fire Nation prince and Firebending master
- **Azula** (Legendary) - Firebending prodigy and Fire Nation princess
- **Iroh** (Legendary) - Wise Firebending master and Dragon of the West
- **Roku** (Legendary) - Fire Nation Avatar of balance and wisdom
- **Asami** (Epic) - Genius inventor and Fire Nation engineer

### Water Element 💧
- **Katara** (Epic) - Master Waterbender and skilled healer
- **Yue** (Rare) - Moon spirit and Water Tribe princess
- **Katara (Painted Lady)** (Legendary) - Mysterious Painted Lady
- **Unalaq** (Legendary) - Dark Waterbending master and spiritual leader
- **Korra** (Legendary) - Water Tribe Avatar of the modern era
- **Sokka** (Epic) - Strategic warrior and tactical leader
- **Amon** (Legendary) - Equalist leader and revolutionary

### Earth Element 🌍
- **Toph** (Epic) - Blind Earthbending master and Metalbender
- **King Bumi** (Epic) - Earthbending king and master strategist
- **Kyoshi** (Legendary) - Legendary Earth Kingdom Avatar of justice
- **Lin Beifong** (Legendary) - Metalbending police chief and protector
- **Teo** (Epic) - Air Nomad inventor and mechanical genius
- **Suki** (Epic) - Kyoshi Warrior leader and skilled fighter
- **Kuei** (Rare) - Earth Kingdom king and diplomatic leader

### Air Element 💨
- **Aang** (Legendary) - The last Airbender and Avatar of the world
- **Tenzin** (Epic) - Airbending master and spiritual teacher
- **Meelo** (Rare) - Young Airbending prodigy and energetic warrior
- **Yangchen** (Legendary) - Ancient Air Nomad Avatar of wisdom
- **Bumi** (Legendary) - Eccentric Airbending master and king
- **Borte** (Epic) - Water Tribe warrior and fierce protector

### Fire Element 🔥
- **Zuko** (Epic) - Fire Nation prince and Firebending master
- **Azula** (Legendary) - Firebending prodigy and Fire Nation princess
- **Iroh** (Legendary) - Wise Firebending master and Dragon of the West
- **Roku** (Legendary) - Fire Nation Avatar of balance and wisdom
- **Asami** (Epic) - Genius inventor and Fire Nation engineer
- **Piandao** (Rare) - Master swordsman and Fire Nation instructor

## 🔧 Technical Details

### Architecture
- **Discord.py 2.0+**: Modern Discord bot framework
- **Slash Commands**: Native Discord slash command support
- **Interactive UI**: Discord UI components for better UX
- **Modular Design**: Organized cog structure for maintainability

### File Structure
```
ArcPythonBot/
├── cogs/                 # Discord bot cogs
│   ├── talent_trees.py   # Talent tree browser
│   ├── leaderboards.py   # Leaderboard system
│   ├── rally_system.py   # Rally management
│   ├── tgl_system.py     # The Greatest Leader system
│   ├── glorious_victory.py # Glorious Victory system
│   ├── hero_info.py      # Hero information system
│   ├── timer_system.py   # Timer system for game activities
│   └── ...
├── utils/                # Utility modules
│   ├── data_parser.py   # Character data management
│   └── embed_generator.py
├── assets/images/        # Talent tree images
├── config/              # Configuration files
└── main.py              # Bot entry point
```

### Key Features
- **Character Data Management**: Centralized character database
- **Image Handling**: WebP talent tree image support
- **Error Handling**: Graceful error management
- **Caching**: Performance optimization with data caching
- **Event Systems**: TGL and Glorious Victory event management
- **Hero Information**: Complete hero unlock and rarity guide
- **Timer System**: Game activity timers with DM notifications

## 🤝 Contributing

> **Note**: While this project is no longer actively maintained, the code remains open source under the MIT License. Community members are welcome to fork the repository and continue development independently.

### Historical Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🗺️ Final Version Features

### Version 1.8.1 (Final Release) 🚀
- ✅ **Multi-Language Support**: Complete translation system with English, German, and Spanish
- ✅ **Hero Progression System**: Complete rarity and star upgrade system
- ✅ **Elemental Skill Trees**: 44 skills across 4 elements with tier progression
- ✅ **PvP Duel System**: Turn-based combat with ELO rating system
- ✅ **Achievement System**: 18+ unique achievements with rewards
- ✅ **Enhanced Global Profiles**: Cross-server progression tracking
- ✅ **Combat Mechanics**: Element advantages, critical hits, evasion system
- ✅ **Duel Statistics**: Comprehensive battle performance tracking
- ✅ **Interactive Battle UI**: Real-time combat interface
- ✅ **Resource Economy**: Hero Shards, Scrolls, and Skill Points integration
- ✅ **Comprehensive Event Systems**: TGL, Glorious Victory, and Purification events
- ✅ **Rally System**: Complete Shattered Skulls Fortress management
- ✅ **Timer System**: Game activity timers with DM notifications
- ✅ **Troops System**: Complete troop information and management
- ✅ **Performance Optimizations**: Embed caching and faster operations
- ✅ Character database with 25+ characters and unlock information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Avatar: The Last Airbender** universe for inspiration
- **Discord.py** community for excellent documentation
- **Contributors** who helped improve this bot:
  - **[Lycaris](https://lycaris.notion.site/A-RC-Event-Overview-20388d602bb58085b119da5f6f612cbe)** for the comprehensive Avatar Realms Collide Event Overview
  - **PrincessBell** and **Samkee** for providing event details
  - **Deng (@2rk)** for leaderboard data contributions and improvements
  - **Kuvira** for contributing talent trees, skill priorities, and town hall statistics
  - **Drummer (@priskent)** and **Marshmellow (@sophremacy)** for providing troop information and costs data

## 📞 Support

> **Support Notice**: As this project is no longer maintained, support is limited to community-driven assistance.

- **GitHub Issues**: Repository remains available for reference
- **Documentation**: Check out [Lycaris' Notion Page](https://lycaris.notion.site/A-RC-Event-Overview-20388d602bb58085b119da5f6f612cbe) for detailed guides
- **Community**: Fork the project to continue development

---

**⭐ This repository serves as an archive of the Avatar Realms Collide Discord Bot**

*Made with ❤️ for the Avatar Realms Collide community*
