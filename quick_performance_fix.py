#!/usr/bin/env python3
"""
Quick Performance Fix Script for Avatar Realms Collide Discord Bot

This script helps identify and fix common performance issues that cause
"Can't keep up" errors and bot disconnections.
"""

import os
import sys
import json
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import aiofiles
        print("✅ aiofiles is installed")
    except ImportError:
        print("❌ aiofiles is missing - installing...")
        os.system("pip install aiofiles>=23.0.0")
    
    try:
        import discord
        print("✅ discord.py is installed")
    except ImportError:
        print("❌ discord.py is missing")
        return False
    
    return True

def analyze_cog_performance():
    """Analyze cog loading performance."""
    print("\n📊 Analyzing cog performance...")
    
    cog_files = [
        'cogs.talent_trees',
        'cogs.leaderboards',
        'cogs.skill_priorities',
        'cogs.town_hall',
        'cogs.hero_rankup',
        'cogs.utility',
        'cogs.statistics',
        'cogs.events',
        'cogs.moderation',
        'cogs.game_info',
        'cogs.minigame_daily',
        'cogs.language_system',
        'cogs.avatar_play_system',
        'cogs.player_system',
        'cogs.skill_system',
        'cogs.duel_system',
        'cogs.player_tools',
        'cogs.rally_system',
        'cogs.tgl_system',
        'cogs.glorious_victory',
        'cogs.hero_info',
        'cogs.timer_system',
        'cogs.avatar_day_festival',
        'cogs.balance_and_order',
        'cogs.borte_scheme',
        'cogs.troops',
        'cogs.troop_calculator',
        'cogs.tier_list',
        'cogs.vote_system',
        'cogs.profile_images'
    ]
    
    print(f"📋 Total cogs: {len(cog_files)}")
    
    # Check for potentially heavy cogs
    heavy_cogs = [
        'cogs.avatar_play_system',  # Large file with many features
        'cogs.timer_system',        # Background tasks
        'cogs.rally_system',        # File I/O operations
        'cogs.leaderboards',        # Data processing
        'cogs.profile_images'       # Image processing
    ]
    
    print("⚠️  Potentially heavy cogs:")
    for cog in heavy_cogs:
        if cog in cog_files:
            print(f"   - {cog}")
    
    return len(cog_files), heavy_cogs

def check_file_operations():
    """Check for synchronous file operations."""
    print("\n📁 Checking file operations...")
    
    # Common file operation patterns to look for
    patterns = [
        'with open(',
        'json.load(',
        'json.dump(',
        'time.sleep(',
        'asyncio.sleep('
    ]
    
    blocking_operations = []
    
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in patterns:
                            if pattern in content:
                                blocking_operations.append((file_path, pattern))
                except Exception:
                    continue
    
    print(f"📊 Found {len(blocking_operations)} potential blocking operations")
    
    # Group by pattern
    pattern_counts = {}
    for file_path, pattern in blocking_operations:
        if pattern not in pattern_counts:
            pattern_counts[pattern] = []
        pattern_counts[pattern].append(file_path)
    
    for pattern, files in pattern_counts.items():
        print(f"   {pattern}: {len(files)} files")
        if len(files) <= 5:  # Show all files if 5 or fewer
            for file_path in files:
                print(f"     - {file_path}")
    
    return blocking_operations

def generate_optimization_report():
    """Generate a performance optimization report."""
    print("\n📋 Generating optimization report...")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "recommendations": []
    }
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        report["recommendations"].append("Install missing dependencies")
    
    # Analyze cogs
    cog_count, heavy_cogs = analyze_cog_performance()
    if cog_count > 25:
        report["recommendations"].append(f"Consider reducing cog count (currently {cog_count})")
    
    if heavy_cogs:
        report["recommendations"].append("Optimize heavy cogs: " + ", ".join(heavy_cogs))
    
    # Check file operations
    blocking_ops = check_file_operations()
    if len(blocking_ops) > 50:
        report["recommendations"].append("Replace synchronous file operations with async equivalents")
    
    # Save report
    with open('performance_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to performance_report.json")
    print(f"📊 Found {len(report['recommendations'])} optimization opportunities")
    
    return report

def apply_quick_fixes():
    """Apply quick performance fixes."""
    print("\n🔧 Applying quick fixes...")
    
    fixes_applied = []
    
    # Check if main.py has been optimized
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'for guild in self.guilds:' in content and 'await self.tree.sync(guild=guild)' in content:
                print("⚠️  main.py still has per-guild command syncing - needs optimization")
                fixes_applied.append("Remove per-guild command syncing from main.py")
            else:
                print("✅ main.py command syncing appears optimized")
    except Exception as e:
        print(f"❌ Could not check main.py: {e}")
    
    # Check timer system
    try:
        with open('cogs/timer_system.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if '@tasks.loop(seconds=30)' in content:
                print("⚠️  Timer system still checks every 30 seconds - needs optimization")
                fixes_applied.append("Increase timer check interval to 60 seconds")
            else:
                print("✅ Timer system appears optimized")
    except Exception as e:
        print(f"❌ Could not check timer_system.py: {e}")
    
    # Check for aiofiles dependency
    try:
        import aiofiles
        print("✅ aiofiles is available for async file operations")
    except ImportError:
        print("❌ aiofiles not installed - run: pip install aiofiles>=23.0.0")
        fixes_applied.append("Install aiofiles: pip install aiofiles>=23.0.0")
    
    return fixes_applied

def main():
    """Main function to run the performance analysis."""
    print("🚀 Avatar Realms Collide Bot Performance Analyzer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ main.py not found. Please run this script from the bot's root directory.")
        return
    
    # Run analysis
    report = generate_optimization_report()
    
    # Apply quick fixes
    fixes = apply_quick_fixes()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 50)
    
    if report["recommendations"]:
        print("🔧 RECOMMENDATIONS:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"   {i}. {rec}")
    else:
        print("✅ No major issues found!")
    
    if fixes:
        print("\n⚠️  QUICK FIXES NEEDED:")
        for i, fix in enumerate(fixes, 1):
            print(f"   {i}. {fix}")
    else:
        print("\n✅ No quick fixes needed!")
    
    print("\n📖 For detailed optimization guide, see: PERFORMANCE_OPTIMIZATION.md")
    print("🔗 For Discord bot performance tips: https://discordpy.readthedocs.io/en/stable/faq.html#performance")

if __name__ == "__main__":
    main()
