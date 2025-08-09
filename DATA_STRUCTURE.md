# Avatar Realms Collide Bot - Data Structure Documentation

## Overview
This document outlines the organized data structure for the Avatar Realms Collide Discord Bot, designed for both GitHub collaboration and development efficiency.

## Directory Structure

```
data/
├── game/                           # Game-related data
│   ├── characters/                 # Character information
│   │   ├── character_list.json     # Complete character list with basic info
│   │   ├── character_1.json        # Extended character data (metadata)
│   │   ├── skill_priorities/       # Character skill priority data
│   │   │   └── skill_priorities.json
│   │   ├── talent_data/            # Talent tree information
│   │   │   ├── talent_types.json   # Character talent types & categories
│   │   │   └── TalentType.txt      # Original talent type file (legacy)
│   │   └── talent_trees/           # Future: Individual talent tree data
│   ├── events/                     # Game events
│   │   ├── current_events.json
│   │   └── past_events.json
│   └── text_data/                  # Game text files
│       ├── alliance-ranks.txt
│       ├── leader-ranks.txt
│       ├── trivia-questions.txt
│       └── troops.txt
├── servers/                        # Server-specific data
│   ├── avatar_play/                # Avatar Play System data
│   │   └── servers/                # Per-server avatar play data
│   └── minigame/                   # Minigame system data
│       └── servers/                # Per-server minigame data
├── system/                         # Bot system data
│   ├── leaderboard_state.json      # Leaderboard system state
│   ├── rally_channels.json         # Rally system configuration
│   ├── rally_stats.json            # Rally system user stats
│   └── usage_stats.json            # Bot usage analytics
└── users/                          # User-specific data
    └── profiles/                   # User profile data

assets/
├── images/
│   ├── characters/                 # Character-related images
│   │   └── talents/                # Talent tree images
│   │       ├── aang-1.webp
│   │       ├── aang-2.webp
│   │       └── ... (all character talent images)
│   ├── leaderboards/               # Leaderboard images
│   └── map/                        # Map images
```

## Data Organization Principles

### 1. **Game Data** (`data/game/`)
- **Characters**: All character-related information organized by type
  - Basic character info in `character_list.json`
  - Skill priorities in dedicated JSON file
  - Talent types and categories in structured format
- **Events**: Current and historical game events
- **Text Data**: Game configuration files (troops, ranks, trivia)

### 2. **Server Data** (`data/servers/`)
- Organized by game system (avatar_play, minigame)
- Each system has per-server data storage
- Automatically excluded from git via .gitignore

### 3. **System Data** (`data/system/`)
- Bot operational data (leaderboards, rallies, stats)
- Configuration files for bot features
- Some files excluded from git for privacy

### 4. **User Data** (`data/users/`)
- User profiles and preferences
- Excluded from git for privacy

### 5. **Assets** (`assets/`)
- Images organized by category and character
- Talent tree images properly categorized

## Key Improvements

### ✅ **Developer Benefits**
- Clear separation of concerns
- Logical file organization
- Easy to find and modify specific data
- Structured JSON files instead of hardcoded data

### ✅ **GitHub Benefits**
- Proper .gitignore configuration
- Directory structure preserved with .gitkeep files
- Sensitive data excluded from version control
- Clean repository organization

### ✅ **Maintenance Benefits**
- Easy to add new characters/data
- Modular data structure
- Backward compatibility maintained
- Clear documentation

## File Formats

### Character Data
- **character_list.json**: Basic character information (name, element, rarity, etc.)
- **skill_priorities.json**: Character skill priority recommendations
- **talent_types.json**: Character talent tree types and categories

### System Data
- **JSON files**: Bot configuration and state
- **Text files**: Game data files (troops, ranks, trivia)

## Migration Notes

All existing functionality has been preserved during the reorganization:
- Data parser updated to use new file locations
- All cogs updated with new file paths
- Setup script validates new structure
- Backward compatibility maintained where possible

## Adding New Data

### New Character
1. Add to `character_list.json`
2. Add skill priorities to `skill_priorities.json`
3. Add talent type to `talent_types.json`
4. Add talent tree images to `assets/images/characters/talents/`

### New Game Data
- Add text files to `data/game/text_data/`
- Add structured data to appropriate JSON files
- Update data parser if needed

This structure provides a solid foundation for future development and collaboration.
