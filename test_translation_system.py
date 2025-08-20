#!/usr/bin/env python3
"""
Test script for the Avatar Realms Collide Discord Bot Translation System
Run this script to test the translation functionality locally before deploying.
"""

import json
import sys
from pathlib import Path
import pytest


@pytest.fixture
def translations():
    """Load translations from JSON file for tests."""
    translations_file = Path("data/translations.json")
    with translations_file.open('r', encoding='utf-8') as f:
        return json.load(f)

def test_translation_file(translations):
    """Test if the translations.json file exists and is valid JSON."""
    print("🔍 Testing translation file...")
    assert isinstance(translations, dict)
    print("✅ Translation file loaded successfully")

def test_language_support(translations):
    """Test if all required languages are supported."""
    print("\n🌍 Testing language support...")
    
    required_languages = ["EN", "DE", "ES"]
    supported_languages = list(translations.keys())
    
    print(f"Supported languages: {supported_languages}")
    
    for lang in required_languages:
        if lang in supported_languages:
            print(f"✅ {lang} (English/Deutsch/Español) - Supported")
        else:
            print(f"❌ {lang} - Missing!")
            return False
    
    return True

def test_translation_keys(translations):
    """Test if all languages have the same translation keys."""
    print("\n🔑 Testing translation keys...")
    
    # Get all keys from English (should be the most complete)
    en_keys = set(translations["EN"].keys())
    de_keys = set(translations["DE"].keys())
    es_keys = set(translations["ES"].keys())
    
    print(f"English keys: {len(en_keys)}")
    print(f"German keys: {len(de_keys)}")
    print(f"Spanish keys: {len(es_keys)}")
    
    # Check for missing keys in each language
    missing_in_de = en_keys - de_keys
    missing_in_es = en_keys - es_keys
    
    if missing_in_de:
        print(f"❌ Missing keys in German: {missing_in_de}")
        return False
    
    if missing_in_es:
        print(f"❌ Missing keys in Spanish: {missing_in_es}")
        return False
    
    print("✅ All languages have the same translation keys")
    return True

def test_variable_formatting(translations):
    """Test if variable formatting works correctly."""
    print("\n🔧 Testing variable formatting...")
    
    # Test a few keys with variables
    test_keys = [
        "current_language",
        "pending_approvals_desc",
        "status_working"
    ]
    
    for key in test_keys:
        if key in translations["EN"]:
            text = translations["EN"][key]
            if "{" in text and "}" in text:
                print(f"✅ {key}: Contains variables")
            else:
                print(f"ℹ️ {key}: No variables")
    
    return True

def test_language_system_cog():
    """Test if the language system cog can be imported."""
    print("\n🤖 Testing language system cog...")
    
    try:
        # Add the project root to Python path
        sys.path.insert(0, str(Path.cwd()))
        
        # Try to import the language system
        from cogs.language_system import LanguageSystem
        print("✅ Language system cog imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Error importing language system cog: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing language system cog: {e}")
        return False

def test_sample_translations(translations):
    """Test a few sample translations to ensure they're properly formatted."""
    print("\n📝 Testing sample translations...")
    
    sample_keys = [
        "language_set_success",
        "invalid_language", 
        "profile_image_submitted",
        "help_title"
    ]
    
    for key in sample_keys:
        if key in translations["EN"]:
            en_text = translations["EN"][key]
            de_text = translations["DE"][key]
            es_text = translations["ES"][key]
            
            print(f"\nKey: {key}")
            print(f"EN: {en_text[:50]}...")
            print(f"DE: {de_text[:50]}...")
            print(f"ES: {es_text[:50]}...")
        else:
            print(f"❌ Key '{key}' not found in translations")
            return False
    
    return True

def test_file_structure():
    """Test if the required file structure exists."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "data/translations.json",
        "cogs/language_system.py"
    ]
    
    required_dirs = [
        "data/users/language_preferences"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - Exists")
        else:
            print(f"❌ {file_path} - Missing!")
            return False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path} - Exists")
        else:
            print(f"⚠️ {dir_path} - Missing (will be created automatically)")
    
    return True

def main():
    """Run all translation system tests."""
    print("🚀 Starting Translation System Tests")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Translation File", test_translation_file),
        ("Language Support", lambda: test_language_support(test_translation_file())),
        ("Translation Keys", lambda: test_translation_keys(test_translation_file())),
        ("Variable Formatting", lambda: test_variable_formatting(test_translation_file())),
        ("Sample Translations", lambda: test_sample_translations(test_translation_file())),
        ("Language System Cog", test_language_system_cog)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Translation system is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
