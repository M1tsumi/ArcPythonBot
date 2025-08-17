"""
Additional Admin Commands for Avatar Realms Collide Discord Bot.
Owner-only commands for user and server management.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from utils.permissions import is_owner

class AdminCommands(commands.Cog):
    """Additional admin commands for comprehensive bot management."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="admin_give_role", description="🎭 Give role to user - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def give_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """Give a role to a user."""
        try:
            await user.add_roles(role)
            embed = discord.Embed(
                title="✅ Role Added",
                description=f"Successfully gave **{role.name}** to {user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to manage this role.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to give role: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_remove_role", description="❌ Remove role from user - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def remove_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """Remove a role from a user."""
        try:
            await user.remove_roles(role)
            embed = discord.Embed(
                title="✅ Role Removed",
                description=f"Successfully removed **{role.name}** from {user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to manage this role.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to remove role: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_change_nickname", description="✏️ Change a user's nickname - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def change_nickname(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        nickname: Optional[str] = None,
    ):
        """Change or clear a member's nickname."""
        try:
            await member.edit(nick=nickname)
            description = (
                f"Successfully changed {member.mention}'s nickname to **{nickname}**"
                if nickname
                else f"Cleared {member.mention}'s nickname"
            )
            embed = discord.Embed(
                title="✅ Nickname Updated",
                description=description,
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to change this nickname.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to change nickname: {str(e)}",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="admin_user_info", description="ℹ️ Get detailed user information - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def user_info(self, interaction: discord.Interaction, user: discord.Member):
        """Get detailed user information."""

        # Get user roles
        roles = [role.mention for role in user.roles if role.name != "@everyone"]
        roles_text = ", ".join(roles) if roles else "No roles"
        
        # Get user permissions
        permissions = []
        for perm, value in user.guild_permissions:
            if value:
                permissions.append(f"✅ {perm.replace('_', ' ').title()}")
        
        embed = discord.Embed(
            title=f"ℹ️ User Information - {user.name}",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue()
        )
        
        embed.add_field(
            name="👤 User Details",
            value=f"**ID**: {user.id}\n"
                  f"**Created**: <t:{int(user.created_at.timestamp())}:F>\n"
                  f"**Joined**: <t:{int(user.joined_at.timestamp())}:F>\n"
                  f"**Status**: {str(user.status).title()}\n"
                  f"**Bot**: {'Yes' if user.bot else 'No'}",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Roles & Permissions",
            value=f"**Top Role**: {user.top_role.mention}\n"
                  f"**Color**: {user.color if user.color != discord.Color.default() else 'Default'}\n"
                  f"**Roles**: {len(user.roles) - 1}\n"
                  f"**Key Permissions**: {len(permissions)}",
            inline=True
        )
        
        embed.add_field(
            name="📊 Server Activity",
            value=f"**Nickname**: {user.nick or 'None'}\n"
                  f"**Timed Out**: {'Yes' if user.timed_out else 'No'}\n"
                  f"**Premium Since**: {user.premium_since.strftime('%Y-%m-%d') if user.premium_since else 'None'}\n"
                  f"**Mobile**: {'Yes' if user.is_on_mobile() else 'No'}",
            inline=True
        )
        
        if len(roles) > 0:
            embed.add_field(
                name="🎭 Roles",
                value=roles_text[:1024] + "..." if len(roles_text) > 1024 else roles_text,
                inline=False
            )
        
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_create_channel", description="📝 Create a new channel - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def create_channel(self, interaction: discord.Interaction, name: str, channel_type: str = "text"):
        """Create a new channel."""
        try:
            if channel_type.lower() in ["text", "txt"]:
                channel = await interaction.guild.create_text_channel(name=name)
                channel_type_name = "Text Channel"
            elif channel_type.lower() in ["voice", "vc"]:
                channel = await interaction.guild.create_voice_channel(name=name)
                channel_type_name = "Voice Channel"
            elif channel_type.lower() in ["category", "cat"]:
                channel = await interaction.guild.create_category(name=name)
                channel_type_name = "Category"
            else:
                embed = discord.Embed(
                    title="❌ Invalid Channel Type",
                    description="Valid types: text, voice, category",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = discord.Embed(
                title="✅ Channel Created",
                description=f"Successfully created **{channel_type_name}**: {channel.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to create channels.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create channel: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_delete_channel", description="🗑️ Delete a channel - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def delete_channel(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        """Delete a channel."""
        try:
            channel_name = channel.name
            await channel.delete()
            embed = discord.Embed(
                title="✅ Channel Deleted",
                description=f"Successfully deleted **{channel_name}**",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to delete this channel.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to delete channel: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_role_create", description="🔧 Create a new role - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def create_role(self, interaction: discord.Interaction, name: str, color: str = "default"):
        """Create a new role."""
        try:
            # Parse color
            if color.lower() == "default":
                role_color = discord.Color.default()
            else:
                # Try to parse hex color
                try:
                    role_color = discord.Color.from_str(color)
                except:
                    role_color = discord.Color.blue()
            
            role = await interaction.guild.create_role(name=name, color=role_color)
            embed = discord.Embed(
                title="✅ Role Created",
                description=f"Successfully created role: {role.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to create roles.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create role: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_ban_user", description="🔨 Ban a user - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def ban_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        """Ban a user from the server."""
        try:
            await user.ban(reason=f"Admin ban by {interaction.user.name}: {reason}")
            embed = discord.Embed(
                title="✅ User Banned",
                description=f"Successfully banned {user.mention}\n**Reason**: {reason}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to ban users.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to ban user: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_unban_user", description="🔓 Unban a user - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def unban_user(self, interaction: discord.Interaction, user_id: str):
        """Unban a user from the server."""
        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            embed = discord.Embed(
                title="✅ User Unbanned",
                description=f"Successfully unbanned {user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid User ID",
                description="Please provide a valid user ID.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to unban users.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to unban user: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="admin_kick_user", description="👢 Kick a user - Owner Only")
    @app_commands.check(is_owner)
    @app_commands.default_permissions(administrator=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        """Kick a user from the server."""
        try:
            await user.kick(reason=f"Admin kick by {interaction.user.name}: {reason}")
            embed = discord.Embed(
                title="✅ User Kicked",
                description=f"Successfully kicked {user.mention}\n**Reason**: {reason}",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to kick users.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to kick user: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
