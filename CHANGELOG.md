# Changelog
## [1.8.0] - 2025-08-09

### Added - 🚀 MAJOR RELEASE: Hero Progression & PvP Duel System
- **Hero Progression System**: Complete hero advancement framework
  - Rarity progression: Rare → Epic → Legendary with 6-star upgrade system
  - Element selection: Fire, Water, Earth, and Air heroes with unique stats
  - Resource management: Hero Shards and Scrolls for upgrades
  - Stat scaling: ATK, DEF, HP scale with rarity and star levels
  - Visual progression tracking with emoji indicators
- **Elemental Skill Trees**: Comprehensive skill progression system
  - 44 unique skills across 4 elements (11 skills per element)
  - Tiered progression: Basic → Advanced → Master → Ultimate skill tiers
  - Skill point economy: Earn through minigames, spend strategically
  - Prerequisites system: Logical skill unlocking requirements
  - Automatic bonus calculations: Stats bonuses from unlocked skills
- **PvP Duel System**: Strategic turn-based combat
  - Turn-based battle mechanics with speed-based turn order
  - Element advantage system: Fire > Air > Earth > Water > Fire
  - Combat mechanics: Critical hits, evasion, status effects
  - Interactive battle UI: Real-time action selection and animations
  - Challenge system: Send, accept, or decline duel invitations
- **ELO Rating System**: Competitive ranking framework
  - Rating tiers: Bronze → Silver → Gold → Platinum → Diamond → Master → Grandmaster
  - Dynamic rating adjustments based on opponent strength
  - Experience-based modifiers for new players
  - Tier promotion/demotion with visual indicators
- **Achievement System**: 18+ unique achievements with rewards
  - Progression achievements: First win, win streaks, rating milestones
  - Combat achievements: Perfect games, damage thresholds, element mastery
  - Special achievements: Underdog victories, consistency rewards
  - Automatic reward distribution: Scrolls, Shards, and Skill Points
- **Enhanced Global Profile System**: Cross-server progression tracking
  - Duel statistics: Wins, losses, draws, streaks, ratings
  - Performance metrics: Damage dealt/taken, favorite elements
  - Element statistics: Per-element win rates and performance
  - Recent duel history: Last 10 battles with detailed results
- **New Discord Commands**: 10 new slash commands across 3 new cogs
  - `/hero upgrade`: Upgrade hero rarity and stars
  - `/hero info`: View detailed hero information and stats
  - `/hero list`: Display personal hero collection
  - `/skills tree`: Browse interactive elemental skill trees
  - `/skills overview`: View personal skill progression
  - `/skills upgrade`: Unlock new skills with skill points
  - `/duel challenge`: Challenge players to PvP battles
  - `/duel stats`: View personal duel statistics
  - `/duel leaderboard`: Browse global duel rankings
  - `/duel cancel`: Cancel pending duel challenges

### Enhanced
- **Minigame Integration**: Enhanced reward system with duel bonuses
  - Increased Epic Scroll drop rate: 2% → 5% for trivia
  - Increased daily epic drop rate: 15% → 20%
  - Bonus Skill Point rewards for duelists with high trivia scores
  - Resource synchronization between minigame and global profiles
- **Global Profile Manager**: Extended with comprehensive new features
  - Hero management: Create, update, and track hero progression
  - Skill management: Unlock skills, calculate bonuses, track progression
  - Resource tracking: Scrolls, Shards, Skill Points across systems
  - Duel statistics: Complete battle performance tracking
  - Achievement processing: Automatic detection and reward distribution
- **Data Architecture**: New JSON configuration files
  - `player_definitions.json`: Hero rarity tiers and progression costs
  - `base_stats.json`: Element-specific base statistics
  - `skill_definitions.json`: Complete skill trees with 44 skills
  - `combat_data.json`: Combat mechanics and element advantages
  - `achievements.json`: Achievement definitions and rewards

### Technical
- **New Utility Modules**: Core game logic implementation
  - `player_manager.py`: Hero progression and stat calculations
  - `skill_manager.py`: Skill tree logic and bonus calculations
  - `duel_manager.py`: Combat simulation and battle management
  - `rating_system.py`: ELO calculations and tier management
