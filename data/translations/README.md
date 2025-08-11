# Translation Folder System

## Overview

This system breaks down the large `translations.json` file into smaller, organized files by module/cog to reduce memory usage and improve maintainability.

## Structure

```
data/translations/
├── index/
│   ├── main_index.json          # Main index of all modules
│   └── key_mapping.json         # Mapping of keys to modules
├── core/
│   └── translations.json        # Core bot functionality
├── profile_images/
│   └── translations.json        # Profile image system
├── profiles/
│   └── translations.json        # User profiles
├── avatar_play/
│   └── translations.json        # Avatar Play system
├── duel_system/
│   └── translations.json        # PvP duel system
├── rally_system/
│   └── translations.json        # Rally system
├── events/
│   └── translations.json        # Event system
├── heroes/
│   └── translations.json        # Hero management
├── skills/
│   └── translations.json        # Skill system
├── troops/
│   └── translations.json        # Troop management
├── leaderboards/
│   └── translations.json        # Leaderboard system
├── minigame/
│   └── translations.json        # Minigame system
├── timer/
│   └── translations.json        # Timer system
├── vote/
│   └── translations.json        # Voting system
├── statistics/
│   └── translations.json        # Bot statistics
├── command_descriptions/
│   └── translations.json        # Command descriptions
├── festivals/
│   └── translations.json        # Festival events
├── ui/
│   └── translations.json        # UI elements
├── translation_loader.py        # Loading utility
└── migration_script.py          # Migration helper
```

## Benefits

1. **Memory Optimization**: Only load needed translation modules
2. **Better Organization**: Translations grouped by functionality
3. **Easier Maintenance**: Smaller files are easier to manage
4. **Faster Loading**: Load only required translations
5. **Better Collaboration**: Multiple developers can work on different modules

## Usage

### Basic Usage

```python
from data.translations.translation_loader import TranslationLoader

# Initialize loader
loader = TranslationLoader()

# Get a specific translation
translation = loader.get_translation("help_title", "EN")

# Load all translations for a language
all_translations = loader.get_all_translations("EN")

# Load specific module
module_translations = loader.load_module("core")
```

### Memory Management

```python
# Unload specific module to free memory
loader.unload_module("events")

# Unload all modules
loader.unload_all()
```

## Migration

1. Run the migration script to analyze current usage:
   ```bash
   python data/translations/migration_script.py
   ```

2. Review the generated report: `translation_migration_report.json`

3. Update your code to use the new loader system

## Adding New Translations

1. Identify the appropriate module for your translation key
2. Add the key to the module's `translations.json` file
3. Update the key mapping in `index/key_mapping.json`
4. Update the main index in `index/main_index.json`

## Backup and Restore

- Backups are automatically created in `data/translations_backup/`
- Original `translations.json` is preserved
- Use the backup files to restore if needed

## Performance Tips

1. Load only required modules
2. Unload modules when not needed
3. Use lazy loading for rarely used translations
4. Cache frequently used translations

## Troubleshooting

- Check the index files for missing modules
- Verify key mapping is correct
- Ensure file paths are correct
- Check file permissions
