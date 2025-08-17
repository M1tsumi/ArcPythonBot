"""
Admin Panel for Avatar Realms Collide Discord Bot.
Owner-only commands for comprehensive bot management.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import json
from pathlib import Path

class AdminPanel(commands.Cog):
    """Admin panel with owner-only commands for bot management."""
    
    def __init__(self, bot):
        self.bot = bot
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
        
    async def cog_check(self, ctx):
        """Check if user is the bot owner."""
        return ctx.author.id == self.owner_id
    
    @app_commands.command(name="admin", description="🔧 Admin Panel - Owner Only")
    @app_commands.default_permissions(administrator=True)
    async def admin_panel(self, interaction: discord.Interaction):
        """Open the admin panel with various management options."""
        # Check if user is owner
        if interaction.user.id != self.owner_id:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="This command is restricted to the bot owner only.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🔧 Admin Panel",
            description="Welcome to the bot administration panel. Select an option below:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Bot Management",
            value="• **Create Webhook** - Create webhook in current channel\n"
                  "• **Leave Server** - Make bot leave current server\n"
                  "• **Server Info** - Get detailed server information\n"
                  "• **Bot Status** - View bot statistics and status",
            inline=False
        )
        
        embed.add_field(
            name="👥 User Management",
            value="• **Give Role** - Give yourself or others roles\n"
                  "• **Remove Role** - Remove roles from users\n"
                  "• **User Info** - Get detailed user information\n"
                  "• **Change Nickname** - Change or reset user nicknames\n"
                  "• **Ban User** - Ban users from server\n"
                  "• **Unban User** - Unban users from server",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Server Management",
            value="• **Channel Info** - Get channel information\n"
                  "• **Create Channel** - Create new channels\n"
                  "• **Delete Channel** - Delete channels\n"
                  "• **Server Settings** - View server configuration\n"
                  "• **Role Management** - Manage server roles",
            inline=False
        )
        
        embed.add_field(
            name="🔍 Monitoring & Debug",
            value="• **Bot Logs** - View recent bot activity\n"
                  "• **Error Logs** - View error reports\n"
                  "• **Performance** - Check bot performance\n"
                  "• **Memory Usage** - Monitor resource usage",
            inline=False
        )
        
        embed.set_footer(text="Owner Only • Use buttons below to access features")
        
        view = AdminPanelView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class AdminPanelView(discord.ui.View):
    """View for admin panel buttons."""
    
    def __init__(self, bot):
        super().__init__(timeout=300)  # 5 minute timeout
        self.bot = bot
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if user is owner."""
        return interaction.user.id == self.owner_id
    
    @discord.ui.button(label="🔗 Create Webhook", style=discord.ButtonStyle.primary, row=0)
    async def create_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Create a webhook in the current channel."""
        try:
            webhook = await interaction.channel.create_webhook(name="Admin Webhook")
            embed = discord.Embed(
                title="✅ Webhook Created",
                description=f"Webhook created successfully!\n**URL**: {webhook.url}",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=embed, view=None)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to create webhooks in this channel.",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to create webhook: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🚪 Leave Server", style=discord.ButtonStyle.danger, row=0)
    async def leave_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Make the bot leave the current server."""
        embed = discord.Embed(
            title="⚠️ Confirm Server Leave",
            description=f"Are you sure you want me to leave **{interaction.guild.name}**?\n\n"
                       f"**Server ID**: {interaction.guild.id}\n"
                       f"**Member Count**: {interaction.guild.member_count}\n"
                       f"**Owner**: {interaction.guild.owner.mention}",
            color=discord.Color.orange()
        )
        
        view = ConfirmLeaveView(self.bot, interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="📊 Server Info", style=discord.ButtonStyle.secondary, row=0)
    async def server_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Get detailed server information."""
        guild = interaction.guild
        
        # Get bot permissions
        bot_permissions = guild.me.guild_permissions
        permission_list = []
        for perm, value in bot_permissions:
            if value:
                permission_list.append(f"✅ {perm.replace('_', ' ').title()}")
            else:
                permission_list.append(f"❌ {perm.replace('_', ' ').title()}")
        
        embed = discord.Embed(
            title=f"📊 Server Information - {guild.name}",
            description=guild.description or "No description",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="👑 Server Details",
            value=f"**Owner**: {guild.owner.mention}\n"
                  f"**Created**: <t:{int(guild.created_at.timestamp())}:F>\n"
                  f"**Members**: {guild.member_count:,}\n"
                  f"**Channels**: {len(guild.channels)}\n"
                  f"**Roles**: {len(guild.roles)}",
            inline=True
        )
        
        embed.add_field(
            name="🔧 Bot Status",
            value=f"**Joined**: <t:{int(guild.me.joined_at.timestamp())}:F>\n"
                  f"**Permissions**: {len([p for p in permission_list if p.startswith('✅')])}/{len(permission_list)}\n"
                  f"**Webhooks**: {len(await guild.webhooks())}\n"
                  f"**Emojis**: {len(guild.emojis)}",
            inline=True
        )
        
        embed.add_field(
            name="📈 Server Stats",
            value=f"**Text Channels**: {len(guild.text_channels)}\n"
                  f"**Voice Channels**: {len(guild.voice_channels)}\n"
                  f"**Categories**: {len(guild.categories)}\n"
                  f"**Boost Level**: {guild.premium_tier}",
            inline=True
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text=f"Server ID: {guild.id}")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🤖 Bot Status", style=discord.ButtonStyle.secondary, row=0)
    async def bot_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        """View bot statistics and status."""
        import psutil
        import time
        
        # Get bot statistics
        uptime = time.time() - self.bot.start_time
        memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        embed = discord.Embed(
            title="🤖 Bot Status & Statistics",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 General Stats",
            value=f"**Servers**: {len(self.bot.guilds):,}\n"
                  f"**Users**: {len(self.bot.users):,}\n"
                  f"**Commands**: {len(self.bot.commands)}\n"
                  f"**Cogs**: {len(self.bot.cogs)}",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Performance",
            value=f"**Uptime**: {int(uptime // 3600)}h {int((uptime % 3600) // 60)}m\n"
                  f"**Memory**: {memory:.1f} MB\n"
                  f"**Latency**: {round(self.bot.latency * 1000)}ms\n"
                  f"**CPU**: {psutil.cpu_percent()}%",
            inline=True
        )
        
        embed.add_field(
            name="🔧 System Info",
            value=f"**Python**: {psutil.sys.version.split()[0]}\n"
                  f"**Discord.py**: {discord.__version__}\n"
                  f"**Platform**: {psutil.sys.platform}\n"
                  f"**Architecture**: {psutil.sys.maxsize > 2**32 and '64-bit' or '32-bit'}",
            inline=True
        )
        
        # Get recent guild joins
        recent_guilds = sorted(self.bot.guilds, key=lambda g: g.me.joined_at, reverse=True)[:5]
        guild_list = "\n".join([f"• {g.name} ({g.member_count:,} members)" for g in recent_guilds])
        
        embed.add_field(
            name="🆕 Recent Servers",
            value=guild_list or "No recent servers",
            inline=False
        )
        
        embed.set_footer(text=f"Bot ID: {self.bot.user.id}")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="👤 User Management", style=discord.ButtonStyle.primary, row=1)
    async def user_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open user management panel."""
        embed = discord.Embed(
            title="👤 User Management Panel",
            description="Select an action to manage users:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Available Actions",
            value="• **Give Role** - Assign roles to users\n"
                  "• **Remove Role** - Remove roles from users\n"
                  "• **User Info** - Get detailed user information\n"
                  "• **Change Nickname** - Change or reset user nicknames\n"
                  "• **Ban User** - Ban users from server\n"
                  "• **Unban User** - Unban users from server\n"
                  "• **Kick User** - Kick users from server",
            inline=False
        )
        
        view = UserManagementView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="⚙️ Server Management", style=discord.ButtonStyle.primary, row=1)
    async def server_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open server management panel."""
        embed = discord.Embed(
            title="⚙️ Server Management Panel",
            description="Select an action to manage the server:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Available Actions",
            value="• **Channel Info** - Get channel information\n"
                  "• **Create Channel** - Create new channels\n"
                  "• **Delete Channel** - Delete channels\n"
                  "• **Role Management** - Manage server roles\n"
                  "• **Server Settings** - View server configuration\n"
                  "• **Permission Audit** - Check bot permissions",
            inline=False
        )
        
        view = ServerManagementView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="🔍 Monitoring", style=discord.ButtonStyle.secondary, row=1)
    async def monitoring(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open monitoring and debug panel."""
        embed = discord.Embed(
            title="🔍 Monitoring & Debug Panel",
            description="Select an action to monitor the bot:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Available Actions",
            value="• **Bot Logs** - View recent bot activity\n"
                  "• **Error Logs** - View error reports\n"
                  "• **Performance** - Check bot performance\n"
                  "• **Memory Usage** - Monitor resource usage\n"
                  "• **Command Stats** - View command usage\n"
                  "• **System Health** - Overall system status",
            inline=False
        )
        
        view = MonitoringView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class ConfirmLeaveView(discord.ui.View):
    """Confirmation view for leaving server."""
    
    def __init__(self, bot, guild):
        super().__init__(timeout=60)
        self.bot = bot
        self.guild = guild
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.owner_id
    
    @discord.ui.button(label="✅ Confirm Leave", style=discord.ButtonStyle.danger)
    async def confirm_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm leaving the server."""
        embed = discord.Embed(
            title="👋 Leaving Server",
            description=f"Goodbye **{self.guild.name}**!\n\n"
                       f"I'm leaving this server now. Thanks for having me!",
            color=discord.Color.red()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Leave the server
        await self.guild.leave()
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel leaving the server."""
        embed = discord.Embed(
            title="✅ Cancelled",
            description="I'm staying in this server.",
            color=discord.Color.green()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)

