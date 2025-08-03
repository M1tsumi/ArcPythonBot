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
    
    @commands.command(name="info", description="Get comprehensive bot information and contribution details")
    async def info_prefix(self, ctx):
        """Traditional prefix command to provide comprehensive bot information and contribution details."""
        embed = discord.Embed(
            title="🤖 Avatar Realms Collide Bot Information",
            description="Welcome to the unofficial Avatar Realms Collide community bot! This bot provides comprehensive game tools and information for the community.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎮 Bot Features",
            value="• **Talent Tree Browser** - View all character talent trees\n• **Skill Priorities** - Get optimal skill upgrade orders\n• **Leaderboards** - Track top players and alliances\n• **Town Hall Info** - View upgrade requirements\n• **Hero Rankup Guide** - Complete rankup costs and guide\n• **Event System** - Current and upcoming events\n• **Interactive Commands** - Modern slash command interface",
            inline=False
        )
        
        embed.add_field(
            name="👨‍💻 Developer",
            value="**Developed by Quefep**\nUnofficial fan-made bot for the community",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Want to Contribute?",
            value="We welcome contributions from the community! If you have any information, data, images, or other resources to share, please don't be a stranger and reach out to **quefep** on Discord.",
            inline=False
        )
        
        embed.add_field(
            name="📊 Bot Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}\n• **Uptime**: Online and ready!",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Disclaimer",
            value="This is an unofficial, fan-made Discord bot and is not affiliated with the game developers. All game data used is from publicly available sources.",
            inline=False
        )
        
        embed.set_footer(text="Join our Discord for updates and community support!")
        
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
            description="Welcome to the unofficial Avatar Realms Collide community bot! This bot provides comprehensive game tools and information for the community.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎮 Bot Features",
            value="• **Talent Tree Browser** - View all character talent trees\n• **Skill Priorities** - Get optimal skill upgrade orders\n• **Leaderboards** - Track top players and alliances\n• **Town Hall Info** - View upgrade requirements\n• **Hero Rankup Guide** - Complete rankup costs and guide\n• **Event System** - Current and upcoming events\n• **Rally System** - Create and join Shattered Skulls Fortress rallies\n• **Interactive Commands** - Modern slash command interface",
            inline=False
        )
        
        embed.add_field(
            name="👨‍💻 Developer",
            value="**Developed by Quefep**\nUnofficial fan-made bot for the community",
            inline=False
        )
        
        embed.add_field(
            name="🤝 Want to Contribute?",
            value="We welcome contributions from the community! If you have any information, data, images, or other resources to share, please don't be a stranger and reach out to **quefep** on Discord.",
            inline=False
        )
        
        embed.add_field(
            name="📊 Bot Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}\n• **Uptime**: Online and ready!",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Disclaimer",
            value="This is an unofficial, fan-made Discord bot and is not affiliated with the game developers. All game data used is from publicly available sources.",
            inline=False
        )
        
        embed.set_footer(text="Join our Discord for updates and community support!")
        
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
            name="🤖 Available Commands",
            value="• `/talent_trees` - Browse character talent trees\n• `/skill_priorities` - View hero skill priorities\n• `/leaderboard` - Check top players and alliances\n• `/townhall` - View town hall requirements\n• `/hero_rankup` - View hero rankup guide and costs\n• `/events` - View current and upcoming events\n• `/ping` - Check bot status and latency\n• `/info` - Comprehensive bot information\n• `/links` - Get bot links and information\n• `/addtoserver` - Add bot to your server\n• `/setup` - Setup rally system (Admin)\n• `/rally` - Create a new rally (level + time limit)\n• `/rally_stats` - View your rally statistics\n• `/rally_leaderboard` - View rally leaderboard\n• `/leader` - Admin leaderboard management (pause/resume/clear)",
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