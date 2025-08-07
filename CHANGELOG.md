# Changelog

All notable changes to the Avatar Realms Collide Discord Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.4] - 2025-08-07

### Changed
- Updated version to 1.6.4
- Enhanced event system UI improvements
- Improved button styling and user experience

### Technical
- Updated events.py with improved button styling
- Enhanced user interface consistency
- Improved event system reliability

## [1.6.3] - 2025-08-06

### Fixed
- **Troops Calculator**: Fixed `/troops calculator` command parsing issues
  - Corrected troop data parsing from troops.txt file
  - Fixed unit names, costs, and stats extraction
  - Resolved column mapping issues for different tier structures
  - Improved handling of inconsistent file format (19 vs 20 columns)
  - Enhanced dynamic column indexing for accurate data extraction
- **Server Command**: Fixed `/server` command embed character limit
  - Reduced character limit threshold from 1000 to 800 characters
  - Implemented compact formatting for server information
  - Fixed embed splitting to prevent Discord's 1024-character limit
  - Improved server list display with concise formatting

### Changed
- Updated version to 1.6.3
- Enhanced troops data parsing with dynamic column mapping
- Improved server command embed formatting and reliability
- Updated data parser to handle inconsistent troops.txt structure

### Technical
- Enhanced `utils/data_parser.py` with improved troops parsing logic
- Updated `cogs/troops.py` to use corrected data parsing
- Modified `cogs/utility.py` server command for better embed handling
- Added dynamic column indexing for troops data extraction

## [1.6.2] - 2025-01-27

### Added
- **Troops System**: Complete troops information and management
  - `/troops` command for viewing detailed troop information
  - Interactive element selection (Water, Earth, Fire, Air)
  - Tier-based troop browsing (T1-T6)
  - Detailed troop stats, costs, and descriptions
  - Element-specific troop overviews and strategies
- **Enhanced UI**: Professional troop selection interface
  - Color-coded element buttons with emojis
  - Tier selection with visual styling
  - Comprehensive troop information displays
  - Interactive navigation system

### Changed
- Updated version to 1.6.2
- Enhanced bot with 16 cogs and 33 commands
- Improved data organization and management

### Technical
- Added new cog: `troops.py`
- Enhanced data parser with troop information
- Improved embed generation for troop displays
- Added comprehensive troop database integration

## [1.6.1] - 2025-08-03

### Added
- **Purification System**: New purification mechanics and tools
  - Enhanced purification tracking and management
  - Improved purification event handling
  - Better purification data organization

### Changed
- Updated version to 1.6.1
- Enhanced purification system functionality
- Improved data handling for purification events

### Technical
- Added purification data management
- Enhanced purification event processing
- Improved purification system integration

## [1.6.0] - 2025-08-03

### Added
- **Timer System**: Complete game activity timer with DM notifications
  - `/timer` command for setting custom timers
  - `/timers` command for viewing active timers
  - `/cancel_timer` command for cancelling specific timers
  - `/cancel_all_timers` command for cancelling all timers
  - `/timer_help` command for timer system help
- **Activity Tracking**: Support for 6 game activities
  - Recruiting, Gathering, Build 1, Build 2, Research, and Event
- **Custom Duration**: Flexible time input up to 24 hours
  - Support for hours, minutes, and seconds (e.g., 2h 30m, 45m, 1h 15m 30s)
- **Timer Management**: Comprehensive timer control system
  - View all active timers with remaining time
  - Cancel individual timers by ID
  - Cancel all timers at once
  - Optional notes for each timer
- **Real-time Updates**: Automatic timer checking every 30 seconds
- **DM Notifications**: Private messages when timers complete
- **Professional UI**: Clean embeds with timer information and management

### Changed
- Updated version to 1.6.0
- Enhanced bot with 15 cogs and 32 commands
- Improved user experience with timer notifications

### Technical
- Added new cog: `timer_system.py`
- Implemented background task for timer checking
- Added timer storage and management system
- Enhanced error handling for timer operations

## [1.5.0] - 2025-08-03

### Added
- **Glorious Victory System**: Complete event information and tools
  - `/glorious_victory` command with comprehensive event details
  - `/gv_calc` command for point calculation
  - Event stages, rewards, and strategy information
  - Point values for all fortress destruction activities
- **Hero Information System**: Comprehensive hero guide and unlock methods
  - `/hero_info` command with complete hero overview
  - `/hero_search` command for specific hero information
  - Rarity classification (Legendary, Epic, Rare, Future)
  - Detailed unlock sources and methods for all heroes
- **Enhanced Character Database**: Added unlock information to all characters
  - Unlock sources for each hero
  - Rarity and acquisition methods
  - Integration with existing character system
- **New Commands**: 4 new slash commands for event and hero information
- **Improved Data Management**: Better organization of hero and event data

### Changed
- Updated character information to include unlock sources
- Enhanced embed displays with unlock information
- Improved command organization and structure
- Updated version to 1.5.0

### Technical
- Added new cogs: `glorious_victory.py` and `hero_info.py`
- Updated main.py to load new cogs
- Enhanced data parser with unlock information
- Improved error handling and user experience