- **New Cogs**: Modular Discord command systems
  - `player_system.py`: Hero management commands
  - `skill_system.py`: Skill tree interaction commands
  - `duel_system.py`: PvP battle commands with interactive UI
- **Enhanced Architecture**: Improved data management and integration
  - Asynchronous combat processing with real-time UI updates
  - Comprehensive error handling for edge cases
  - Resource validation and conflict prevention
  - Cross-system integration with existing minigame economy

### Changed
- **Version**: Updated from 1.7.2 to 1.8.0
- **Bot Description**: Enhanced to reflect new RPG progression features
- **Profile Schema**: Updated to version 1.1 with new data structures
- **Command Count**: Expanded from ~25 to 35+ commands total

### Admin Features
- **XP Management Commands**: Owner-only admin commands for player progression
  - `!addxp` / `/addxp`: Add whole levels to user progression (Owner only)
  - Automatic avatar token distribution (10 tokens per level)
  - Safety limits: Maximum 100 levels per command
  - Comprehensive error handling and validation
  - Detailed feedback with before/after statistics

## [1.7.2] - 2025-08-09

### Fixed
- **TGL System**: Fixed corrupted emoji encodings throughout the TGL command system
  - All emojis now display correctly (🏆, 📊, 🎯, ⛏️, 👥, ⚡, 🗡️, 💪, etc.)
  - Fixed bullet point character corruption in command outputs
  - Verified all 5 daily stages are properly included in overview and dropdown navigation

### Improved
- **TGL Overview**: Enhanced interactive dropdown functionality with proper emoji display
- **Code Quality**: Improved readability and formatting of TGL system code

## [1.7.1] - 2025-08-08

### Fixed
- `/tierlist` command reliability: correctly detects and displays the tier list image when present at
  `assets/images/leaderboards/hero-tierlist.webp` (WebP/PNG/JPG supported).

### Changed
- Leaderboard system (text-file mode) robustness and UX improvements:
  - Preserves the header line's date as the "checked" date; no automatic date changes.
  - Parses ranked lines starting with `1.` format; ignores non-ranked lines.
  - Normalizes dash characters for consistent display in embeds.
  - Paginated embeds (20 entries per page) with Prev/Next and Close controls; monospaced alignment for readability.
  - Clear, actionable error messages when files are missing or incorrectly formatted.

### Docs
- README updated: expanded Leaderboard System details and noted the `/tierlist` fix in 1.7.1.

### Notes
- Rank files' header dates reflect when rankings were checked; they are not updated automatically.
## [1.7.0] - 2025-08-07

### Added
- Tier List: New `/tierlist` command that displays the community hero tier list image (place at `assets/images/leaderboards/hero-tierlist.webp`).

### Changed
- Professionalized embeds across multiple cogs using centralized `EmbedGenerator.finalize_embed` (standard footer + timestamp).
- Anti-spam: Added sensible cooldowns to frequently used commands (prefix and slash).
- Event Calendar: Added WIP disclaimer to indicate event dates/times may be incorrect.
- Hero Info: Cleaned up formatting, added “All heroes require 10 shards to unlock” to overview, rarities, and search results.

### Security/Hardening
- Set `allowed_mentions=none` to prevent unsolicited pings.
- Global slash command error handling with professional ephemerals for cooldowns/unexpected errors.

### Technical
- New cog: `cogs/tier_list.py`.
- Registered new cog in `main.py`.
- Standardized event embeds and messages in `cogs/events.py`.
- Version bumped to 1.7.0.


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

- **1.8.0** (Current): Hero Progression & PvP Duel System - Major Release
- **1.7.2**: TGL System Fixes, Emoji Encoding Improvements
- **1.7.1**: Tierlist Command Reliability, Leaderboard System Enhancements
- **1.7.0**: Tier List System, Professional Embeds, Anti-spam Features
- **1.6.4**: Event System UI Improvements
- **1.6.3**: Troops Calculator, Server Command Fixes
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