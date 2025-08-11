#!/usr/bin/env python3
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
