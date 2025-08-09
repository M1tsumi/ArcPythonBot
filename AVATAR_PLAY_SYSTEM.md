# 🎮 Avatar Play System v2.0

## Overview
The enhanced Avatar Play System is a comprehensive trivia-based game centered around Avatar: The Last Airbender and The Legend of Korra knowledge. Built with Discord Components v2, it features interactive gameplay, progression systems, and social features.

## 🌟 Key Features

### 🎯 Game Modes
- **⚡ Quick Play** (3 questions, 8s each) - Perfect for quick sessions
- **🎯 Standard** (5 questions, 10s each) - Balanced gameplay with 1.2x XP
- **🔥 Challenge** (8 questions, 12s each) - Extended rounds with 1.5x XP
- **💨 Blitz** (10 questions, 5s each) - Lightning fast with 2x XP
- **👑 Master** (15 questions, 15s each) - Ultimate test with 3x XP

### 📊 Difficulty Levels
- **🟢 Easy** - Simpler questions, 80% XP
- **🟡 Normal** - Standard difficulty
- **🟠 Hard** - Advanced questions, 150% XP  
- **🔴 Expert** - Master-level challenges, 200% XP

### 🏆 Progression System
- **Exponential Leveling** - 15% XP increase per level
- **Avatar Tokens** - Earned from level ups and achievements
- **Spirit Energy** - Visual representation of player status
- **Daily Bonuses** - 2x XP for first game each day
- **Streak Bonuses** - +10% XP per consecutive correct answer

### 🏅 Achievement System
- **🥉 Trivia Novice** - 10 correct answers
- **🥈 Trivia Apprentice** - 50 correct answers
- **🥇 Trivia Master** - 200 correct answers
- **👑 Trivia Grandmaster** - 500 correct answers
- **🔥 Streak Warrior** - 5-question streak
- **⚡ Streak Legend** - 10-question streak
- **💎 Perfect Player** - 3 perfect games
- **📅 Daily Champion** - 7-day daily streak

### 🎨 Enhanced UI Components
- **Interactive Buttons** - Quick mode selection with emojis
- **Dynamic Embeds** - Real-time question display with progress
- **Countdown Timers** - Visual time pressure for each question
- **Difficulty Selector** - Dropdown menu for preference setting
- **Live Stats** - Real-time performance tracking

## 📚 Question Categories
The system automatically categorizes questions:
- **Avatar & Airbending** - Aang, Air Nomads, airbending techniques
- **Water Tribe & Waterbending** - Katara, Sokka, Water Tribe culture
- **Earth Kingdom & Earthbending** - Toph, Ba Sing Se, earthbending
- **Fire Nation & Firebending** - Zuko, Azula, Fire Nation politics
- **Spirits & Avatar Lore** - Avatar State, past lives, spiritual world
- **General Knowledge** - Mixed Avatar universe content

## 🎮 How to Play

### Starting a Game
1. Use `/play` to open the main interface
2. Select your preferred game mode
3. Optionally adjust difficulty via dropdown
4. Answer questions using A/B/C/D buttons
5. Earn XP and compete for achievements!

### Scoring System
- **Base XP**: 75 points per correct answer
- **Mode Multipliers**: 1.0x to 3.0x based on difficulty
- **Difficulty Bonus**: Up to 2.0x for Expert level
- **Streak Bonus**: +10% per consecutive correct
- **Perfect Game**: +200 XP bonus for 100% accuracy
- **Daily Bonus**: 2x XP for first game of the day

### Unlocking Content
- **Level 5**: Unlock Challenge mode
- **Level 10**: Unlock Blitz mode  
- **Level 20 OR Trivia Master achievement**: Unlock Master mode

## 🏆 Leaderboards & Stats

### Player Statistics
- **Level & Total XP** - Overall progression
- **Games Played** - Total sessions completed
- **Accuracy Percentage** - Lifetime correct answer rate
- **Best Streak** - Longest consecutive correct answers
- **Perfect Games** - Games with 100% accuracy
- **Daily Streak** - Consecutive days played

### Leaderboards
- **Server Leaderboard** - Compete with guild members
- **Global Leaderboard** - Cross-server competition
- **Duplicate Merging** - Fixed issue where users appeared multiple times

## 🔧 Technical Features

### Discord Components v2
- **Enhanced Views** - Modern button and select interfaces
- **Async Interactions** - Smooth, responsive gameplay
- **Error Handling** - Graceful failure recovery
- **Timeout Management** - Automatic session cleanup

### Data Management
- **JSON Storage** - Efficient player data persistence
- **Schema Versioning** - Future-proof data structure
- **Backup & Recovery** - Safe data handling
- **Performance Optimization** - Fast load times

### Question Processing
- **Smart Parsing** - Multiple question format support
- **Difficulty Estimation** - Automatic categorization
- **Random Selection** - Fair question distribution
- **Validation System** - Question file verification

## 🛠️ Commands

### Primary Commands
- `/play` - Enter the Avatar Trivia Arena
- `/trivia leaderboard global` - View global rankings (now fixed!)
- `/trivia leaderboard server` - View server rankings
- `/trivia validate` - Check trivia file status

### Features in Commands
- **Dynamic Embeds** - Rich visual information
- **Interactive Buttons** - Smooth gameplay flow
- **Progress Tracking** - Real-time performance display
- **Achievement Notifications** - Instant unlock alerts

## 🎨 Visual Design

### Color Coding
- **Blue** - Main interface and questions
- **Green** - Correct answers and success
- **Red** - Incorrect answers and errors
- **Gold** - Perfect games and achievements
- **Orange** - Warnings and timeouts

### Emoji Usage
- **⚡🎯🔥💨👑** - Game mode indicators
- **🟢🟡🟠🔴** - Difficulty levels
- **🇦🇧🇨🇩** - Answer options
- **🏆📊🎮🧠** - Interface navigation

## 🔄 Integration with Existing System

### Compatibility
- **Separate Data Storage** - No conflicts with minigame_daily
- **Shared Trivia File** - Uses same question database
- **Independent Progression** - Own leveling system
- **Cross-Reference** - Links to existing leaderboards

### Migration Path
- **Optional Upgrade** - Can run alongside existing system
- **Data Preservation** - Original stats remain intact
- **Feature Enhancement** - Builds upon current functionality

## 🚀 Future Enhancements

### Planned Features
- **Custom Titles** - Unlock display names through achievements
- **Team Battles** - Collaborative trivia challenges
- **Season System** - Rotating leaderboards and rewards
- **Question Contributions** - Community-sourced content
- **Advanced Analytics** - Detailed performance insights

### Technical Improvements
- **Caching System** - Faster question loading
- **WebSocket Integration** - Real-time multiplayer
- **API Endpoints** - External integrations
- **Mobile Optimization** - Better mobile Discord experience

---

*The Avatar Play System represents the next evolution of Avatar trivia gaming on Discord, combining modern UI components with deep Avatar universe knowledge for an engaging and competitive experience.*
