# Discord Bot Performance Optimization Guide

## Overview
This guide addresses the "Can't keep up" error and bot disconnection issues by optimizing performance bottlenecks.

## Root Causes Identified

### 1. **Heavy File I/O Operations**
- **Problem**: Synchronous file operations blocking the event loop
- **Impact**: Bot falls behind on Discord heartbeats
- **Solution**: Use async file operations with `aiofiles`

### 2. **Per-Guild Command Syncing**
- **Problem**: Syncing commands for every guild individually
- **Impact**: Slow startup and potential timeouts
- **Solution**: Only sync globally, remove per-guild sync

### 3. **Frequent Timer Checks**
- **Problem**: Timer system checking every 30 seconds
- **Impact**: Unnecessary CPU usage when no timers active
- **Solution**: Increase check interval to 60 seconds, add early exit

### 4. **Large Number of Cogs**
- **Problem**: 30+ cogs loading simultaneously
- **Impact**: Slow startup and potential blocking operations
- **Solution**: Optimize cog loading and use async operations

## Implemented Fixes

### 1. **Optimized Command Syncing**
```python
# Before: Per-guild sync (slow)
for guild in self.guilds:
    await self.tree.sync(guild=guild)

# After: Global sync only (fast)
await self.tree.sync()
```

### 2. **Improved Timer System**
```python
# Before: Check every 30 seconds
@tasks.loop(seconds=30)

# After: Check every 60 seconds with early exit
@tasks.loop(seconds=60)
async def check_timers(self):
    if not self.active_timers:
        return  # Early exit if no timers
```

### 3. **Async File Operations**
- Added `AsyncFileHandler` class
- Use `aiofiles` for non-blocking file I/O
- Replace synchronous file operations with async equivalents

## Additional Recommendations

### 1. **Reduce Cog Loading Time**
- Load essential cogs first
- Use lazy loading for non-critical features
- Consider splitting large cogs into smaller modules

### 2. **Optimize Database Operations**
- Use connection pooling
- Implement caching for frequently accessed data
- Batch database operations when possible

### 3. **Monitor Performance**
- Add performance logging
- Track command execution times
- Monitor memory usage

### 4. **Implement Rate Limiting**
- Add cooldowns to heavy commands
- Use Discord's built-in rate limiting
- Implement custom rate limiting for expensive operations

## Quick Fixes to Apply

### 1. **Install Dependencies**
```bash
pip install aiofiles>=23.0.0
```

### 2. **Update Bot Configuration**
- Reduce timer check frequency
- Remove per-guild command syncing
- Use async file operations

### 3. **Monitor Logs**
- Watch for "Can't keep up" messages
- Monitor command response times
- Check for memory leaks

## Performance Monitoring

### Key Metrics to Watch
1. **Latency**: Bot response time to Discord
2. **Memory Usage**: RAM consumption over time
3. **CPU Usage**: Processing overhead
4. **Command Response Times**: Individual command performance

### Logging Improvements
```python
# Add performance logging
import time

async def command_with_timing(self, interaction):
    start_time = time.time()
    # ... command logic ...
    execution_time = time.time() - start_time
    if execution_time > 1.0:  # Log slow commands
        self.logger.warning(f"Slow command: {execution_time:.2f}s")
```

## Emergency Fixes

If the bot is still experiencing issues:

1. **Reduce Cog Count**: Temporarily disable non-essential cogs
2. **Increase Timer Intervals**: Set timer checks to 120+ seconds
3. **Disable Heavy Features**: Turn off image processing, complex calculations
4. **Use Minimal Intents**: Only enable required Discord intents

## Long-term Solutions

1. **Database Migration**: Move from JSON files to proper database
2. **Caching Layer**: Implement Redis or in-memory caching
3. **Microservices**: Split bot into multiple smaller services
4. **Load Balancing**: Distribute load across multiple bot instances

## Testing Performance

### Before Optimization
- Monitor bot startup time
- Check command response times
- Watch for "Can't keep up" errors

### After Optimization
- Compare startup times
- Measure command performance
- Verify error reduction

## Conclusion

These optimizations should significantly improve your bot's performance and eliminate the "Can't keep up" errors. Focus on:

1. **Async Operations**: Replace blocking operations with async equivalents
2. **Efficient Startup**: Optimize cog loading and command syncing
3. **Resource Management**: Reduce unnecessary CPU and memory usage
4. **Monitoring**: Track performance metrics to identify bottlenecks

Remember to test changes in a development environment before deploying to production.
