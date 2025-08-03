"""
Timer System command module for Avatar Realms Collide Discord Bot.
Provides customizable timers for various game activities with completion notifications.
"""

import discord
from discord import app_commands
from discord.ext import commands, tasks
from typing import Dict, List, Optional
import asyncio
import time
from datetime import datetime, timedelta

class TimerSystem(commands.Cog):
    """Timer command cog for game activity tracking."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        
        # Timer storage: {user_id: {timer_id: timer_data}}
        self.active_timers = {}
        self.timer_counter = 0
        
        # Start the timer checker
        self.check_timers.start()
    
    def cog_unload(self):
        """Clean up when cog is unloaded."""
        self.check_timers.cancel()
    
    @tasks.loop(seconds=30)  # Check every 30 seconds
    async def check_timers(self):
        """Check for completed timers and notify users."""
        current_time = time.time()
        completed_timers = []
        
        for user_id, user_timers in self.active_timers.items():
            for timer_id, timer_data in user_timers.items():
                if current_time >= timer_data['end_time']:
                    completed_timers.append((user_id, timer_id, timer_data))
        
        # Process completed timers
        for user_id, timer_id, timer_data in completed_timers:
            await self._notify_timer_completion(user_id, timer_data)
            # Remove completed timer
            if user_id in self.active_timers:
                self.active_timers[user_id].pop(timer_id, None)
                if not self.active_timers[user_id]:
                    self.active_timers.pop(user_id, None)
    
    async def _notify_timer_completion(self, user_id: int, timer_data: Dict):
        """Notify user that their timer has completed."""
        try:
            user = self.bot.get_user(user_id)
            if user:
                embed = discord.Embed(
                    title="⏰ Timer Complete!",
                    description=f"Your **{timer_data['activity']}** timer has finished!",
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                
                embed.add_field(
                    name="Activity",
                    value=timer_data['activity'],
                    inline=True
                )
                
                embed.add_field(
                    name="Duration",
                    value=timer_data['duration_text'],
                    inline=True
                )
                
                embed.add_field(
                    name="Started At",
                    value=f"<t:{int(timer_data['start_time'])}:R>",
                    inline=False
                )
                
                embed.set_footer(text="Timer completed")
                
                await user.send(embed=embed)
                self.logger.info(f"Timer notification sent to user {user_id} for {timer_data['activity']}")
                
        except Exception as e:
            self.logger.error(f"Failed to send timer notification to user {user_id}: {e}")
    
    def _parse_duration(self, duration_str: str) -> Optional[int]:
        """Parse duration string to seconds."""
        try:
            duration_str = duration_str.lower().strip()
            total_seconds = 0
            
            # Parse hours
            if 'h' in duration_str or 'hour' in duration_str:
                if 'h' in duration_str:
                    hours = int(duration_str.split('h')[0])
                else:
                    hours = int(duration_str.split('hour')[0])
                total_seconds += hours * 3600
                duration_str = duration_str.replace(f'{hours}h', '').replace(f'{hours}hour', '').replace('s', '')
            
            # Parse minutes
            if 'm' in duration_str or 'min' in duration_str:
                if 'm' in duration_str and 'min' not in duration_str:
                    minutes = int(duration_str.split('m')[0])
                else:
                    minutes = int(duration_str.split('min')[0])
                total_seconds += minutes * 60
                duration_str = duration_str.replace(f'{minutes}m', '').replace(f'{minutes}min', '').replace('s', '')
            
            # Parse seconds
            if duration_str.strip() and duration_str.strip().isdigit():
                total_seconds += int(duration_str.strip())
            
            return total_seconds if total_seconds > 0 else None
            
        except (ValueError, IndexError):
            return None
    
    def _format_duration(self, seconds: int) -> str:
        """Format seconds to human readable duration."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    @app_commands.command(name="timer", description="Set a timer for game activities")
    @app_commands.describe(
        activity="The type of activity to time",
        duration="Duration (e.g., 2h 30m, 45m, 1h 15m 30s)",
        note="Optional note about the timer"
    )
    @app_commands.choices(activity=[
        app_commands.Choice(name="Recruiting", value="Recruiting"),
        app_commands.Choice(name="Gathering", value="Gathering"),
        app_commands.Choice(name="Build 1", value="Build 1"),
        app_commands.Choice(name="Build 2", value="Build 2"),
        app_commands.Choice(name="Research", value="Research"),
        app_commands.Choice(name="Event", value="Event")
    ])
    async def set_timer(
        self, 
        interaction: discord.Interaction, 
        activity: str, 
        duration: str, 
        note: Optional[str] = None
    ):
        """Set a timer for a game activity."""
        # Parse duration
        seconds = self._parse_duration(duration)
        if not seconds:
            embed = discord.Embed(
                title="❌ Invalid Duration",
                description="Please provide a valid duration format.\n\n**Examples:**\n• `2h 30m` - 2 hours 30 minutes\n• `45m` - 45 minutes\n• `1h 15m 30s` - 1 hour 15 minutes 30 seconds\n• `30s` - 30 seconds",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if duration is reasonable (max 24 hours)
        if seconds > 86400:  # 24 hours
            embed = discord.Embed(
                title="❌ Duration Too Long",
                description="Timers cannot exceed 24 hours. Please use a shorter duration.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Create timer
        user_id = interaction.user.id
        timer_id = self.timer_counter
        self.timer_counter += 1
        
        current_time = time.time()
        end_time = current_time + seconds
        
        timer_data = {
            'id': timer_id,
            'activity': activity,
            'duration': seconds,
            'duration_text': self._format_duration(seconds),
            'start_time': current_time,
            'end_time': end_time,
            'note': note,
            'user_id': user_id
        }
        
        # Store timer
        if user_id not in self.active_timers:
            self.active_timers[user_id] = {}
        self.active_timers[user_id][timer_id] = timer_data
        
        # Create confirmation embed
        embed = discord.Embed(
            title="⏰ Timer Set Successfully!",
            description=f"Your **{activity}** timer has been started.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Activity",
            value=activity,
            inline=True
        )
        
        embed.add_field(
            name="Duration",
            value=self._format_duration(seconds),
            inline=True
        )
        
        embed.add_field(
            name="Completion Time",
            value=f"<t:{int(end_time)}:R>",
            inline=False
        )
        
        if note:
            embed.add_field(
                name="Note",
                value=note,
                inline=False
            )
        
        embed.set_footer(text=f"Timer ID: {timer_id}")
        
        await interaction.response.send_message(embed=embed)
        self.logger.info(f"Timer set for user {user_id}: {activity} for {self._format_duration(seconds)}")
    
    @app_commands.command(name="timers", description="View your active timers")
    async def view_timers(self, interaction: discord.Interaction):
        """View all active timers for the user."""
        user_id = interaction.user.id
        user_timers = self.active_timers.get(user_id, {})
        
        if not user_timers:
            embed = discord.Embed(
                title="⏰ No Active Timers",
                description="You don't have any active timers.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="How to Set a Timer",
                value="Use `/timer <activity> <duration>` to set a new timer.\n\n**Available Activities:**\n• Recruiting\n• Gathering\n• Build 1\n• Build 2\n• Research\n• Event",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⏰ Your Active Timers",
            description=f"You have **{len(user_timers)}** active timer(s).",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for timer_id, timer_data in user_timers.items():
            time_remaining = timer_data['end_time'] - time.time()
            
            if time_remaining > 0:
                remaining_text = f"<t:{int(timer_data['end_time'])}:R>"
            else:
                remaining_text = "Completing soon..."
            
            field_value = f"**Duration:** {timer_data['duration_text']}\n"
            field_value += f"**Remaining:** {remaining_text}\n"
            
            if timer_data.get('note'):
                field_value += f"**Note:** {timer_data['note']}"
            
            embed.add_field(
                name=f"{timer_data['activity']} (ID: {timer_id})",
                value=field_value,
                inline=False
            )
        
        embed.set_footer(text="You'll be notified when timers complete")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="cancel_timer", description="Cancel a specific timer")
    @app_commands.describe(timer_id="The ID of the timer to cancel")
    async def cancel_timer(self, interaction: discord.Interaction, timer_id: int):
        """Cancel a specific timer."""
        user_id = interaction.user.id
        user_timers = self.active_timers.get(user_id, {})
        
        if timer_id not in user_timers:
            embed = discord.Embed(
                title="❌ Timer Not Found",
                description=f"Timer ID `{timer_id}` not found. Use `/timers` to view your active timers.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        timer_data = user_timers[timer_id]
        
        # Remove timer
        del user_timers[timer_id]
        if not user_timers:
            self.active_timers.pop(user_id, None)
        
        embed = discord.Embed(
            title="✅ Timer Cancelled",
            description=f"Your **{timer_data['activity']}** timer has been cancelled.",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Cancelled Timer",
            value=f"**Activity:** {timer_data['activity']}\n**Duration:** {timer_data['duration_text']}\n**Note:** {timer_data.get('note', 'None')}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.logger.info(f"Timer cancelled for user {user_id}: {timer_data['activity']}")
    
    @app_commands.command(name="cancel_all_timers", description="Cancel all your active timers")
    async def cancel_all_timers(self, interaction: discord.Interaction):
        """Cancel all active timers for the user."""
        user_id = interaction.user.id
        user_timers = self.active_timers.get(user_id, {})
        
        if not user_timers:
            embed = discord.Embed(
                title="❌ No Active Timers",
                description="You don't have any active timers to cancel.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        timer_count = len(user_timers)
        timer_list = []
        
        for timer_id, timer_data in user_timers.items():
            timer_list.append(f"• {timer_data['activity']} ({timer_data['duration_text']})")
        
        # Remove all timers
        self.active_timers.pop(user_id, None)
        
        embed = discord.Embed(
            title="✅ All Timers Cancelled",
            description=f"Cancelled **{timer_count}** timer(s).",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Cancelled Timers",
            value="\n".join(timer_list),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.logger.info(f"All timers cancelled for user {user_id}: {timer_count} timers")
    
    @app_commands.command(name="timer_help", description="Get help with timer commands")
    async def timer_help(self, interaction: discord.Interaction):
        """Show help information for timer commands."""
        embed = discord.Embed(
            title="⏰ Timer System Help",
            description="Set timers for your game activities and get notified when they complete!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📋 Available Activities",
            value="• **Recruiting** - Track recruitment times\n"
                  "• **Gathering** - Monitor resource gathering\n"
                  "• **Build 1** - Track first building queue\n"
                  "• **Build 2** - Track second building queue\n"
                  "• **Research** - Monitor research progress\n"
                  "• **Event** - Track event activities",
            inline=False
        )
        
        embed.add_field(
            name="⏱️ Duration Format",
            value="**Examples:**\n"
                  "• `2h 30m` - 2 hours 30 minutes\n"
                  "• `45m` - 45 minutes\n"
                  "• `1h 15m 30s` - 1 hour 15 minutes 30 seconds\n"
                  "• `30s` - 30 seconds\n"
                  "• `2h` - 2 hours",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Commands",
            value="• `/timer` - Set a new timer\n"
                  "• `/timers` - View your active timers\n"
                  "• `/cancel_timer` - Cancel a specific timer\n"
                  "• `/cancel_all_timers` - Cancel all timers\n"
                  "• `/timer_help` - Show this help message",
            inline=False
        )
        
        embed.add_field(
            name="💡 Tips",
            value="• Timers can be up to 24 hours long\n"
                  "• You'll receive a DM when timers complete\n"
                  "• Use notes to remember what each timer is for\n"
                  "• Timer IDs are shown when you set timers",
            inline=False
        )
        
        embed.set_footer(text="Timer notifications are sent via DM")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TimerSystem(bot)) 