# 🌟 Avatar Realms Collide Discord Bot

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/yourusername/ArcPythonBot)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-purple.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> **🎮 Version 1.4.0 - Avatar Realms Collide Discord Bot**  
> An interactive Discord bot for exploring character talent trees, leaderboards, rally system, and game information in the Avatar Realms Collide universe.

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

### 🎯 **Interactive Talent Tree Browser**
- **Element-based Navigation**: Browse characters by Fire, Water, Earth, and Air elements
- **Character Profiles**: Detailed character information with rarity, element, and category
- **Talent Tree Images**: View both talent tree variations for each character
- **Professional UI**: Clean, minimalist embeds with personalized messaging

### 🏆 **Leaderboard System**
- **Top 10 Leaders**: View the most powerful players
- **Top 10 Alliances**: Check the strongest alliances
- **Real-time Updates**: Regularly updated leaderboard data
- **Interactive Buttons**: Easy navigation between different rankings
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

### 👥 **Character Database**
- **25+ Characters**: Comprehensive roster from the Avatar universe
- **Element Classification**: Proper categorization by bending elements
- **Rarity System**: Common, Rare, Epic, Legendary, and Mythic tiers
- **Detailed Descriptions**: Rich character backgrounds and lore

### ⚡ **Performance Optimizations**
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

#### `/ping` & `/info`
Bot status and information:
- **Performance Metrics**: Latency and response times
- **Bot Statistics**: Server count, user count, commands
- **Contribution Details**: How to contribute to the project
- **Development Server**: Link to community Discord

## 🎮 Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/talent_trees` | Interactive talent tree browser | Select element → Choose character → View trees |
| `/leaderboard` | View top leaders and alliances | Choose leaderboard type → View rankings |
| `/rally` | Create and manage rallies | Level → Time limit → Join/Leave system |
| `/rally_stats` | View personal rally statistics | Personal points and participation |
| `/rally_leaderboard` | View global rally leaderboard | Top players by rally points |
| `/ping` | Check bot status and latency | Performance metrics and statistics |
| `/info` | Bot information and contribution details | Development server and features |
| `/setup` | Configure rally system (Admin) | Set rally channel for server |
| `/leader` | Admin leaderboard management | Pause/resume/clear leaderboards |

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
│   ├── slash_commands.py # Main slash commands
│   └── ...
├── utils/                # Utility modules
│   ├── data_parser.py   # Character data management
│   └── embed_generator.py
├── HeroTalentImages/     # Talent tree images
├── config/              # Configuration files
└── main.py              # Bot entry point
```

### Key Features
- **Character Data Management**: Centralized character database
- **Image Handling**: WebP talent tree image support
- **Error Handling**: Graceful error management
- **Caching**: Performance optimization with data caching

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🗺️ Roadmap

### Version 1.4.0 (Current)
- ✅ Interactive talent tree browser
- ✅ **Leaderboard System**: Complete with admin controls and event-aware pausing
- ✅ **Rally System**: Complete Shattered Skulls Fortress management
- ✅ **Performance Optimizations**: Embed caching and faster operations
- ✅ **New Commands**: `/ping`, `/info`, `/rally`, `/rally_stats`, `/rally_leaderboard`, `/leader`
- ✅ Character database with 25+ characters
- ✅ Element-based categorization
- ✅ Professional Discord UI
- ✅ **Creator Restrictions**: Rally creators cannot join own rallies
- ✅ **Time Limits**: Configurable rally durations with auto-cleanup
- ✅ **Point System**: Automatic tracking and rewards
- ✅ **Admin Controls**: Leaderboard pause/resume/clear functionality

### Upcoming Features
- 🔄 **Skill Priorities**: Character skill progression system
- 🔄 **Rarity Changes**: Dynamic rarity updates
- 🔄 **Level Requirements**: Character level progression
- 🔄 **Resource Requirements**: Game resource management
- 🔄 **Event System**: In-game event tracking
- 🔄 **User Profiles**: Player profile management
- 🔄 **Advanced Search**: Enhanced character search
- 🔄 **Mobile Optimization**: Better mobile Discord experience

### Future Updates
- **Real-time Data**: Live game data integration
- **Analytics**: Usage statistics and insights
- **Customization**: User preference settings
- **API Integration**: External game API support

## 📝 Version Notes

### Version 1.4.0
This is a **stable release** with comprehensive functionality including leaderboard management, rally system, and performance optimizations:

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

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/ArcPythonBot/issues)
- **Discord Server**: Join our community server for support
- **Documentation**: Check our [Wiki](https://github.com/yourusername/ArcPythonBot/wiki) for detailed guides

---

**⭐ Star this repository if you find it helpful!**

*Made with ❤️ for the Avatar Realms Collide community* 