class UserManagementView(discord.ui.View):
    """View for user management options."""
    
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.owner_id
    
    @discord.ui.button(label="🎭 Give Role", style=discord.ButtonStyle.primary)
    async def give_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Give a role to a user."""
        embed = discord.Embed(
            title="🎭 Give Role",
            description="Use `/admin_give_role @user @role` to give a role to a user.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="❌ Remove Role", style=discord.ButtonStyle.danger)
    async def remove_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Remove a role from a user."""
        embed = discord.Embed(
            title="❌ Remove Role",
            description="Use `/admin_remove_role @user @role` to remove a role from a user.",
            color=discord.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="ℹ️ User Info", style=discord.ButtonStyle.secondary)
    async def user_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Get user information."""
        embed = discord.Embed(
            title="ℹ️ User Info",
            description="Use `/admin_user_info @user` to get detailed user information.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="✏️ Change Nickname", style=discord.ButtonStyle.secondary)
    async def change_nickname(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show command to change a user's nickname."""
        embed = discord.Embed(
            title="✏️ Change Nickname",
            description="Use `/admin_change_nickname @user new_nick` to change or clear a user's nickname.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)

class ServerManagementView(discord.ui.View):
    """View for server management options."""
    
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.owner_id
    
    @discord.ui.button(label="📝 Create Channel", style=discord.ButtonStyle.primary)
    async def create_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Create a new channel."""
        embed = discord.Embed(
            title="📝 Create Channel",
            description="Use `/admin_create_channel name type` to create a new channel.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🗑️ Delete Channel", style=discord.ButtonStyle.danger)
    async def delete_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Delete a channel."""
        embed = discord.Embed(
            title="🗑️ Delete Channel",
            description="Use `/admin_delete_channel #channel` to delete a channel.",
            color=discord.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🔧 Role Management", style=discord.ButtonStyle.secondary)
    async def role_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Manage server roles."""
        embed = discord.Embed(
            title="🔧 Role Management",
            description="Use `/admin_role_create name` to create a new role.",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=None)

class MonitoringView(discord.ui.View):
    """View for monitoring options."""
    
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        # Hardcoded owner ID
        self.owner_id = 1051142172130422884
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.owner_id
    
    @discord.ui.button(label="📊 Performance", style=discord.ButtonStyle.primary)
    async def performance(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Check bot performance."""
        import psutil
        import time
        
        uptime = time.time() - self.bot.start_time
        memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        embed = discord.Embed(
            title="📊 Performance Metrics",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="⚡ System Performance",
            value=f"**CPU Usage**: {psutil.cpu_percent()}%\n"
                  f"**Memory Usage**: {memory:.1f} MB\n"
                  f"**Uptime**: {int(uptime // 3600)}h {int((uptime % 3600) // 60)}m\n"
                  f"**Latency**: {round(self.bot.latency * 1000)}ms",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🔍 System Health", style=discord.ButtonStyle.secondary)
    async def system_health(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Check overall system health."""
        import psutil
        
        embed = discord.Embed(
            title="🔍 System Health Check",
            color=discord.Color.green()
        )
        
        # Check various system components
        checks = []
        
        # Memory check
        memory_percent = psutil.virtual_memory().percent
        if memory_percent < 80:
            checks.append(f"✅ Memory: {memory_percent}%")
        else:
            checks.append(f"⚠️ Memory: {memory_percent}% (High)")
        
        # CPU check
        cpu_percent = psutil.cpu_percent()
        if cpu_percent < 80:
            checks.append(f"✅ CPU: {cpu_percent}%")
        else:
            checks.append(f"⚠️ CPU: {cpu_percent}% (High)")
        
        # Bot latency check
        latency = self.bot.latency * 1000
        if latency < 200:
            checks.append(f"✅ Latency: {round(latency)}ms")
        else:
            checks.append(f"⚠️ Latency: {round(latency)}ms (High)")
        
        # Guild count check
        guild_count = len(self.bot.guilds)
        if guild_count > 0:
            checks.append(f"✅ Guilds: {guild_count}")
        else:
            checks.append(f"❌ Guilds: {guild_count}")
        
        embed.add_field(
            name="System Status",
            value="\n".join(checks),
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=None)

async def setup(bot):
    await bot.add_cog(AdminPanel(bot))
