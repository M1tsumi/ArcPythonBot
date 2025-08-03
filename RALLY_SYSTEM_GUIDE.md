# Rally System Guide - Avatar Realms Collide Bot

## 🏰 Overview

The Rally System allows players to organize and participate in Shattered Skulls Fortress raids with automatic point tracking and user statistics. This system makes it easy to coordinate team activities and track community participation.

## 🚀 Getting Started

### 1. Setup (Administrators Only)

**Command**: `/setup #channel`

**Description**: Configure the rally system for your server by specifying which channel rallies will be posted in.

**Example**:
```
/setup #rally-channel
```

**Requirements**:
- Administrator permissions
- Valid text channel

**What it does**:
- Sets the designated rally channel
- Saves configuration for the server
- Provides setup confirmation with available commands

### 2. Creating Rallies

**Command**: `/rally level:1-6 time_limit:5m|15m|30m|1hr`

**Description**: Create a new rally for a specific Shattered Skulls Fortress level with a time limit.

**Example**:
```
/rally level:3 time_limit:15m
```

**Level Requirements**:
- **Level 1**: 1 player, 10 points
- **Level 2**: 1 player, 20 points  
- **Level 3**: 2 players, 30 points
- **Level 4**: 3 players, 45 points
- **Level 5**: 4 players, 50 points
- **Level 6**: 5 players, 60 points

**Time Limit Options**:
- **5m**: 5 minutes
- **15m**: 15 minutes
- **30m**: 30 minutes
- **1hr**: 1 hour

## 🎮 Rally Features

### Professional Rally Embeds

Each rally creates a beautiful embed with:
- **Fortress Level**: Clear level indication
- **Creator**: Who started the rally
- **Points**: Points earned for participation
- **Player Count**: Current/maximum players
- **Time Limit**: How long the rally will last
- **Status**: Recruiting, Full, or Ready to Start

### Interactive Buttons

**Green Button (✅ Join Rally)**:
- Join the rally if space is available
- Updates player count in real-time
- Awards points when rally completes
- Only works once per user per rally
- **Creator cannot join their own rally**

**Red Button (🗑️ Delete Rally)**:
- Available to rally creator and administrators
- Immediately removes the rally
- Cleans up rally data

### Auto-Completion System

When a rally reaches its maximum players:
1. Status updates to "Full - Ready to Start"
2. Completion message appears
3. Rally automatically disappears after 5 seconds
4. All participants receive their points

### Time Limit System

Each rally has a configurable time limit:
- **Automatic Expiration**: Rally disappears when time limit is reached
- **Creator Notification**: DM sent to creator if no one joins
- **Cleanup**: Automatic removal of expired rallies
- **Flexible Options**: 5m, 15m, 30m, or 1hr time limits

## 📊 Statistics & Tracking

### Personal Statistics

**Command**: `/rally_stats`

**Shows**:
- Total points earned
- Number of rallies joined
- Number of rallies created
- Total participation count
- Average points per rally

### Global Leaderboard

**Command**: `/rally_leaderboard`

**Shows**:
- Top 10 players by points
- Points earned per player
- Rallies joined per player
- Real-time updates

### Data Persistence

All data is automatically saved to JSON files:
- **User Statistics**: `data/rally_stats.json`
- **Channel Configuration**: `data/rally_channels.json`
- **Active Rallies**: In-memory with automatic cleanup

## 🏆 Point System

### Point Distribution

| Level | Players Required | Points Per Player |
|-------|------------------|-------------------|
| 1     | 1               | 10                |
| 2     | 1               | 20                |
| 3     | 2               | 30                |
| 4     | 3               | 45                |
| 5     | 4               | 50                |
| 6     | 5               | 60                |

### Point Tracking

- **Automatic**: Points awarded when rally completes
- **Immediate**: Statistics update in real-time
- **Persistent**: All data saved permanently
- **Transparent**: Clear point values shown on rally creation

## 🔧 Technical Details

### Rally Lifecycle

1. **Creation**: User creates rally with `/rally`
2. **Recruitment**: Players join via green button
3. **Monitoring**: Real-time updates to player count
4. **Completion**: Auto-deletion when full
5. **Rewards**: Points distributed to all participants

### Error Handling

- **Invalid Level**: Clear error message for levels outside 1-6
- **No Setup**: Guides users to contact administrators
- **Channel Issues**: Handles missing or inaccessible channels
- **Permission Errors**: Clear feedback for insufficient permissions
- **Duplicate Joins**: Prevents multiple joins from same user

### Performance Features

- **Efficient Storage**: JSON-based persistence
- **Memory Management**: Automatic cleanup of completed rallies
- **Real-time Updates**: Instant embed modifications
- **Error Recovery**: Graceful handling of edge cases

## 📋 Command Reference

### Administrator Commands

| Command | Description | Permissions |
|---------|-------------|-------------|
| `/setup` | Setup rally system | Administrator |

### User Commands

| Command | Description | Permissions |
|---------|-------------|-------------|
| `/rally` | Create a new rally | Any user |
| `/rally_stats` | View personal statistics | Any user |
| `/rally_leaderboard` | View global leaderboard | Any user |

### Button Interactions

| Button | Action | Permissions |
|--------|--------|-------------|
| ✅ Join Rally | Join the rally | Any user (once per rally) |
| 🗑️ Delete Rally | Delete the rally | Creator or Administrator |

## 🎯 Best Practices

### For Administrators

1. **Setup Early**: Configure the rally system before community use
2. **Choose Wisely**: Select a channel that's easily accessible
3. **Monitor Activity**: Check leaderboards for community engagement
4. **Provide Guidance**: Help users understand the system

### For Users

1. **Join Appropriately**: Only join rallies you can actually participate in
2. **Check Levels**: Ensure you can handle the fortress level
3. **Track Progress**: Use `/rally_stats` to monitor your participation
4. **Be Respectful**: Don't join rallies you can't complete

### For Rally Creators

1. **Clear Communication**: Specify any special requirements
2. **Monitor Progress**: Watch for rally completion
3. **Be Available**: Ensure you can participate when rally fills
4. **Create Regularly**: Help keep the community active

## 🔄 Integration

The Rally System integrates seamlessly with existing bot features:
- **Help System**: All rally commands included in `/help`
- **Info Command**: Rally system featured in bot information
- **Statistics**: Personal and global tracking
- **Professional UI**: Consistent with bot's design language

## 🚀 Future Enhancements

Potential future features:
- **Rally Scheduling**: Pre-scheduled rallies
- **Team Roles**: Automatic role assignment
- **Advanced Statistics**: Detailed analytics
- **Rally Categories**: Different types of rallies
- **Integration**: Connect with game APIs

---

**Developed by Quefep** • Version 1.3.0 • Avatar Realms Collide Bot 