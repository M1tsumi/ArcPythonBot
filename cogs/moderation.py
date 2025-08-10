"""
Moderation commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
import json
from pathlib import Path

class Moderation(commands.Cog):
    """Basic moderation commands for the bot."""
    
    # Keep in sync with the owner check used in other cogs
    AUTHORIZED_USER_ID: int = 1051142172130422884
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Kick a member from the server."""
        if member == ctx.author:
            embed = EmbedGenerator.create_error_embed("You cannot kick yourself.")
            await ctx.send(embed=embed)
            return
        
        if member.guild_permissions.administrator:
            embed = EmbedGenerator.create_error_embed("You cannot kick an administrator.")
            await ctx.send(embed=embed)
            return
        
        try:
            await member.kick(reason=reason)
            embed = EmbedGenerator.create_success_embed(
                f"Successfully kicked {member.mention} for: {reason}"
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to kick that member.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @kick_member.error
    async def kick_member_error(self, ctx, error):
        """Error handler for kick command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to kick members.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify a member to kick.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Ban a member from the server."""
        if member == ctx.author:
            embed = EmbedGenerator.create_error_embed("You cannot ban yourself.")
            await ctx.send(embed=embed)
            return
        
        if member.guild_permissions.administrator:
            embed = EmbedGenerator.create_error_embed("You cannot ban an administrator.")
            await ctx.send(embed=embed)
            return
        
        try:
            await member.ban(reason=reason)
            embed = EmbedGenerator.create_success_embed(
                f"Successfully banned {member.mention} for: {reason}"
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to ban that member.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @ban_member.error
    async def ban_member_error(self, ctx, error):
        """Error handler for ban command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to ban members.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify a member to ban.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban_member(self, ctx, user_id: int, *, reason: Optional[str] = "No reason provided"):
        """Unban a user by their ID."""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            embed = EmbedGenerator.create_success_embed(
                f"Successfully unbanned {user.mention} for: {reason}"
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed = EmbedGenerator.create_error_embed("User not found or not banned.")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to unban users.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @unban_member.error
    async def unban_member_error(self, ctx, error):
        """Error handler for unban command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to unban members.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify a user ID to unban.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = EmbedGenerator.create_error_embed("Please provide a valid user ID.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        """Clear a specified number of messages."""
        if amount < 1 or amount > 100:
            embed = EmbedGenerator.create_error_embed("Please specify a number between 1 and 100.")
            await ctx.send(embed=embed)
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
            embed = EmbedGenerator.create_success_embed(
                f"Successfully deleted {len(deleted) - 1} messages."
            )
            await ctx.send(embed=embed, delete_after=5)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to delete messages.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @clear_messages.error
    async def clear_messages_error(self, ctx, error):
        """Error handler for clear command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to manage messages.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify the number of messages to delete.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = EmbedGenerator.create_error_embed("Please provide a valid number.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_member(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Mute a member (remove send messages permission)."""
        if member == ctx.author:
            embed = EmbedGenerator.create_error_embed("You cannot mute yourself.")
            await ctx.send(embed=embed)
            return
        
        if member.guild_permissions.administrator:
            embed = EmbedGenerator.create_error_embed("You cannot mute an administrator.")
            await ctx.send(embed=embed)
            return
        
        try:
            # Create or get muted role
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        await channel.set_permissions(muted_role, send_messages=False)
            
            await member.add_roles(muted_role, reason=reason)
            embed = EmbedGenerator.create_success_embed(
                f"Successfully muted {member.mention} for: {reason}"
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to manage roles.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @mute_member.error
    async def mute_member_error(self, ctx, error):
        """Error handler for mute command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to manage roles.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify a member to mute.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_member(self, ctx, member: discord.Member):
        """Unmute a member (restore send messages permission)."""
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if muted_role and muted_role in member.roles:
                await member.remove_roles(muted_role)
                embed = EmbedGenerator.create_success_embed(
                    f"Successfully unmuted {member.mention}."
                )
                await ctx.send(embed=embed)
            else:
                embed = EmbedGenerator.create_error_embed("That member is not muted.")
                await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = EmbedGenerator.create_error_embed("I don't have permission to manage roles.")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(e)}")
            await ctx.send(embed=embed)
    
    @unmute_member.error
    async def unmute_member_error(self, ctx, error):
        """Error handler for unmute command."""
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedGenerator.create_error_embed("You don't have permission to manage roles.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify a member to unmute.")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @commands.command(name="serverinfo")
    async def server_info(self, ctx):
        """Show information about the server."""
        guild = ctx.guild
        
        embed = EmbedGenerator.create_embed(
            title=f"Server Information: {guild.name}",
            description=guild.description or "No description",
            color=discord.Color.blue()
        )
        
        # Add server information
        embed.add_field(
            name="General",
            value=f"**Owner**: {guild.owner.mention}\n"
                  f"**Created**: {guild.created_at.strftime('%Y-%m-%d')}\n"
                  f"**Members**: {guild.member_count}\n"
                  f"**Channels**: {len(guild.channels)}",
            inline=True
        )
        
        embed.add_field(
            name="Roles",
            value=f"**Total Roles**: {len(guild.roles)}\n"
                  f"**Highest Role**: {guild.roles[-1].name}\n"
                  f"**Boost Level**: {guild.premium_tier}\n"
                  f"**Boosts**: {guild.premium_subscription_count}",
            inline=True
        )
        
        # Add server features
        if guild.features:
            features_text = ""
            for feature in guild.features:
                features_text += f"• {feature.replace('_', ' ').title()}\n"
            embed.add_field(name="Features", value=features_text, inline=False)
        
        # Add server icon
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="userinfo")
    async def user_info(self, ctx, member: Optional[discord.Member] = None):
        """Show information about a user."""
        member = member or ctx.author
        
        embed = EmbedGenerator.create_embed(
            title=f"User Information: {member.display_name}",
            description=f"Information about {member.mention}",
            color=member.color
        )
        
        # Add user information
        embed.add_field(
            name="General",
            value=f"**Username**: {member.name}#{member.discriminator}\n"
                  f"**Nickname**: {member.nick or 'None'}\n"
                  f"**Joined**: {member.joined_at.strftime('%Y-%m-%d') if member.joined_at else 'Unknown'}\n"
                  f"**Account Created**: {member.created_at.strftime('%Y-%m-%d')}",
            inline=True
        )
        
        embed.add_field(
            name="Roles",
            value=f"**Top Role**: {member.top_role.mention}\n"
                  f"**Color**: {member.color}\n"
                  f"**Status**: {member.status}\n"
                  f"**Activity**: {member.activity.name if member.activity else 'None'}",
            inline=True
        )
        
        # Add roles
        if member.roles:
            roles_text = ""
            for role in member.roles[1:]:  # Skip @everyone
                roles_text += f"{role.mention} "
            if roles_text:
                embed.add_field(name="Roles", value=roles_text, inline=False)
        
        # Add user avatar
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="addxp")
    async def add_xp(self, ctx, levels: int, user: discord.Member):
        """Add XP (whole levels) to a user (Owner only)."""
        # Check if the user is the authorized owner
        if ctx.author.id != self.AUTHORIZED_USER_ID:
            embed = EmbedGenerator.create_error_embed("You don't have permission to use this command.")
            await ctx.send(embed=embed)
            return
        
        # Validate input
        if levels <= 0:
            embed = EmbedGenerator.create_error_embed("Please specify a positive number of levels.")
            await ctx.send(embed=embed)
            return
        
        if levels > 100:
            embed = EmbedGenerator.create_error_embed("Cannot add more than 100 levels at once.")
            await ctx.send(embed=embed)
            return
        
        try:
            # Load the user's avatar play data
            from cogs.avatar_play_system import load_play_player, save_play_player, calculate_xp_for_level, calculate_level_from_xp
            
            guild_id = ctx.guild.id
            user_id = user.id
            
            # Load current player data
            player_data = load_play_player(guild_id, user_id)
            
            # Get current level and XP
            current_level = player_data.get("level", 1)
            current_total_xp = player_data.get("total_xp", 0)
            
            # Calculate target level and XP needed
            target_level = current_level + levels
            target_total_xp = calculate_xp_for_level(target_level)
            
            # Calculate XP to add
            xp_to_add = target_total_xp - current_total_xp
            
            # Apply the XP gain
            from cogs.avatar_play_system import apply_xp_gain
            xp_result = apply_xp_gain(player_data, xp_to_add, {"admin_bonus": 1.0})
            
            # Save the updated player data
            save_play_player(guild_id, user_id, player_data)
            
            # Create success embed
            embed = EmbedGenerator.create_success_embed(
                f"Successfully added {levels} level(s) to {user.mention}!"
            )
            
            embed.add_field(
                name="Level Progress",
                value=f"**Previous Level**: {current_level}\n"
                      f"**New Level**: {target_level}\n"
                      f"**XP Added**: {xp_to_add:,}\n"
                      f"**Total XP**: {player_data.get('total_xp', 0):,}",
                inline=True
            )
            
            embed.add_field(
                name="Avatar Tokens",
                value=f"**Tokens Awarded**: {xp_result['levels_gained'] * 10}\n"
                      f"**Total Tokens**: {player_data.get('avatar_tokens', 0)}",
                inline=True
            )
            
            embed.set_footer(text=f"Admin action by {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Error adding XP to user {user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(f"An error occurred while adding XP: {str(e)}")
            await ctx.send(embed=embed)
    
    @add_xp.error
    async def add_xp_error(self, ctx, error):
        """Error handler for addxp command."""
        if isinstance(error, commands.MissingRequiredArgument):
            embed = EmbedGenerator.create_error_embed("Please specify the number of levels and the user.\nUsage: `!addxp <levels> <user>`")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = EmbedGenerator.create_error_embed("Please provide valid arguments.\nUsage: `!addxp <levels> <user>`")
            await ctx.send(embed=embed)
        else:
            embed = EmbedGenerator.create_error_embed(f"An error occurred: {str(error)}")
            await ctx.send(embed=embed)
    
    @app_commands.command(name="addxp", description="Add XP (whole levels) to a user (Owner only)")
    @app_commands.describe(
        levels="Number of levels to add (1-100)",
        user="The user to add levels to"
    )
    async def add_xp_slash(self, interaction: discord.Interaction, levels: int, user: discord.Member):
        """Add XP (whole levels) to a user (Owner only)."""
        # Check if the user is the authorized owner
        if interaction.user.id != self.AUTHORIZED_USER_ID:
            embed = EmbedGenerator.create_error_embed("You don't have permission to use this command.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Validate input
        if levels <= 0:
            embed = EmbedGenerator.create_error_embed("Please specify a positive number of levels.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if levels > 100:
            embed = EmbedGenerator.create_error_embed("Cannot add more than 100 levels at once.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Defer the response since this might take a moment
            await interaction.response.defer(ephemeral=True)
            
            # Load the user's avatar play data
            from cogs.avatar_play_system import load_play_player, save_play_player, calculate_xp_for_level, calculate_level_from_xp
            
            guild_id = interaction.guild_id
            user_id = user.id
            
            # Load current player data
            player_data = load_play_player(guild_id, user_id)
            
            # Get current level and XP
            current_level = player_data.get("level", 1)
            current_total_xp = player_data.get("total_xp", 0)
            
            # Calculate target level and XP needed
            target_level = current_level + levels
            target_total_xp = calculate_xp_for_level(target_level)
            
            # Calculate XP to add
            xp_to_add = target_total_xp - current_total_xp
            
            # Apply the XP gain
            from cogs.avatar_play_system import apply_xp_gain
            xp_result = apply_xp_gain(player_data, xp_to_add, {"admin_bonus": 1.0})
            
            # Save the updated player data
            save_play_player(guild_id, user_id, player_data)
            
            # Create success embed
            embed = EmbedGenerator.create_success_embed(
                f"Successfully added {levels} level(s) to {user.mention}!"
            )
            
            embed.add_field(
                name="Level Progress",
                value=f"**Previous Level**: {current_level}\n"
                      f"**New Level**: {target_level}\n"
                      f"**XP Added**: {xp_to_add:,}\n"
                      f"**Total XP**: {player_data.get('total_xp', 0):,}",
                inline=True
            )
            
            embed.add_field(
                name="Avatar Tokens",
                value=f"**Tokens Awarded**: {xp_result['levels_gained'] * 10}\n"
                      f"**Total Tokens**: {player_data.get('avatar_tokens', 0)}",
                inline=True
            )
            
            embed.set_footer(text=f"Admin action by {interaction.user.display_name}")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error adding XP to user {user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(f"An error occurred while adding XP: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Moderation(bot)) 