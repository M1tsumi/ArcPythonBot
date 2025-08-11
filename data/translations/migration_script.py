#!/usr/bin/env python3
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
            lines = content.split('\n')
            
            # Common patterns for translation usage
            patterns = [
                r'get_text\(["']([^"']+)["']\)',
                r'get_translation\(["']([^"']+)["']\)',
                r'\["']([^"']+)\"']\s*:\s*get_text\(["']([^"']+)["']\)',
                r'translations\.get\(["']([^"']+)["']\)',
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