## [1.4.0] - 2025-08-03

### Added
- **Leaderboard System**: Complete leaderboard management
  - `/leaderboard` command for viewing top leaders and alliances
  - Admin controls for pausing, resuming, and clearing leaderboards
  - Event-aware system that pauses during non-event periods
  - Interactive buttons for easy navigation
- **Rally System**: Complete Shattered Skulls Fortress management
  - `/rally` command for creating and managing rallies
  - `/rally_stats` for personal rally statistics
  - `/rally_leaderboard` for global rally rankings
  - Time limits and auto-cleanup functionality
  - Creator restrictions (creators cannot join own rallies)
- **TGL System**: The Greatest Leader event tools
  - `/tgl` command for event information
  - `/tgl_calc` command for point calculation
  - Event stages, rewards, and strategy information
- **Performance Optimizations**: Enhanced speed and efficiency
  - Embed caching system (5-minute cache)
  - Optimized string processing and field generation
  - Enhanced logging with timing information
- **New Commands**: 6 new slash commands for various features
- **Professional UI**: Enhanced embeds and interactive components

### Changed
- Updated version to 1.4.0
- Improved error handling and user experience
- Enhanced command organization
- Better data persistence with JSON storage

### Technical
- Added new cogs: `leaderboards.py`, `rally_system.py`, `tgl_system.py`
- Enhanced embed generator with new features
- Improved data management and caching
- Better file structure and organization

## [1.3.0] - 2025-08-03

### Added
- **Interactive Talent Tree Browser**: Complete talent tree system
  - `/talent_trees` command for browsing by element
  - Character profiles with detailed information
  - Talent tree image support (WebP format)
  - Professional UI with clean embeds
- **Character Database**: Comprehensive character information
  - 25+ characters from the Avatar universe
  - Element-based categorization (Fire, Water, Earth, Air)
  - Rarity system (Common, Rare, Epic, Legendary, Mythic)
  - Detailed character descriptions and lore
- **Basic Commands**: Core bot functionality
  - `/ping` for bot status and latency
  - `/info` for bot information and contribution details
  - `/help` for command assistance

### Changed
- Updated version to 1.3.0
- Improved command structure and organization
- Enhanced error handling

### Technical
- Added new cogs: `talent_trees.py`, `game_info.py`
- Created data parser for character management
- Implemented embed generator for consistent UI
- Added image handling for talent tree images

## [1.2.0] - 2025-08-03

### Added
- **Basic Bot Structure**: Foundation for Discord bot
  - Discord.py 2.0+ integration
  - Slash command support
  - Modular cog structure
  - Environment configuration
- **Core Features**: Essential bot functionality
  - Command prefix system
  - Error handling
  - Logging system
  - Performance tracking

### Changed
- Updated version to 1.2.0
- Established project structure

### Technical
- Created main bot class
- Implemented cog loading system
- Added configuration management
- Set up logging and error handling

## [1.1.0] - 2025-08-03

### Added
- **Project Foundation**: Initial setup and structure
  - Basic file organization
  - Requirements.txt with dependencies
  - README.md with project information
  - License and contribution guidelines

### Changed
- Updated version to 1.1.0
- Established project documentation

### Technical
- Created project structure
- Added dependency management
- Implemented basic documentation

## [1.0.0] - 2025-08-03

### Added
- **Initial Release**: Avatar Realms Collide Discord Bot
  - Basic Discord bot functionality
  - Project structure and organization
  - Core dependencies and configuration

### Technical
- Created initial project structure
- Set up basic Discord bot framework
- Added essential dependencies

---

## Version History Summary

- **1.6.4** (Current): Event System UI Improvements
- **1.6.3** (Current): Troops Calculator, Server Command Fixes
- **1.6.2**: Troops System, Enhanced UI, Improved Data Management
- **1.6.1**: Purification System, Enhanced Event Handling, Improved Data Management
- **1.6.0**: Timer System, Game Activity Tracking, DM Notifications
- **1.5.0**: Glorious Victory System, Hero Information System, Enhanced Character Database
- **1.4.0**: Leaderboard System, Rally System, TGL System, Performance Optimizations
- **1.3.0**: Interactive Talent Tree Browser, Character Database, Basic Commands
- **1.2.0**: Basic Bot Structure, Core Features, Discord.py Integration
- **1.1.0**: Project Foundation, Documentation, Dependencies
- **1.0.0**: Initial Release, Basic Discord Bot Framework

## Future Plans

### Upcoming Features (Planned)
- **Skill Priorities**: Character skill progression system
- **Rarity Changes**: Dynamic rarity updates based on game balance
- **Level Requirements**: Character level progression and requirements
- **Resource Requirements**: Game resource costs and management
- **Advanced Analytics**: Detailed character and game statistics
- **Event Integration**: Real-time game event tracking
- **User Customization**: Personalized bot experience settings

### Technical Improvements
- **Real-time Data**: Live game data integration
- **API Integration**: External game API support
- **Mobile Optimization**: Better mobile Discord experience
- **Advanced Search**: Enhanced character search functionality
- **User Profiles**: Player profile management system

---

*For detailed information about each version, see the individual version notes in the README.md file.* 