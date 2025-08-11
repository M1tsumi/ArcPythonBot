#!/usr/bin/env python3
"""
Translation Folder System
=========================

This script breaks down the large translations.json file into smaller, organized files
by folder/module to reduce memory usage and improve maintainability.

Usage:
    python translation_folder_system.py

Features:
- Analyzes existing translations.json structure
- Creates organized folder structure for translations
- Splits translations by cog/module
- Generates index files for easy loading
- Provides memory usage optimization
- Creates backup and restore functionality
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class TranslationFolderSystem:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.translations_path = self.base_path / "translations.json"
        self.translations_folder = self.base_path / "translations"
        self.backup_path = self.base_path / "translations_backup"
        
        # Define module/cog categories and their translation keys
        self.module_categories = {
            "core": {
                "description": "Core bot functionality and basic commands",
                "keys": [
                    "language_set_success", "language_set_error", "invalid_language",
                    "current_language", "available_languages", "pong_title", 
                    "checking_bot_status", "bot_online_responding", "api_latency",
                    "bot_status", "online_ready", "servers", "servers_plural",
                    "users", "users_plural", "commands", "slash_commands",
                    "help_title", "help_description", "bot_information_title",
                    "bot_information_desc", "no_permission", "error_occurred"
                ]
            },
            "profile_images": {
                "description": "Profile image submission and approval system",
                "keys": [
                    "profile_image_submitted", "profile_image_submitted_desc",
                    "what_happens_next", "what_happens_next_desc", "note", "note_desc",
                    "invalid_file_type", "file_too_large", "download_failed",
                    "save_failed", "processing_error", "approval_request_title",
                    "approval_request_desc", "profile_approved_title", "profile_approved_desc",
                    "next_steps", "next_steps_desc", "profile_rejected_title",
                    "profile_rejected_desc", "what_to_do", "what_to_do_desc",
                    "pending_approvals_title", "no_pending_approvals", "pending_approvals_desc",
                    "profile_image_info_title", "profile_image_found", "file_missing",
                    "no_profile_image", "pending_approval_status", "profile_image_ok",
                    "profile_image_fixed", "what_was_fixed", "no_pending_to_clear",
                    "no_pending_desc", "pending_cleared", "pending_cleared_desc",
                    "approval_expired_title", "approval_expired_desc", "what_happened",
                    "what_happened_desc", "already_processed", "error_approving",
                    "error_rejecting", "error_getting_info", "error_fixing",
                    "error_clearing", "error_notifying", "error_timeout",
                    "error_handling_timeout", "file_exists", "file_missing_status",
                    "file_size_mb", "file_size_bytes"
                ]
            },
            "profiles": {
                "description": "User profile and statistics system",
                "keys": [
                    "global_profile_title", "global_profile_desc", "global_statistics",
                    "performance", "global_ranking", "global_achievements",
                    "account_info", "server_profile_title", "server_profile_desc",
                    "profile_private", "profile_error", "profile_display_error"
                ]
            },
            "avatar_play": {
                "description": "Avatar Play system and game mechanics",
                "keys": [
                    # Add avatar play specific keys here
                ]
            },
            "duel_system": {
                "description": "PvP duel system and combat mechanics",
                "keys": [
                    # Add duel system specific keys here
                ]
            },
            "rally_system": {
                "description": "Rally system and alliance mechanics",
                "keys": [
                    # Add rally system specific keys here
                ]
            },
            "events": {
                "description": "Event system and special game modes",
                "keys": [
                    # Add events specific keys here
                ]
            },
            "heroes": {
                "description": "Hero management and information system",
                "keys": [
                    # Add hero system specific keys here
                ]
            },
            "skills": {
                "description": "Skill system and talent trees",
                "keys": [
                    # Add skill system specific keys here
                ]
            },
            "troops": {
                "description": "Troop management and calculator",
                "keys": [
                    # Add troop system specific keys here
                ]
            },
            "leaderboards": {
                "description": "Leaderboard and ranking system",
                "keys": [
                    # Add leaderboard specific keys here
                ]
            },
            "minigame": {
                "description": "Minigame and daily reward system",
                "keys": [
                    # Add minigame specific keys here
                ]
            },
            "timer": {
                "description": "Timer and reminder system",
                "keys": [
                    # Add timer system specific keys here
                ]
            },
            "vote": {
                "description": "Voting and reward system",
                "keys": [
                    # Add vote system specific keys here
                ]
            },
            "statistics": {
                "description": "Bot statistics and analytics",
                "keys": [
                    "server_statistics", "comprehensive_overview", "overview",
                    "total_servers", "total_members", "average_members",
                    "distribution", "large_servers", "medium_servers", "small_servers",
                    "recent_activity", "joined_last_30_days", "active_servers",
                    "bot_commands", "top_10_servers", "performance", "bot_latency",
                    "uptime", "memory_usage", "server_statistics_generated",
                    "error_generating_statistics", "commands_refreshed",
                    "successfully_synced", "available_commands", "commands_now_available",
                    "refresh_failed", "error_refreshing_commands", "failed_refresh_commands",
                    "no_servers_found"
                ]
            },
            "command_descriptions": {
                "description": "Command descriptions and help text",
                "keys": [
                    "talent_trees_desc", "skill_priorities_desc", "hero_info_desc",
                    "hero_rankup_desc", "townhall_desc", "leaderboard_desc",
                    "map_desc", "troops_desc", "troopcalc_desc", "tierlist_desc",
                    "events_desc", "avatar_day_festival_desc", "festival_tasks_desc",
                    "festival_shop_desc", "festival_guide_desc", "festival_rewards_desc",
                    "balance_and_order_desc", "balance_tasks_desc", "balance_guide_desc",
                    "borte_scheme_desc", "borte_mechanics_desc", "borte_rewards_desc",
                    "borte_guide_desc", "play_desc", "daily_desc", "minigame_desc",
                    "trivia_desc", "trivia_leaderboard_desc", "inventory_desc",
                    "hero_desc", "skills_desc", "duel_desc", "setup_desc",
                    "rally_desc", "rally_stats_desc", "rally_leaderboard_desc",
                    "leader_desc", "tgl_desc", "tgl_calc_desc", "glorious_victory_desc",
                    "gv_calc_desc", "timer_desc", "timers_desc", "cancel_timer_desc",
                    "cancel_all_timers_desc", "vote_desc", "vote_status_desc",
                    "ping_desc", "info_desc", "links_desc", "addtoserver_desc",
                    "refresh_desc", "statistics_desc"
                ]
            },
            "festivals": {
                "description": "Festival and special event translations",
                "keys": [
                    # Add festival specific keys here
                ]
            },
            "ui": {
                "description": "User interface and interaction elements",
                "keys": [
                    # Add UI specific keys here
                ]
            }
        }

    def load_translations(self) -> Dict[str, Any]:
        """Load the main translations.json file."""
        try:
            with open(self.translations_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {self.translations_path} not found!")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {self.translations_path}: {e}")
            return {}

    def create_backup(self) -> bool:
        """Create a backup of the current translations.json file."""
        try:
            import time
            if not self.backup_path.exists():
                self.backup_path.mkdir(parents=True)
            
            backup_file = self.backup_path / f"translations_backup_{int(time.time())}.json"
            shutil.copy2(self.translations_path, backup_file)
            print(f"✅ Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False

    def create_folder_structure(self) -> bool:
        """Create the organized folder structure for translations."""
        try:
            # Create main translations folder
            if not self.translations_folder.exists():
                self.translations_folder.mkdir(parents=True)
            
            # Create subfolders for each module
            for module_name in self.module_categories.keys():
                module_folder = self.translations_folder / module_name
                if not module_folder.exists():
                    module_folder.mkdir(parents=True)
            
            # Create uncategorized folder for any keys that don't fit
            uncategorized_folder = self.translations_folder / "uncategorized"
            if not uncategorized_folder.exists():
                uncategorized_folder.mkdir(parents=True)
            
            # Create index folder
            index_folder = self.translations_folder / "index"
            if not index_folder.exists():
                index_folder.mkdir(parents=True)
            
            print("✅ Folder structure created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating folder structure: {e}")
            return False

    def analyze_translations(self, translations: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze translations and categorize keys by module."""
        categorized_keys = {module: [] for module in self.module_categories.keys()}
        uncategorized_keys = []
        
        # Get all translation keys from the first language (assuming EN exists)
        if "EN" in translations:
            all_keys = list(translations["EN"].keys())
            
            for key in all_keys:
                categorized = False
                
                # Check if key belongs to any predefined category
                for module_name, category_info in self.module_categories.items():
                    if key in category_info.get("keys", []):
                        categorized_keys[module_name].append(key)
                        categorized = True
                        break
                
                # If not in predefined categories, try to categorize by key pattern
                if not categorized:
                    module_name = self.categorize_key_by_pattern(key)
                    if module_name:
                        categorized_keys[module_name].append(key)
                        categorized = True
                
                if not categorized:
                    uncategorized_keys.append(key)
        
        # Add uncategorized keys to a special category
        if uncategorized_keys:
            categorized_keys["uncategorized"] = uncategorized_keys
        
        return categorized_keys

    def categorize_key_by_pattern(self, key: str) -> Optional[str]:
        """Categorize a key based on its pattern/name."""
        key_lower = key.lower()
        
        # Pattern-based categorization
        patterns = {
            "avatar_play": ["avatar", "play", "game"],
            "duel_system": ["duel", "combat", "battle", "fight"],
            "rally_system": ["rally", "alliance", "group"],
            "events": ["event", "festival", "special"],
            "heroes": ["hero", "character"],
            "skills": ["skill", "talent", "ability"],
            "troops": ["troop", "army", "unit"],
            "leaderboards": ["leaderboard", "ranking", "rank"],
            "minigame": ["minigame", "daily", "reward"],
            "timer": ["timer", "reminder", "schedule"],
            "vote": ["vote", "voting"],
            "festivals": ["festival", "celebration"],
            "ui": ["button", "modal", "view", "embed"]
        }
        
        for module_name, pattern_list in patterns.items():
            if any(pattern in key_lower for pattern in pattern_list):
                return module_name
        
        return None

    def split_translations(self, translations: Dict[str, Any], categorized_keys: Dict[str, List[str]]) -> bool:
        """Split translations into separate files by module."""
        try:
            for module_name, keys in categorized_keys.items():
                if not keys:
                    continue
                
                module_translations = {}
                
                # Create module translations for each language
                for language in translations.keys():
                    module_translations[language] = {}
                    for key in keys:
                        if key in translations[language]:
                            module_translations[language][key] = translations[language][key]
                
                # Save module translations
                module_file = self.translations_folder / module_name / "translations.json"
                with open(module_file, 'w', encoding='utf-8') as f:
                    json.dump(module_translations, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Created {module_name}: {len(keys)} keys")
            
            return True
        except Exception as e:
            print(f"❌ Error splitting translations: {e}")
            return False

    def create_index_files(self, categorized_keys: Dict[str, List[str]]) -> bool:
        """Create index files for easy loading and management."""
        try:
            # Create main index
            from datetime import datetime
            main_index = {
                "modules": {},
                "total_keys": sum(len(keys) for keys in categorized_keys.values()),
                "created_at": str(datetime.now()),
                "version": "1.0"
            }
            
            for module_name, keys in categorized_keys.items():
                if keys:
                    main_index["modules"][module_name] = {
                        "key_count": len(keys),
                        "file_path": f"{module_name}/translations.json",
                        "description": self.module_categories.get(module_name, {}).get("description", "")
                    }
            
            # Save main index
            index_file = self.translations_folder / "index" / "main_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(main_index, f, indent=2, ensure_ascii=False)
            
            # Create key mapping index
            key_mapping = {}
            for module_name, keys in categorized_keys.items():
                for key in keys:
                    key_mapping[key] = module_name
            
            mapping_file = self.translations_folder / "index" / "key_mapping.json"
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(key_mapping, f, indent=2, ensure_ascii=False)
            
            print("✅ Index files created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating index files: {e}")
            return False

    def create_loader_utility(self) -> bool:
        """Create a utility script for loading translations efficiently."""
        loader_script = '''#!/usr/bin/env python3
"""
Translation Loader Utility
==========================

This utility provides efficient loading of translations from the folder structure.
It supports lazy loading and memory optimization.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache

class TranslationLoader:
    def __init__(self, translations_path: str = "data/translations"):
        self.translations_path = Path(translations_path)
        self.index_path = self.translations_path / "index" / "main_index.json"
        self.mapping_path = self.translations_path / "index" / "key_mapping.json"
        self._loaded_modules = {}
        self._key_mapping = None
        
    def load_index(self) -> Dict[str, Any]:
        """Load the main index file."""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Index file not found at {self.index_path}")
            return {}
    
    def load_key_mapping(self) -> Dict[str, str]:
        """Load the key mapping file."""
        if self._key_mapping is None:
            try:
                with open(self.mapping_path, 'r', encoding='utf-8') as f:
                    self._key_mapping = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Key mapping file not found at {self.mapping_path}")
                self._key_mapping = {}
        return self._key_mapping
    
    def load_module(self, module_name: str) -> Dict[str, Any]:
        """Load a specific module's translations."""
        if module_name in self._loaded_modules:
            return self._loaded_modules[module_name]
        
        module_file = self.translations_path / module_name / "translations.json"
        try:
            with open(module_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                self._loaded_modules[module_name] = translations
                return translations
        except FileNotFoundError:
            print(f"Warning: Module {module_name} not found")
            return {}
    
    def get_translation(self, key: str, language: str = "EN", module_name: Optional[str] = None) -> str:
        """Get a specific translation by key and language."""
        if module_name:
            module_translations = self.load_module(module_name)
        else:
            # Try to find the module from key mapping
            key_mapping = self.load_key_mapping()
            module_name = key_mapping.get(key)
            if not module_name:
                return f"Missing translation: {key}"
            module_translations = self.load_module(module_name)
        
        return module_translations.get(language, {}).get(key, f"Missing translation: {key}")
    
    def get_all_translations(self, language: str = "EN") -> Dict[str, str]:
        """Get all translations for a specific language (loads all modules)."""
        index = self.load_index()
        all_translations = {}
        
        for module_name in index.get("modules", {}).keys():
            module_translations = self.load_module(module_name)
            all_translations.update(module_translations.get(language, {}))
        
        return all_translations
    
    def unload_module(self, module_name: str) -> None:
        """Unload a module from memory."""
        if module_name in self._loaded_modules:
            del self._loaded_modules[module_name]
    
    def unload_all(self) -> None:
        """Unload all modules from memory."""
        self._loaded_modules.clear()
        self._key_mapping = None

# Usage example:
if __name__ == "__main__":
    loader = TranslationLoader()
    
    # Load a specific translation
    translation = loader.get_translation("help_title", "EN")
    print(f"Translation: {translation}")
    
    # Load all translations for a language
    all_translations = loader.get_all_translations("EN")
    print(f"Total translations loaded: {len(all_translations)}")
'''
        
        try:
            loader_file = self.translations_folder / "translation_loader.py"
            with open(loader_file, 'w', encoding='utf-8') as f:
                f.write(loader_script)
            
            print("✅ Translation loader utility created")
            return True
        except Exception as e:
            print(f"❌ Error creating loader utility: {e}")
            return False

    def create_migration_script(self) -> bool:
        """Create a migration script to update existing code."""
        migration_script = '''#!/usr/bin/env python3
"""
Translation Migration Script
============================

This script helps migrate existing code to use the new folder-based translation system.
"""

import json
import re
from pathlib import Path
from typing import List, Tuple

def find_translation_usage(file_path: Path) -> List[Tuple[str, int, str]]:
    """Find all translation key usage in a file."""
    usage = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\\n')
            
            # Common patterns for translation usage
            patterns = [
                r'get_text\\(["\']([^"\']+)["\']\\)',
                r'get_translation\\(["\']([^"\']+)["\']\\)',
                r'\\["\']([^"\']+)\\"\']\\s*:\\s*get_text\\(["\']([^"\']+)["\']\\)',
                r'translations\\.get\\(["\']([^"\']+)["\']\\)',
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        key = match.group(1)
                        usage.append((key, line_num, line.strip()))
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return usage

def generate_migration_report():
    """Generate a report of translation usage across the codebase."""
    cogs_dir = Path("cogs")
    utils_dir = Path("utils")
    
    all_usage = {}
    
    # Scan cogs directory
    if cogs_dir.exists():
        for file_path in cogs_dir.rglob("*.py"):
            usage = find_translation_usage(file_path)
            if usage:
                all_usage[str(file_path)] = usage
    
    # Scan utils directory
    if utils_dir.exists():
        for file_path in utils_dir.rglob("*.py"):
            usage = find_translation_usage(file_path)
            if usage:
                all_usage[str(file_path)] = usage
    
    # Generate report
    report = {
        "total_files": len(all_usage),
        "total_translation_usage": sum(len(usage) for usage in all_usage.values()),
        "files": all_usage
    }
    
    with open("translation_migration_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Migration report generated: translation_migration_report.json")
    print(f"Total files with translation usage: {len(all_usage)}")
    print(f"Total translation key usage: {sum(len(usage) for usage in all_usage.values())}")

if __name__ == "__main__":
    generate_migration_report()
'''
        
        try:
            migration_file = self.translations_folder / "migration_script.py"
            with open(migration_file, 'w', encoding='utf-8') as f:
                f.write(migration_script)
            
            print("✅ Migration script created")
            return True
        except Exception as e:
            print(f"❌ Error creating migration script: {e}")
            return False

    def create_readme(self) -> bool:
        """Create a README file explaining the new translation system."""
        readme_content = '''# Translation Folder System

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
'''
        
        try:
            readme_file = self.translations_folder / "README.md"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print("✅ README file created")
            return True
        except Exception as e:
            print(f"❌ Error creating README: {e}")
            return False

    def run_full_migration(self) -> bool:
        """Run the complete migration process."""
        print("🚀 Starting Translation Folder System Migration")
        print("=" * 50)
        
        # Step 1: Load current translations
        print("📖 Loading current translations...")
        translations = self.load_translations()
        if not translations:
            return False
        
        # Step 2: Create backup
        print("💾 Creating backup...")
        if not self.create_backup():
            return False
        
        # Step 3: Create folder structure
        print("📁 Creating folder structure...")
        if not self.create_folder_structure():
            return False
        
        # Step 4: Analyze and categorize translations
        print("🔍 Analyzing translations...")
        categorized_keys = self.analyze_translations(translations)
        
        # Step 5: Split translations
        print("✂️ Splitting translations...")
        if not self.split_translations(translations, categorized_keys):
            return False
        
        # Step 6: Create index files
        print("📋 Creating index files...")
        if not self.create_index_files(categorized_keys):
            return False
        
        # Step 7: Create utility files
        print("🛠️ Creating utility files...")
        if not self.create_loader_utility():
            return False
        
        if not self.create_migration_script():
            return False
        
        if not self.create_readme():
            return False
        
        # Step 8: Generate summary
        print("\n📊 Migration Summary:")
        print("=" * 30)
        total_keys = sum(len(keys) for keys in categorized_keys.values())
        print(f"Total translation keys: {total_keys}")
        
        for module_name, keys in categorized_keys.items():
            if keys:
                print(f"  {module_name}: {len(keys)} keys")
        
        print(f"\n✅ Migration completed successfully!")
        print(f"📁 New structure created in: {self.translations_folder}")
        print(f"💾 Backup saved in: {self.backup_path}")
        print(f"📖 Read the README at: {self.translations_folder}/README.md")
        
        return True

def main():
    """Main function to run the migration."""
    system = TranslationFolderSystem()
    success = system.run_full_migration()
    
    if success:
        print("\n🎉 Translation folder system is ready!")
        print("Next steps:")
        print("1. Review the generated structure")
        print("2. Test the translation loader")
        print("3. Update your code to use the new system")
        print("4. Remove the old translations.json when ready")
    else:
        print("\n❌ Migration failed. Check the errors above.")

if __name__ == "__main__":
    main()
