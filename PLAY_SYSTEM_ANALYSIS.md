# Avatar Play System Analysis & Global Leaderboard Recommendations

## Current Data Storage Analysis

### 🔍 **Player Data Storage**
**Location**: `data/servers/avatar_play/servers/{guild_id}/players/{user_id}.json`

**Current Player Data Structure**:
```json
{
  "user_id": 123456789,
  "guild_id": 987654321,
  "created_at": "2025-01-08T...",
  "level": 5,
  "xp": 750,
  "total_xp": 2250,
  "avatar_tokens": 15,
  "spirit_energy": 100,
  "stats": {
    "games_played": 12,
    "questions_answered": 60,
    "correct_answers": 48,
    "perfect_games": 3,
    "best_streak": 8,
    "current_streak": 0,
    "favorite_mode": "standard",
    "last_played": "2025-01-08T...",
    "daily_streak": 5,
    "last_daily": "2025-01-08"
  },
  "achievements": ["trivia_novice", "streak_warrior"],
  "unlocked_modes": ["quick", "standard", "challenge"],
  "custom_title": null,
  "preferred_difficulty": "normal",
  "game_history": []
}
```

### 🔍 **Current Leaderboard Implementation**
**Type**: Server-only leaderboard
**Data Source**: Reads all player files from server directory
**Sorting**: By `total_xp` (descending)
**Display**: Top 10 players per server

## ⚠️ **Current Limitations**

1. **No Global Leaderboard**: Only server-specific rankings
2. **Performance Issues**: Reads all files every time leaderboard is requested
3. **No Cross-Server Data**: Players can't compare across servers
4. **Data Duplication**: Same user data stored separately per server
5. **Scaling Problems**: File-based storage becomes slow with many players

## 🚀 **Recommended Solution: Hybrid Data Architecture**

### **New Data Structure**

```
data/
├── servers/
│   ├── avatar_play/
│   │   └── servers/
│   │       └── {guild_id}/
│   │           ├── server.json           # Server-specific settings
│   │           ├── leaderboard_cache.json # Server leaderboard cache
│   │           └── players/
│   │               └── {user_id}.json    # Server-specific player data
└── users/
    ├── global_profiles/
    │   └── {user_id}.json               # Global user profile
    └── leaderboards/
        ├── global_cache.json            # Global leaderboard cache
        └── server_rankings/
            └── {guild_id}.json          # Server-specific rankings
```

### **Data Architecture Design**

#### 1. **Global User Profile** (`data/users/global_profiles/{user_id}.json`)
```json
{
  "user_id": 123456789,
  "created_at": "2025-01-08T...",
  "global_stats": {
    "total_games_played": 45,
    "total_questions_answered": 225,
    "total_correct_answers": 180,
    "total_xp": 8500,
    "global_level": 12,
    "best_streak_ever": 15,
    "perfect_games_total": 8,
    "servers_played": ["987654321", "111222333"],
    "favorite_difficulty": "normal",
    "last_global_activity": "2025-01-08T..."
  },
  "achievements": {
    "global": ["trivia_master", "streak_legend"],
    "server_specific": {
      "987654321": ["server_champion"],
      "111222333": ["newcomer"]
    }
  },
  "preferences": {
    "display_name": "AvatarMaster",
    "custom_title": "Trivia Grandmaster",
    "privacy_settings": {
      "show_on_global_leaderboard": true,
      "show_server_stats": true
    }
  }
}
```

#### 2. **Server Player Data** (`data/servers/avatar_play/servers/{guild_id}/players/{user_id}.json`)
```json
{
  "user_id": 123456789,
  "guild_id": 987654321,
  "joined_server_at": "2025-01-08T...",
  "server_stats": {
    "games_played": 12,
    "questions_answered": 60,
    "correct_answers": 48,
    "server_xp": 2250,
    "server_level": 5,
    "best_streak": 8,
    "perfect_games": 3,
    "last_played": "2025-01-08T...",
    "daily_streak": 5,
    "last_daily": "2025-01-08"
  },
  "server_achievements": ["server_rookie", "daily_player"],
  "unlocked_modes": ["quick", "standard", "challenge"],
  "game_history": []
}
```

#### 3. **Leaderboard Cache Files**

**Global Cache** (`data/users/leaderboards/global_cache.json`):
```json
{
  "last_updated": "2025-01-08T...",
  "rankings": [
    {
      "user_id": 123456789,
      "global_level": 12,
      "total_xp": 8500,
      "total_correct": 180,
      "accuracy": 80.0,
      "servers_count": 2
    }
  ]
}
```

**Server Cache** (`data/users/leaderboards/server_rankings/{guild_id}.json`):
```json
{
  "guild_id": 987654321,
  "last_updated": "2025-01-08T...",
  "rankings": [
    {
      "user_id": 123456789,
      "server_level": 5,
      "server_xp": 2250,
      "correct_answers": 48,
      "accuracy": 80.0,
      "games_played": 12
    }
  ]
}
```

## 🛠️ **Implementation Strategy**

### **Phase 1: Data Migration & Dual Writing**
1. **Migrate Existing Data**: Convert current server-only files to new structure
2. **Dual Writing**: Write to both old and new structures during transition
3. **Maintain Compatibility**: Keep existing commands working

### **Phase 2: Enhanced Leaderboard System**
1. **Add Global Leaderboard Command**: `/leaderboard global`
2. **Enhance Server Leaderboard**: `/leaderboard server`
3. **Leaderboard Categories**: XP, Accuracy, Games Played, Streaks
4. **Caching System**: Auto-refresh every 10 minutes or on significant changes

### **Phase 3: Performance Optimization**
1. **Background Tasks**: Update caches automatically
2. **Smart Caching**: Only rebuild when needed
3. **Pagination**: Handle large leaderboards efficiently

## 📋 **Proposed Commands**

```
/leaderboard global [category] [page]
/leaderboard server [category] [page]
/profile [user] [scope: global|server]
/stats compare @user
```

## 🔧 **Key Benefits**

1. ✅ **Global Rankings**: Cross-server competition
2. ✅ **Performance**: Cached leaderboards for fast access
3. ✅ **Scalability**: Efficient data structure for growth
4. ✅ **User Experience**: Rich profile system with achievements
5. ✅ **Privacy**: User control over data visibility
6. ✅ **Analytics**: Better insights into player behavior

## 📊 **Leaderboard Categories**

### **Global Leaderboards**
- 🏆 **Total XP**: Overall experience points
- 🎯 **Accuracy**: Percentage of correct answers
- 🔥 **Best Streak**: Longest correct answer streak
- 🎮 **Games Played**: Total trivia sessions
- ⭐ **Perfect Games**: Games with 100% accuracy

### **Server Leaderboards**
- 📍 **Server XP**: Experience earned on this server
- 🏠 **Server Level**: Level achieved on this server
- 📅 **Daily Streak**: Consecutive days played
- 🆕 **Recent Activity**: Most active players this week

This architecture provides a solid foundation for both global and server-specific leaderboards while maintaining performance and scalability.
