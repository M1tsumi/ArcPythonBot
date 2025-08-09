"""
Rally System module for Avatar Realms Collide Discord Bot.
Provides rally management, tracking, and point system functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class RallySystem(commands.Cog):
    """Rally system cog for managing rallies and tracking user participation."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.rally_channels = {}  # {guild_id: channel_id}
        self.active_rallies = {}  # {message_id: rally_data}
        self.user_stats_file = "data/system/rally_stats.json"
        self.load_rally_channels()
        self.load_user_stats()
        
        # Rally configuration
        self.rally_config = {
            1: {"max_players": 1, "points": 10, "name": "Level 1 Fortress"},
            2: {"max_players": 1, "points": 20, "name": "Level 2 Fortress"},
            3: {"max_players": 2, "points": 30, "name": "Level 3 Fortress"},
            4: {"max_players": 3, "points": 45, "name": "Level 4 Fortress"},
            5: {"max_players": 4, "points": 50, "name": "Level 5 Fortress"},
            6: {"max_players": 5, "points": 60, "name": "Level 6 Fortress"}
        }
        
        # Time limit options
        self.time_options = {
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "1hr": 60
        }
    
    def load_rally_channels(self):
        """Load rally channel configurations from file."""
        try:
            if os.path.exists("data/system/rally_channels.json"):
                with open("data/system/rally_channels.json", "r") as f:
                    self.rally_channels = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading rally channels: {e}")
            self.rally_channels = {}
    
    def save_rally_channels(self):
        """Save rally channel configurations to file."""
        try:
            os.makedirs("data/system", exist_ok=True)
            with open("data/system/rally_channels.json", "w") as f:
                json.dump(self.rally_channels, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving rally channels: {e}")
    
    def load_user_stats(self):
        """Load user statistics from file."""
        try:
            if os.path.exists(self.user_stats_file):
                with open(self.user_stats_file, "r") as f:
                    self.user_stats = json.load(f)
            else:
                self.user_stats = {}
        except Exception as e:
            self.logger.error(f"Error loading user stats: {e}")
            self.user_stats = {}
    
    def save_user_stats(self):
        """Save user statistics to file."""
        try:
            os.makedirs(os.path.dirname(self.user_stats_file), exist_ok=True)
            with open(self.user_stats_file, "w") as f:
                json.dump(self.user_stats, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving user stats: {e}")
    
    def update_user_stats(self, user_id: str, rally_level: int, action: str):
        """Update user statistics."""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "rallies_joined": 0,
                "rallies_created": 0,
                "points_earned": 0,
                "total_rallies": 0
            }
        
        if action == "joined":
            self.user_stats[user_id]["rallies_joined"] += 1
            self.user_stats[user_id]["points_earned"] += self.rally_config[rally_level]["points"]
        elif action == "created":
            self.user_stats[user_id]["rallies_created"] += 1
        
        self.user_stats[user_id]["total_rallies"] += 1
        self.save_user_stats()
    
    async def cleanup_expired_rally(self, message_id: str, rally_data: dict):
        """Clean up an expired rally and notify the creator."""
        try:
            # Get the message and delete it
            channel = self.bot.get_channel(int(rally_data["channel_id"]))
            if channel:
                try:
                    message = await channel.fetch_message(int(message_id))
                    await message.delete()
                except:
                    pass  # Message might already be deleted
            
            # Notify the creator
            creator = self.bot.get_user(rally_data["creator_id"])
            if creator:
                embed = discord.Embed(
                    title="⏰ Rally Expired",
                    description=f"Your rally for **{self.rally_config[rally_data['level']]['name']}** has expired with no participants.",
                    color=discord.Color.orange()
                )
                
                embed.add_field(
                    name="📊 Rally Details",
                    value=f"• **Level**: {rally_data['level']}\n• **Time Limit**: {rally_data['time_limit']}\n• **Players Joined**: {len(rally_data['joined_players'])}/{rally_data['max_players']}",
                    inline=False
                )
                
                embed.add_field(
                    name="💡 Tips",
                    value="• Try creating rallies during peak hours\n• Consider lower level fortresses for faster fills\n• Use shorter time limits for quick rallies",
                    inline=False
                )
                
                embed.set_footer(text="Don't give up! Try creating another rally.")
                
                try:
                    await creator.send(embed=embed)
                except:
                    pass  # User might have DMs disabled
            
            # Remove from active rallies
            if message_id in self.active_rallies:
                del self.active_rallies[message_id]
                
        except Exception as e:
            self.logger.error(f"Error cleaning up expired rally: {e}")
    
    @app_commands.command(name="setup", description="Setup rally system for this server")
    @app_commands.describe(channel="The channel where rallies will be posted")
    # @app_commands.default_permissions(administrator=True)  # Temporarily disabled for testing
    async def setup_rally(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Setup rally system for the server."""
        try:
            # Check if user has administrator permissions
            if not interaction.user.guild_permissions.administrator:
                embed = discord.Embed(
                    title="❌ Permission Denied",
                    description="You need administrator permissions to setup the rally system.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            guild_id = str(interaction.guild_id)
            self.rally_channels[guild_id] = channel.id
            self.save_rally_channels()
            
            embed = discord.Embed(
                title="✅ Rally System Setup Complete",
                description=f"Rally system has been successfully configured for this server!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="📢 Rally Channel",
                value=f"Rallies will be posted in {channel.mention}",
                inline=False
            )
            
            embed.add_field(
                name="🎮 Available Commands",
                value="• `/rally` - Create a new rally\n• `/rally_stats` - View your rally statistics\n• `/rally_leaderboard` - View rally leaderboard",
                inline=False
            )
            
            embed.add_field(
                name="🏰 Rally Levels",
                value="• **Level 1**: 1 player, 10 points\n• **Level 2**: 1 player, 20 points\n• **Level 3**: 2 players, 30 points\n• **Level 4**: 3 players, 45 points\n• **Level 5**: 4 players, 50 points\n• **Level 6**: 5 players, 60 points",
                inline=False
            )
            
            embed.add_field(
                name="⏰ Time Limits",
                value="• **5m** - 5 minutes\n• **15m** - 15 minutes\n• **30m** - 30 minutes\n• **1hr** - 1 hour",
                inline=False
            )
            
            embed.set_footer(text="Developed by Quefep • Avatar Realms Collide Bot")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Error setting up rally system: {e}")
            embed = discord.Embed(
                title="❌ Setup Failed",
                description="An error occurred while setting up the rally system. Please try again.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="rally", description="Create a new rally")
    @app_commands.describe(
        level="Shattered Skulls Fortress level (1-6)",
        time_limit="Time limit for the rally (5m, 15m, 30m, 1hr)"
    )
    async def create_rally(self, interaction: discord.Interaction, level: int, time_limit: str):
        """Create a new rally."""
        try:
            # Check if level is valid
            if level not in self.rally_config:
                embed = discord.Embed(
                    title="❌ Invalid Level",
                    description="Please select a level between 1 and 6.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Check if time limit is valid
            if time_limit not in self.time_options:
                embed = discord.Embed(
                    title="❌ Invalid Time Limit",
                    description="Please select a valid time limit: 5m, 15m, 30m, or 1hr.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Check if rally system is setup
            guild_id = str(interaction.guild_id)
            if guild_id not in self.rally_channels:
                embed = discord.Embed(
                    title="❌ Rally System Not Setup",
                    description="The rally system has not been configured for this server. An administrator needs to run `/setup` first.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Get rally channel
            rally_channel = self.bot.get_channel(self.rally_channels[guild_id])
            if not rally_channel:
                embed = discord.Embed(
                    title="❌ Channel Not Found",
                    description="The rally channel could not be found. Please contact an administrator.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Create rally embed
            rally_config = self.rally_config[level]
            embed = discord.Embed(
                title=f"🏰 {rally_config['name']} Rally",
                description=f"A new rally has been created for **{rally_config['name']}**!",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="👤 Created By",
                value=f"{interaction.user.mention}",
                inline=True
            )
            
            embed.add_field(
                name="🎯 Level",
                value=f"**Level {level}**",
                inline=True
            )
            
            embed.add_field(
                name="🏆 Points",
                value=f"**{rally_config['points']} points**",
                inline=True
            )
            
            embed.add_field(
                name="👥 Players",
                value=f"**0/{rally_config['max_players']}** joined",
                inline=True
            )
            
            embed.add_field(
                name="⏰ Time Limit",
                value=f"**{time_limit}**",
                inline=True
            )
            
            embed.add_field(
                name="📋 Status",
                value="🟡 **Recruiting**",
                inline=True
            )
            
            embed.set_footer(text="Click the green button to join, red button to delete (admin only)")
            
            # Create view with buttons
            view = RallyView(self, level, interaction.user.id)
            
            # Send rally message
            rally_message = await rally_channel.send(embed=embed, view=view)
            
            # Calculate expiration time
            minutes = self.time_options[time_limit]
            expiration_time = datetime.now() + timedelta(minutes=minutes)
            
            # Store rally data
            self.active_rallies[str(rally_message.id)] = {
                "level": level,
                "creator_id": interaction.user.id,
                "creator_name": interaction.user.display_name,
                "joined_players": [],
                "max_players": rally_config["max_players"],
                "points": rally_config["points"],
                "created_at": datetime.now().isoformat(),
                "expiration_time": expiration_time.isoformat(),
                "time_limit": time_limit,
                "message_id": str(rally_message.id),
                "channel_id": str(rally_channel.id)
            }
            
            # Update user stats
            self.update_user_stats(str(interaction.user.id), level, "created")
            
            # Confirm to creator
            confirm_embed = discord.Embed(
                title="✅ Rally Created",
                description=f"Your rally for **{rally_config['name']}** has been posted in {rally_channel.mention}!",
                color=discord.Color.green()
            )
            
            confirm_embed.add_field(
                name="📊 Rally Details",
                value=f"• **Level**: {level}\n• **Players**: 0/{rally_config['max_players']}\n• **Points**: {rally_config['points']}\n• **Time Limit**: {time_limit}",
                inline=False
            )
            
            confirm_embed.add_field(
                name="⏰ Expiration",
                value=f"This rally will expire at <t:{int(expiration_time.timestamp())}:R>",
                inline=False
            )
            
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            
            # Schedule cleanup task
            asyncio.create_task(self.schedule_rally_cleanup(str(rally_message.id), minutes * 60))
            
        except Exception as e:
            self.logger.error(f"Error creating rally: {e}")
            embed = discord.Embed(
                title="❌ Rally Creation Failed",
                description="An error occurred while creating the rally. Please try again.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def schedule_rally_cleanup(self, message_id: str, delay_seconds: int):
        """Schedule cleanup of a rally after the specified delay."""
        try:
            await asyncio.sleep(delay_seconds)
            
            if message_id in self.active_rallies:
                rally_data = self.active_rallies[message_id]
                
                # Check if rally is still active (not completed)
                if len(rally_data["joined_players"]) < rally_data["max_players"]:
                    await self.cleanup_expired_rally(message_id, rally_data)
                    
        except Exception as e:
            self.logger.error(f"Error in rally cleanup: {e}")
    
    @app_commands.command(name="rally_stats", description="View your rally statistics")
    async def rally_stats(self, interaction: discord.Interaction):
        """View user rally statistics."""
        try:
            user_id = str(interaction.user.id)
            
            if user_id not in self.user_stats:
                embed = discord.Embed(
                    title="📊 Rally Statistics",
                    description="You haven't participated in any rallies yet.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="🎯 Get Started",
                    value="Use `/rally` to create your first rally or join existing ones!",
                    inline=False
                )
            else:
                stats = self.user_stats[user_id]
                total_points = stats["points_earned"]
                
                embed = discord.Embed(
                    title="📊 Rally Statistics",
                    description=f"Statistics for {interaction.user.display_name}",
                    color=discord.Color.blue()
                )
                
                embed.add_field(
                    name="🏆 Total Points",
                    value=f"**{total_points:,}** points",
                    inline=True
                )
                
                embed.add_field(
                    name="🎮 Rallies Joined",
                    value=f"**{stats['rallies_joined']}** rallies",
                    inline=True
                )
                
                embed.add_field(
                    name="🚀 Rallies Created",
                    value=f"**{stats['rallies_created']}** rallies",
                    inline=True
                )
                
                embed.add_field(
                    name="📈 Total Participation",
                    value=f"**{stats['total_rallies']}** total rallies",
                    inline=True
                )
                
                # Calculate average points per rally
                if stats['rallies_joined'] > 0:
                    avg_points = total_points / stats['rallies_joined']
                    embed.add_field(
                        name="📊 Average Points",
                        value=f"**{avg_points:.1f}** points per rally",
                        inline=True
                    )
                
                embed.set_footer(text="Keep participating to earn more points!")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error displaying rally stats: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while loading your statistics.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="rally_leaderboard", description="View rally leaderboard")
    async def rally_leaderboard(self, interaction: discord.Interaction):
        """View rally leaderboard."""
        try:
            if not self.user_stats:
                embed = discord.Embed(
                    title="🏆 Rally Leaderboard",
                    description="No rally data available yet.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="🎯 Get Started",
                    value="Use `/rally` to create your first rally!",
                    inline=False
                )
                await interaction.response.send_message(embed=embed)
                return
            
            # Sort users by points
            sorted_users = sorted(
                self.user_stats.items(),
                key=lambda x: x[1]["points_earned"],
                reverse=True
            )[:10]  # Top 10
            
            embed = discord.Embed(
                title="🏆 Rally Leaderboard",
                description="Top players by points earned",
                color=discord.Color.gold()
            )
            
            for i, (user_id, stats) in enumerate(sorted_users, 1):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    username = user.display_name
                except:
                    username = f"User {user_id}"
                
                points = stats["points_earned"]
                rallies_joined = stats["rallies_joined"]
                
                embed.add_field(
                    name=f"{i}. {username}",
                    value=f"🏆 **{points:,}** points • 🎮 **{rallies_joined}** rallies",
                    inline=False
                )
            
            embed.set_footer(text="Updated in real-time • Developed by Quefep")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Error displaying leaderboard: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while loading the leaderboard.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

class RallyView(discord.ui.View):
    """View for rally interaction buttons."""
    
    def __init__(self, rally_system: RallySystem, level: int, creator_id: int):
        super().__init__(timeout=None)
        self.rally_system = rally_system
        self.level = level
        self.creator_id = creator_id
    
    @discord.ui.button(label="Join Rally", style=discord.ButtonStyle.green, emoji="✅")
    async def join_rally(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Join a rally."""
        try:
            message_id = str(interaction.message.id)
            
            if message_id not in self.rally_system.active_rallies:
                embed = discord.Embed(
                    title="❌ Rally Not Found",
                    description="This rally no longer exists.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            rally_data = self.rally_system.active_rallies[message_id]
            user_id = interaction.user.id
            
            # Check if user is the creator
            if user_id == rally_data["creator_id"]:
                embed = discord.Embed(
                    title="❌ Cannot Join Own Rally",
                    description="You cannot join your own rally. Wait for others to join!",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Check if user is already in the rally
            if user_id in rally_data["joined_players"]:
                embed = discord.Embed(
                    title="❌ Already Joined",
                    description="You have already joined this rally.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Check if rally is full
            if len(rally_data["joined_players"]) >= rally_data["max_players"]:
                embed = discord.Embed(
                    title="❌ Rally Full",
                    description="This rally is already full.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Add user to rally
            rally_data["joined_players"].append(user_id)
            
            # Update user stats
            self.rally_system.update_user_stats(str(user_id), self.level, "joined")
            
            # Update embed
            embed = interaction.message.embeds[0]
            
            # Update players field
            for field in embed.fields:
                if field.name == "👥 Players":
                    field.value = f"**{len(rally_data['joined_players'])}/{rally_data['max_players']}** joined"
                    break
            
            # Update status if full
            if len(rally_data["joined_players"]) >= rally_data["max_players"]:
                for field in embed.fields:
                    if field.name == "📋 Status":
                        field.value = "🟢 **Full - Ready to Start**"
                        break
                
                # Add completion message
                embed.add_field(
                    name="🎉 Rally Complete!",
                    value=f"All players have joined! The rally is ready to begin.",
                    inline=False
                )
            
            await interaction.message.edit(embed=embed)
            
            # Confirm to user
            confirm_embed = discord.Embed(
                title="✅ Joined Rally",
                description=f"You have successfully joined the **Level {self.level}** rally!",
                color=discord.Color.green()
            )
            
            confirm_embed.add_field(
                name="🏆 Points",
                value=f"You will earn **{rally_data['points']}** points when the rally completes.",
                inline=False
            )
            
            await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
            
            # If rally is full, delete it after a delay
            if len(rally_data["joined_players"]) >= rally_data["max_players"]:
                await asyncio.sleep(5)  # Give time for everyone to see the completion
                try:
                    await interaction.message.delete()
                    del self.rally_system.active_rallies[message_id]
                except:
                    pass  # Message might already be deleted
            
        except Exception as e:
            self.rally_system.logger.error(f"Error joining rally: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while joining the rally.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="Delete Rally", style=discord.ButtonStyle.red, emoji="🗑️")
    async def delete_rally(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Delete a rally (admin only)."""
        try:
            # Check if user is creator or has admin permissions
            if interaction.user.id != self.creator_id and not interaction.user.guild_permissions.administrator:
                embed = discord.Embed(
                    title="❌ Permission Denied",
                    description="Only the rally creator or administrators can delete this rally.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            message_id = str(interaction.message.id)
            
            if message_id in self.rally_system.active_rallies:
                del self.rally_system.active_rallies[message_id]
            
            # Delete the message
            await interaction.message.delete()
            
            # Confirm to user
            embed = discord.Embed(
                title="✅ Rally Deleted",
                description="The rally has been successfully deleted.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.rally_system.logger.error(f"Error deleting rally: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while deleting the rally.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(RallySystem(bot)) 