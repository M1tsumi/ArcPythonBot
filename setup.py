#!/usr/bin/env python3
"""
Setup script for Avatar Realms Collide Discord Bot
"""

import os
import sys

def create_env_file():
    """Create .env file if it doesn't exist."""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Discord Bot Configuration\n")
            f.write("# Get your bot token from https://discord.com/developers/applications\n\n")
            f.write("DISCORD_TOKEN=your_discord_bot_token_here\n")
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your Discord bot token!")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import discord
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data_files():
    """Check if data files exist."""
    required_files = [
        'data/game/characters/character_list.json',
        'data/game/characters/character_1.json',
        'data/game/events/current_events.json',
        'data/game/events/past_events.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All data files are present")
        return True

def main():
    """Main setup function."""
    print("🚀 Avatar Realms Collide Discord Bot Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        print("\n⚠️  Some data files are missing. Please ensure all files are present.")
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. Edit .env file and add your Discord bot token")
    print("2. Run the bot: python main.py")
    print("3. Use !help to see all available commands")
    print("\n📚 For more information, see README.md")
    print("=" * 50)

if __name__ == "__main__":
    main() 