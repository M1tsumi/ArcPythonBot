#!/usr/bin/env python3
"""
Translation Verification Script
==============================

This script verifies that all translation keys have translations for all 3 languages (EN, DE, ES).
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

def load_translation_module(module_path: Path) -> Dict[str, Dict[str, str]]:
    """Load a translation module file."""
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {module_path}: {e}")
        return {}

def verify_module_translations(module_name: str, translations: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
    """Verify that all keys have translations for all 3 languages."""
    issues = {
        "missing_languages": [],
        "missing_keys": [],
        "empty_translations": []
    }
    
    if not translations:
        issues["missing_keys"].append("No translations found")
        return issues
    
    # Get all unique keys from all languages
    all_keys = set()
    for language, lang_translations in translations.items():
        all_keys.update(lang_translations.keys())
    
    # Check each language has all keys
    expected_languages = {"EN", "DE", "ES"}
    found_languages = set(translations.keys())
    
    # Check for missing languages
    missing_languages = expected_languages - found_languages
    if missing_languages:
        issues["missing_languages"].extend(list(missing_languages))
    
    # Check each language has all keys
    for language in found_languages:
        lang_keys = set(translations[language].keys())
        missing_keys = all_keys - lang_keys
        if missing_keys:
            issues["missing_keys"].extend([f"{language}: {key}" for key in missing_keys])
    
    # Check for empty translations
    for language, lang_translations in translations.items():
        for key, value in lang_translations.items():
            if not value or value.strip() == "":
                issues["empty_translations"].append(f"{language}: {key}")
    
    return issues

def main():
    """Main verification function."""
    print("🔍 Translation Verification Script")
    print("=" * 50)
    
    translations_path = Path("data/translations")
    if not translations_path.exists():
        print("❌ Translations folder not found!")
        return
    
    # Load main index
    index_path = translations_path / "index" / "main_index.json"
    if not index_path.exists():
        print("❌ Main index not found!")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    total_issues = 0
    modules_with_issues = []
    
    print(f"📋 Checking {len(index['modules'])} modules...")
    print()
    
    for module_name, module_info in index["modules"].items():
        print(f"🔍 Checking {module_name}...")
        
        # Load module translations
        module_file = translations_path / module_info["file_path"]
        translations = load_translation_module(module_file)
        
        # Verify translations
        issues = verify_module_translations(module_name, translations)
        
        # Report issues
        has_issues = False
        for issue_type, issue_list in issues.items():
            if issue_list:
                has_issues = True
                total_issues += len(issue_list)
                print(f"  ❌ {issue_type}: {len(issue_list)} issues")
                for issue in issue_list[:3]:  # Show first 3 issues
                    print(f"    - {issue}")
                if len(issue_list) > 3:
                    print(f"    ... and {len(issue_list) - 3} more")
        
        if has_issues:
            modules_with_issues.append(module_name)
        else:
            print(f"  ✅ All translations complete")
        
        print()
    
    # Summary
    print("📊 VERIFICATION SUMMARY")
    print("=" * 30)
    print(f"Total modules checked: {len(index['modules'])}")
    print(f"Modules with issues: {len(modules_with_issues)}")
    print(f"Total issues found: {total_issues}")
    
    if modules_with_issues:
        print(f"\n❌ Modules with issues:")
        for module in modules_with_issues:
            print(f"  - {module}")
    else:
        print("\n🎉 All translations are complete for all 3 languages!")
    
    # Check specific command descriptions
    print(f"\n🔍 Detailed Command Descriptions Check:")
    cmd_desc_file = translations_path / "command_descriptions" / "translations.json"
    cmd_translations = load_translation_module(cmd_desc_file)
    
    if cmd_translations:
        cmd_issues = verify_module_translations("command_descriptions", cmd_translations)
        if any(cmd_issues.values()):
            print("❌ Command descriptions have issues:")
            for issue_type, issue_list in cmd_issues.items():
                if issue_list:
                    print(f"  - {issue_type}: {len(issue_list)} issues")
        else:
            print("✅ All command descriptions are complete!")
    
    print(f"\n📋 Next steps:")
    if total_issues > 0:
        print("1. Fix missing translations in the modules listed above")
        print("2. Ensure all keys have translations for EN, DE, and ES")
        print("3. Remove any empty translation values")
        print("4. Re-run this verification script")
    else:
        print("1. All translations are complete!")
        print("2. Your bot is ready for multilingual support")
        print("3. Users can use /language to switch between EN, DE, ES")

if __name__ == "__main__":
    main()
