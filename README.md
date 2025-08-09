<p align="center">
  <strong>🚀 Add the Avatar Realms Collide Bot to Your Server!</strong><br><br>
  <a href="https://discord.com/oauth2/authorize?client_id=1242988284347420673&permissions=274877910016&scope=bot%20applications.commands">
    <img alt="Add Bot to Server" src="https://img.shields.io/badge/Add%20Bot%20to%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  </a>
  <br>
</p>

# 🌟 Avatar Realms Collide Discord Bot

[![Version](https://img.shields.io/badge/version-1.8.0-blue.svg)](https://github.com/M1tsumi/ArcPythonBot)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-purple.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> **🎮 Version 1.8.0 - Avatar Realms Collide Discord Bot**  
> An interactive Discord bot featuring hero progression, elemental skills, PvP duels, character talent trees, leaderboards, rally system, and comprehensive game management for the Avatar Realms Collide universe.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Commands](#-commands)
- [Character Database](#-character-database)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

## ✨ Features

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
| `/tgl` | The Greatest Leader event information | Event details, stages, rewards |
| `/tgl_calc` | Calculate TGL points for activities | Point calculation tool |
| `/events` | List current and upcoming events | View all available events (dates/times WIP) |
| `/event_details` | Get detailed information about specific events | Event mechanics, tips, rewards (dates/times WIP) |
| `/upcoming` | Show upcoming events only | Future event information (dates/times WIP) |
| `/event_search` | Search for events by name or description | Find specific events (dates/times WIP) |
| `/event_rewards` | Show rewards for a specific event | Detailed reward breakdown (dates/times WIP) |

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

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🗺️ Roadmap

### Version 1.8.0 (Current) 🚀 MAJOR RELEASE
- ✅ **Hero Progression System**: Complete rarity and star upgrade system
- ✅ **Elemental Skill Trees**: 44 skills across 4 elements with tier progression
- ✅ **PvP Duel System**: Turn-based combat with ELO rating system
- ✅ **Achievement System**: 18+ unique achievements with rewards
- ✅ **Enhanced Global Profiles**: Cross-server progression tracking
- ✅ **Combat Mechanics**: Element advantages, critical hits, evasion system
- ✅ **Duel Statistics**: Comprehensive battle performance tracking
- ✅ **Interactive Battle UI**: Real-time combat interface
- ✅ **Resource Economy**: Hero Shards, Scrolls, and Skill Points integration
- ✅ **Minigame Enhancements**: Improved drop rates and duel bonuses
- ✅ **New Commands**: `/hero`, `/skills`, `/duel` command groups (10 new commands)
- ✅ Interactive talent tree browser
- ✅ **Leaderboard System**: Complete with admin controls and event-aware pausing
- ✅ **Rally System**: Complete Shattered Skulls Fortress management
- ✅ **TGL System**: The Greatest Leader event tools and point calculator
- ✅ **Glorious Victory System**: Complete event information and point calculator
- ✅ **Purification Event System**: Complete 30-level progressive challenge event
- ✅ **Hero Information System**: Comprehensive hero guide and unlock methods
- ✅ **Timer System**: Game activity timers with DM notifications
- ✅ **Performance Optimizations**: Embed caching and faster operations
- ✅ Character database with 25+ characters and unlock information
- ✅ Element-based categorization with rarity system
- ✅ Professional Discord UI with interactive components

### Upcoming Features
- 🔄 **Advanced PvP**: Tournament system and seasonal rankings
- 🔄 **Guild System**: Alliance-based progression and battles
- 🔄 **Daily Quests**: Regular challenges for additional rewards
- 🔄 **Equipment System**: Gear and artifacts for heroes
- 🔄 **Prestige System**: Advanced progression beyond Legendary
- 🔄 **Real-time Events**: Live game event integration
- 🔄 **Mobile Optimization**: Better mobile Discord experience
- 🔄 **Advanced Analytics**: Detailed battle and progression statistics

### Future Updates
- **Real-time Data**: Live game data integration
- **Analytics**: Usage statistics and insights
- **Customization**: User preference settings
- **API Integration**: External game API support

## 📝 Version Notes

### Version 1.6.2
This is a **major feature release** with comprehensive troops system:

- **Troops System**: Complete troops information and management with `/troops` command
- **Interactive Element Selection**: Choose from Water, Earth, Fire, and Air elements
- **Tier-based Browsing**: Browse troops by tiers T1-T6 with detailed information
- **Professional UI**: Color-coded element buttons with emojis and visual styling
- **Comprehensive Data**: Detailed troop stats, costs, and element-specific descriptions
- **Enhanced Navigation**: Interactive tier selection with professional embeds
- **Element Overviews**: Strategic information for each element's troop characteristics
- **New Cog**: Added `troops.py` with 315 lines of troop management functionality
- **Improved Data Management**: Enhanced data parser and embed generation for troops

### Version 1.6.1
This is a **minor update** with acknowledgments and UI improvements:

- **Added Kuvira**: Added Kuvira to the acknowledgments section
- **Optimized `/info` Command**: Streamlined the info command to be more concise and user-friendly
- **All Contributors Listed**: Now properly credits all contributors including Lycaris, PrincessBell, Samkee, and Kuvira
- **Reduced Text Wall**: Condensed verbose descriptions into concise, readable format
- **Better UX**: Much easier to read and digest information
- **Maintained Functionality**: All essential information preserved while improving readability

### Version 1.6.0
This is a **major feature release** with comprehensive event systems and timer functionality:

- **Purification Event System**: Complete 30-level progressive challenge event with detailed mechanics
- **Event Management**: Comprehensive event system with `/events`, `/event_details`, `/upcoming`, `/event_search`, `/event_rewards`
- **Progressive Challenge**: 30 levels with 6 different enemy types and increasing rewards
- **Alliance Cooperation**: Enhanced rewards through alliance coordination and strategy
- **Timer System**: Complete game activity timer with DM notifications
- **Activity Tracking**: Support for Recruiting, Gathering, Build 1, Build 2, Research, and Event
- **Custom Duration**: Flexible time input up to 24 hours (hours, minutes, seconds)
- **Timer Management**: View, cancel individual timers, or cancel all timers
- **Notes Support**: Optional notes to remember what each timer is for
- **Real-time Updates**: Automatic timer checking every 30 seconds
- **New Commands**: `/timer`, `/timers`, `/cancel_timer`, `/cancel_all_timers`, `/timer_help`
- **Event Commands**: `/events`, `/event_details`, `/upcoming`, `/event_search`, `/event_rewards`
- **DM Notifications**: Private messages when timers complete
- **Professional UI**: Clean embeds with timer information and management

### Version 1.5.0
This is a **major feature release** with comprehensive event systems and hero information:

- **Glorious Victory System**: Complete event information, point calculator, and strategy guide
- **Hero Information System**: Comprehensive hero guide with unlock methods and rarity classification
- **Enhanced Character Database**: Added unlock sources and detailed hero information
- **New Commands**: `/glorious_victory`, `/gv_calc`, `/hero_info`, `/hero_search`
- **Event Integration**: Seamless integration of multiple event systems
- **Improved Data Management**: Better organization of hero and event data
- **Professional UI**: Enhanced embeds and interactive components
- **Performance Optimizations**: Continued improvements in speed and efficiency

### Version 1.4.0
Previous stable release with leaderboard management, rally system, and performance optimizations:

- **Leaderboard Management**: Complete admin controls for pausing, resuming, and clearing leaderboards
- **Event-Aware System**: Automatic leaderboard pausing when events are not active
- **Rally System**: Complete Shattered Skulls Fortress management with time limits and point tracking
- **Performance Optimizations**: Embed caching, optimized operations, and enhanced logging
- **New Commands**: `/ping`, `/info`, `/rally`, `/rally_stats`, `/rally_leaderboard`, `/leader`
- **Creator Restrictions**: Rally creators cannot join their own rallies
- **Auto-cleanup**: Automatic expiration and creator notifications
- **Professional UI**: Enhanced embeds and interactive buttons
- **Data Persistence**: JSON-based storage for rally statistics, leaderboard state, and configuration

### Planned Future Updates
- **Skill Priorities**: Character skill tree progression system
- **Rarity Changes**: Dynamic character rarity updates based on game balance
- **Level Requirements**: Character level progression and requirements
- **Resource Requirements**: Game resource costs and management
- **Advanced Analytics**: Detailed character and game statistics
- **Event Integration**: Real-time game event tracking
- **User Customization**: Personalized bot experience settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Avatar: The Last Airbender** universe for inspiration
- **Discord.py** community for excellent documentation
- **Contributors** who help improve this bot
- **[Lycaris](https://lycaris.notion.site/A-RC-Event-Overview-20388d602bb58085b119da5f6f612cbe)** for the comprehensive Avatar Realms Collide Event Overview
- **PrincessBell** and **Samkee** for providing event details
- **Deng (@2rk)** for leaderboard data contributions and improvements
- **Kuvira** for contributing talent trees, skill priorities, and town hall statistics to the bot's development
- **Drummer (@priskent)** and **Marshmellow (@sophremacy)** for providing troop information and costs data

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/ArcPythonBot/issues)
- **Discord Server**: Join our community server for support
- **Documentation**: Check out [Lycaris' Notion Page](https://lycaris.notion.site/A-RC-Event-Overview-20388d602bb58085b119da5f6f612cbe) for detailed guides

---

**⭐ Star this repository if you find it helpful!**

*Made with ❤️ for the Avatar Realms Collide community* 
