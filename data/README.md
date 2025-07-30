# Data Directory

This directory contains all the game data used by the Avatar Realms Collide Discord Bot.

## Structure

### Characters
- `characters/character_list.json` - List of all available characters
- `characters/character_1.json` - Detailed data for Fire Mage (ID: 1)
- `characters/character_2.json` - Detailed data for Ice Warrior (ID: 2)
- ... (and so on for all 26 characters)

### Events
- `events/current_events.json` - Currently active and upcoming events
- `events/past_events.json` - Archive of past events

## Data Format

### Character Data Structure
Each character file contains:
- Basic information (name, description, category, element, etc.)
- Stats (health, mana, attack, defense, magic, speed)
- Abilities (passive abilities)
- Skills (4 skills with 5 levels each)
- Talents (talent tree with tiers and prerequisites)

### Event Data Structure
Each event contains:
- Basic information (name, description, type, difficulty)
- Dates (start_date, end_date, duration)
- Requirements (what players need to participate)
- Rewards (what players can earn)
- Mechanics (how the event works)
- Tips (strategies for success)

## Adding New Data

### Adding a New Character
1. Add the character to `characters/character_list.json`
2. Create a detailed file `characters/character_X.json` where X is the character ID
3. Follow the same structure as the existing character files

### Adding a New Event
1. Add the event to either `current_events.json` or `past_events.json`
2. Follow the same structure as the existing event files

## Notes
- All data is in JSON format for easy parsing
- Character IDs should be unique and sequential
- Event dates should be in YYYY-MM-DD format
- All text should be appropriate for Discord embeds (avoid extremely long descriptions)

## Disclaimer
This data is for demonstration purposes only and does not represent actual game content. The bot is not affiliated with any game developers. 