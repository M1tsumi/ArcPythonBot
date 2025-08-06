"""
Utility command module for Avatar Realms Collide Discord Bot.
Provides utility commands like links, help, ping, info, and bot management.
"""

import discord
from discord import app_commands
from discord.ext import commands
from config.settings import DISCORD_SERVER_LINK, BOT_INVITE_LINK, DEVELOPMENT_SERVER_LINK
import time

class Utility(commands.Cog):
    """Utility command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @commands.command(name="ping", description="Check bot latency and status")
    async def ping_prefix(self, ctx):
        """Traditional prefix command to check bot latency and status."""
        start_time = time.time()
        
        # Create initial embed
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Checking bot status and latency...",
            color=discord.Color.blue()
        )
        
        # Send initial response
        message = await ctx.send(embed=embed)
        
        # Calculate latency
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        api_latency = round(self.bot.latency * 1000, 2)  # Discord API latency
        
        # Update embed with results
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Bot is online and responding!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 Response Time",
            value=f"**{latency:.1f}ms**",
            inline=True
        )
        
        embed.add_field(
            name="🌐 API Latency",
            value=f"**{api_latency}ms**",
            inline=True
        )
        
        embed.add_field(
            name="🆔 Bot Status",
            value="✅ Online and Ready",
            inline=True
        )
        
        embed.add_field(
            name="🏠 Servers",
            value=f"**{len(self.bot.guilds)}** servers",
            inline=True
        )
        
        embed.add_field(
            name="👥 Users",
            value=f"**{len(self.bot.users)}** users",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Commands",
            value=f"**{len(self.bot.tree.get_commands())}** slash commands",
            inline=True
        )
        
        embed.set_footer(text="Developed by Quefep • Avatar Realms Collide Bot")
        
        await message.edit(embed=embed)
    
    @commands.command(name="help", description="Get help and command information")
    async def help_prefix(self, ctx):
        """Traditional prefix command to provide help and command information."""
        embed = discord.Embed(
            title="🌟 Avatar Realms Collide Bot Help",
            description="Welcome to the Avatar Realms Collide community bot! Here are all available commands organized by category.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎮 Game Information Commands",
            value="• `!talent_trees` - Browse character talent trees\n• `!skill_priorities` - View hero skill priorities\n• `!hero_info` - Get detailed hero information\n• `!hero_rankup` - View hero rankup guide and costs\n• `!townhall` - View town hall requirements\n• `!leaderboard` - Check top players and alliances",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Event Commands",
            value="• `!events` - View current and upcoming events\n• `!avatar_day_festival` - Avatar Day Festival information\n• `!festival_tasks` - View all festival tasks by day\n• `!festival_shop` - View festival exchange shop\n• `!festival_guide` - Get festival tips and strategy\n• `!festival_rewards` - View all festival rewards\n• `!balance_and_order` - Balance and Order event information\n• `!balance_tasks` - View Balance and Order tasks\n• `!balance_guide` - Get Balance and Order tips\n• `!borte_scheme` - Borte's Scheme event information\n• `!borte_mechanics` - View Borte's Scheme mechanics\n• `!borte_rewards` - View Borte's Scheme rewards\n• `!borte_guide` - Get Borte's Scheme tips",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Rally System Commands",
            value="• `!setup` - Setup rally system (Admin)\n• `!rally` - Create a new rally (level + time limit)\n• `!rally_stats` - View your rally statistics\n• `!rally_leaderboard` - View rally leaderboard\n• `!leader` - Admin leaderboard management (pause/resume/clear)",
            inline=False
        )
        
        embed.add_field(
            name="🏆 TGL Commands",
            value="• `!tgl` - The Greatest Leader event information\n• `!tgl_calc` - Calculate TGL points for activities",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Utility Commands",
            value="• `!ping` - Check bot status and latency\n• `!info` - Comprehensive bot information\n• `!links` - Get bot links and information\n• `!addtoserver` - Add bot to your server",
            inline=False
        )
        
        embed.add_field(
            name="📱 Join Our Discord Server",
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\nGet help, ask questions, and connect with other players!",
            inline=False
        )
        
        embed.set_footer(text="Developed by Quefep • Use /help for slash commands • Join our Discord for the best experience!")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="info", description="Get comprehensive bot information and contribution details")
    async def info_prefix(self, ctx):
        """Traditional prefix command to provide comprehensive bot information and contribution details."""
        embed = discord.Embed(
            title="🤖 Avatar Realms Collide Bot Information",
            description="Unofficial community bot providing game tools and information.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎮 Key Features",
            value="• Talent Trees & Hero Info\n• Leaderboards & Rally System\n• Event Tools & Timers\n• Town Hall & Skill Guides",
            inline=False
        )
        
        embed.add_field(
            name="👨‍💻 Developer & Contributors",
            value="**Developed by Quefep**\n**Contributors**: Lycaris (comprehensive event overview), PrincessBell & Samkee (event details), Kuvira (talent trees, skill priorities, town hall stats)",
            inline=False
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Contribute",
            value="Share game data, images, or resources! Contact **quefep** on Discord.",
            inline=False
        )
        
        embed.set_footer(text="Unofficial fan-made bot • Join our Discord!")
        
        # Create view with development server button
        view = discord.ui.View(timeout=None)
        dev_server_button = discord.ui.Button(
            label="Join Development Server",
            url=DEVELOPMENT_SERVER_LINK,
            style=discord.ButtonStyle.link,
            emoji="🔗"
        )
        view.add_item(dev_server_button)
        
        await ctx.send(embed=embed, view=view)
    
    @app_commands.command(name="ping", description="Check bot latency and status")
    async def ping(self, interaction: discord.Interaction):
        """Command to check bot latency and status."""
        start_time = time.time()
        
        # Create initial embed
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Checking bot status and latency...",
            color=discord.Color.blue()
        )
        
        # Send initial response
        await interaction.response.send_message(embed=embed)
        
        # Calculate latency
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        api_latency = round(self.bot.latency * 1000, 2)  # Discord API latency
        
        # Update embed with results
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Bot is online and responding!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 Response Time",
            value=f"**{latency:.1f}ms**",
            inline=True
        )
        
        embed.add_field(
            name="🌐 API Latency",
            value=f"**{api_latency}ms**",
            inline=True
        )
        
        embed.add_field(
            name="🆔 Bot Status",
            value="✅ Online and Ready",
            inline=True
        )
        
        embed.add_field(
            name="🏠 Servers",
            value=f"**{len(self.bot.guilds)}** servers",
            inline=True
        )
        
        embed.add_field(
            name="👥 Users",
            value=f"**{len(self.bot.users)}** users",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Commands",
            value=f"**{len(self.bot.tree.get_commands())}** slash commands",
            inline=True
        )
        
        embed.set_footer(text="Developed by Quefep • Avatar Realms Collide Bot")
        
        await interaction.edit_original_response(embed=embed)
    
    @app_commands.command(name="info", description="Get comprehensive bot information and contribution details")
    async def info(self, interaction: discord.Interaction):
        """Command to provide comprehensive bot information and contribution details."""
        embed = discord.Embed(
            title="🤖 Avatar Realms Collide Bot Information",
            description="Unofficial community bot providing game tools and information.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎮 Key Features",
            value="• Talent Trees & Hero Info\n• Leaderboards & Rally System\n• Event Tools & Timers\n• Town Hall & Skill Guides",
            inline=False
        )
        
        embed.add_field(
            name="👨‍💻 Developer & Contributors",
            value="**Developed by Quefep**\n**Contributors**: Lycaris (comprehensive event overview), PrincessBell & Samkee (event details), Kuvira (talent trees, skill priorities, town hall stats), Drummer (@priskent) & Marshmellow (@sophremacy) (troop information and costs)",
            inline=False
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Contribute",
            value="Share game data, images, or resources! Contact **quefep** on Discord.",
            inline=False
        )
        
        embed.set_footer(text="Unofficial fan-made bot • Join our Discord!")
        
        # Create view with development server button
        view = discord.ui.View(timeout=None)
        dev_server_button = discord.ui.Button(
            label="Join Development Server",
            url=DEVELOPMENT_SERVER_LINK,
            style=discord.ButtonStyle.link,
            emoji="🔗"
        )
        view.add_item(dev_server_button)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="links", description="Get bot links and information")
    async def links(self, interaction: discord.Interaction):
        """Command to provide bot links and information."""
        embed = discord.Embed(
            title="🔗 Bot Links & Information",
            description="Connect with the Avatar Realms Collide community!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📱 Join Our Discord Server",
            value=f"[Join Server]({DISCORD_SERVER_LINK})",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Add Bot to Your Server",
            value=f"[Add to Server]({BOT_INVITE_LINK})",
            inline=True
        )
        
        embed.add_field(
            name="👨‍💻 Developer",
            value="**Developed by Quefep**",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Bot Features",
            value="• Talent Tree Browser\n• Skill Priorities\n• Leaderboards\n• Town Hall Info\n• Hero Rankup Guide\n• Interactive Commands",
            inline=False
        )
        
        embed.set_footer(text="Join our Discord for more information and updates!")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Get help and join our Discord server")
    async def help(self, interaction: discord.Interaction):
        """Command to provide help and Discord server link."""
        embed = discord.Embed(
            title="🌟 Avatar Realms Collide Bot Help",
            description="Welcome to the Avatar Realms Collide community bot! Here's how to get help and stay connected.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📱 Join Our Discord Server",
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\nGet help, ask questions, and connect with other players!",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Game Information Commands",
            value="• `/talent_trees` - Browse character talent trees\n• `/skill_priorities` - View hero skill priorities\n• `/hero_info` - Get detailed hero information\n• `/hero_rankup` - View hero rankup guide and costs\n• `/townhall` - View town hall requirements\n• `/leaderboard` - Check top players and alliances",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Event Commands",
            value="• `/events` - View current and upcoming events\n• `/avatar_day_festival` - Avatar Day Festival information\n• `/festival_tasks` - View all festival tasks by day\n• `/festival_shop` - View festival exchange shop\n• `/festival_guide` - Get festival tips and strategy\n• `/festival_rewards` - View all festival rewards\n• `/balance_and_order` - Balance and Order event information\n• `/balance_tasks` - View Balance and Order tasks\n• `/balance_guide` - Get Balance and Order tips\n• `/borte_scheme` - Borte's Scheme event information\n• `/borte_mechanics` - View Borte's Scheme mechanics\n• `/borte_rewards` - View Borte's Scheme rewards\n• `/borte_guide` - Get Borte's Scheme tips",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Rally System Commands",
            value="• `/setup` - Setup rally system (Admin)\n• `/rally` - Create a new rally (level + time limit)\n• `/rally_stats` - View your rally statistics\n• `/rally_leaderboard` - View rally leaderboard\n• `/leader` - Admin leaderboard management (pause/resume/clear)",
            inline=False
        )
        
        embed.add_field(
            name="🏆 TGL Commands",
            value="• `/tgl` - The Greatest Leader event information\n• `/tgl_calc` - Calculate TGL points for activities",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Utility Commands",
            value="• `/ping` - Check bot status and latency\n• `/info` - Comprehensive bot information\n• `/links` - Get bot links and information\n• `/addtoserver` - Add bot to your server",
            inline=False
        )
        
        embed.add_field(
            name="💡 Need More Help?",
            value="Join our Discord server for:\n• Real-time help and support\n• Game updates and announcements\n• Community discussions\n• Bug reports and suggestions\n• Contribution opportunities",
            inline=False
        )
        
        embed.set_footer(text="Developed by Quefep • Join our Discord for the best experience!")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="addtoserver", description="Add the bot to your server")
    async def addtoserver(self, interaction: discord.Interaction):
        """Command to add the bot to a server with an embed and button."""
        embed = discord.Embed(
            title="🤖 Add Avatar Realms Collide Bot to Your Server",
            description="Enhance your server with powerful game tools and community features!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎮 Bot Features",
            value="• **Talent Tree Browser** - View all character talent trees\n• **Skill Priorities** - Get optimal skill upgrade orders\n• **Leaderboards** - Track top players and alliances\n• **Town Hall Info** - View upgrade requirements\n• **Hero Rankup Guide** - Complete rankup costs and guide\n• **Event System** - Current and upcoming events\n• **Rally System** - Create and join Shattered Skulls Fortress rallies\n• **Interactive Commands** - Modern slash command interface",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Permissions Required",
            value="• Send Messages\n• Embed Links\n• Attach Files\n• Use Slash Commands\n• Read Message History",
            inline=False
        )
        
        embed.add_field(
            name="📱 Community",
            value=f"[Join our Discord server]({DISCORD_SERVER_LINK}) for support and updates!",
            inline=False
        )
        
        embed.set_footer(text="Developed by Quefep • Unofficial fan-made bot")
        
        # Create view with invite button
        view = discord.ui.View(timeout=None)
        invite_button = discord.ui.Button(
            label="Add to Server",
            url=BOT_INVITE_LINK,
            style=discord.ButtonStyle.link,
            emoji="🤖"
        )
        view.add_item(invite_button)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="server", description="List all servers the bot is in (Owner only)")
    async def server_list(self, interaction: discord.Interaction):
        """Command to list all servers the bot is in with invite links and owner info."""
        # Check if user is authorized (only specific user ID can use this)
        AUTHORIZED_USER_ID = 1051142172130422884
        
        if interaction.user.id != AUTHORIZED_USER_ID:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Defer the response since this might take a while
            await interaction.response.defer(ephemeral=True)
            
            embed = discord.Embed(
                title="🏠 Bot Server List",
                description=f"Bot is currently in **{len(self.bot.guilds)}** servers",
                color=discord.Color.blue()
            )
            
            # Get all guilds and sort them by member count
            guilds = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)
            
            server_list = ""
            total_members = 0
            
            for i, guild in enumerate(guilds, 1):
                # Get owner info
                owner = guild.owner
                owner_mention = owner.mention if owner else "Unknown"
                owner_name = owner.display_name if owner else "Unknown"
                
                # Try to create invite link
                try:
                    # Look for a channel where the bot can create invites
                    invite_channel = None
                    for channel in guild.channels:
                        if (isinstance(channel, discord.TextChannel) and 
                            channel.permissions_for(guild.me).create_instant_invite):
                            invite_channel = channel
                            break
                    
                    if invite_channel:
                        invite = await invite_channel.create_invite(max_age=0, max_uses=0)
                        invite_link = invite.url
                    else:
                        invite_link = "No permission to create invite"
                except Exception as e:
                    invite_link = f"Error: {str(e)[:20]}..."
                
                # Format server info with compact format
                server_info = f"**{i}.** {guild.name} ({guild.member_count:,})\n"
                server_info += f"👑 {owner_name} | 📅 {guild.me.joined_at.strftime('%Y-%m-%d') if guild.me.joined_at else 'Unknown'}\n"
                server_info += f"🔗 {invite_link}\n"
                server_info += "─" * 25 + "\n"
                
                server_list += server_info
                total_members += guild.member_count
                
                # Split into multiple embeds if too long (Discord field limit is 1024 characters)
                if len(server_list) > 800:
                    embed.add_field(
                        name="📋 Server List (Part 1)",
                        value=server_list,
                        inline=False
                    )
                    
                    # Create new embed for remaining servers
                    embed2 = discord.Embed(
                        title="🏠 Bot Server List (Continued)",
                        color=discord.Color.blue()
                    )
                    
                    # Continue with remaining servers
                    remaining_list = ""
                    for j, remaining_guild in enumerate(guilds[i:], i+1):
                        owner = remaining_guild.owner
                        owner_mention = owner.mention if owner else "Unknown"
                        owner_name = owner.display_name if owner else "Unknown"
                        
                        try:
                            invite_channel = None
                            for channel in remaining_guild.channels:
                                if (isinstance(channel, discord.TextChannel) and 
                                    channel.permissions_for(remaining_guild.me).create_instant_invite):
                                    invite_channel = channel
                                    break
                            
                            if invite_channel:
                                invite = await invite_channel.create_invite(max_age=0, max_uses=0)
                                invite_link = invite.url
                            else:
                                invite_link = "No permission to create invite"
                        except Exception as e:
                            invite_link = f"Error: {str(e)[:20]}..."
                        
                        remaining_info = f"**{j}.** {remaining_guild.name} ({remaining_guild.member_count:,})\n"
                        remaining_info += f"👑 {owner_name} | 📅 {remaining_guild.me.joined_at.strftime('%Y-%m-%d') if remaining_guild.me.joined_at else 'Unknown'}\n"
                        remaining_info += f"🔗 {invite_link}\n"
                        remaining_info += "─" * 25 + "\n"
                        
                        remaining_list += remaining_info
                    
                    embed2.add_field(
                        name="📋 Server List (Part 2)",
                        value=remaining_list,
                        inline=False
                    )
                    
                    embed2.add_field(
                        name="📊 Summary",
                        value=f"**Total Servers**: {len(self.bot.guilds)}\n**Total Members**: {total_members:,}",
                        inline=False
                    )
                    
                    embed2.set_footer(text="Server list generated by bot owner")
                    
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    await interaction.followup.send(embed=embed2, ephemeral=True)
                    return
            
            # If we didn't need to split, add the server list to the original embed
            embed.add_field(
                name="📋 Server List",
                value=server_list,
                inline=False
            )
            
            embed.add_field(
                name="📊 Summary",
                value=f"**Total Servers**: {len(self.bot.guilds)}\n**Total Members**: {total_members:,}",
                inline=False
            )
            
            embed.set_footer(text="Server list generated by bot owner")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"An error occurred while generating the server list: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
    
    @app_commands.command(name="refresh", description="Refresh slash commands (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def refresh(self, interaction: discord.Interaction):
        """Command to manually refresh slash commands."""
        try:
            # Defer the response first to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            # Sync commands
            synced = await self.bot.tree.sync()
            
            embed = discord.Embed(
                title="✅ Commands Refreshed",
                description=f"Successfully synced {len(synced)} slash command(s)",
                color=discord.Color.green()
            )
            
            # List all available commands
            all_commands = []
            for cmd in self.bot.tree.get_commands():
                all_commands.append(f"`/{cmd.name}`")
            
            embed.add_field(
                name="📋 Available Commands",
                value=", ".join(all_commands),
                inline=False
            )
            
            embed.set_footer(text="Commands are now available in Discord!")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            try:
                embed = discord.Embed(
                    title="❌ Refresh Failed",
                    description=f"Error refreshing commands: {str(e)}",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                # If followup also fails, try to send a simple message
                try:
                    await interaction.followup.send("❌ Failed to refresh commands. Please try again later.", ephemeral=True)
                except:
                    pass  # If all else fails, just log the error

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Utility(bot)) 