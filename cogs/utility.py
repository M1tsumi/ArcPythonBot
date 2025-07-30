"""
Utility commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from config.settings import DISCLAIMER, BOT_NAME, BOT_VERSION, BOT_DESCRIPTION

class Utility(commands.Cog):
    """Utility commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        
        # Command help data
        self.commands_data = [
            {
                "name": "ping",
                "description": "Check bot latency",
                "usage": "!ping"
            },
            {
                "name": "help",
                "description": "Show this help message",
                "usage": "!help [command]"
            },
            {
                "name": "about",
                "description": "Show information about the bot",
                "usage": "!about"
            },
            {
                "name": "server",
                "description": "Get Discord server invite link",
                "usage": "!server"
            },
            {
                "name": "support",
                "description": "Show support information",
                "usage": "!support"
            },
            {
                "name": "characters",
                "description": "List all available characters",
                "usage": "!characters"
            },
            {
                "name": "character",
                "description": "Get information about a specific character",
                "usage": "!character <name>"
            },
            {
                "name": "character_skills",
                "description": "Show skills for a specific character",
                "usage": "!character_skills <name>"
            },
            {
                "name": "character_talent",
                "description": "Show talent tree for a specific character",
                "usage": "!character_talent <name>"
            },
            {
                "name": "talent_trees",
                "description": "List all available talent trees by type",
                "usage": "!talent_trees"
            },
            {
                "name": "events",
                "description": "List current and upcoming events",
                "usage": "!events [current/past]"
            },
            {
                "name": "event_details",
                "description": "Get detailed information about a specific event",
                "usage": "!event_details <name>"
            }
        ]
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)
        
        embed = EmbedGenerator.create_embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="help")
    async def help_command(self, ctx, command_name: Optional[str] = None):
        """Show help information for commands."""
        if command_name:
            # Show help for specific command
            command = discord.utils.get(self.bot.commands, name=command_name)
            if command:
                embed = EmbedGenerator.create_embed(
                    title=f"Help: !{command.name}",
                    description=command.help or "No description available.",
                    color=discord.Color.blue()
                )
                
                # Add usage information
                if command.usage:
                    embed.add_field(name="Usage", value=f"`{command.usage}`", inline=False)
                else:
                    embed.add_field(name="Usage", value=f"`!{command.name}`", inline=False)
                
                # Add cooldown information
                if hasattr(command, '_buckets') and command._buckets:
                    cooldown = command._buckets._cooldown
                    embed.add_field(name="Cooldown", value=f"{cooldown.per} seconds", inline=True)
                
            else:
                embed = EmbedGenerator.create_error_embed(f"Command `{command_name}` not found.")
        else:
            # Show general help
            embed = EmbedGenerator.create_help_embed(self.commands_data)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="about")
    async def about(self, ctx):
        """Show information about the bot."""
        embed = EmbedGenerator.create_embed(
            title=f"About {BOT_NAME}",
            description=BOT_DESCRIPTION,
            color=discord.Color.purple()
        )
        
        # Add bot information
        embed.add_field(
            name="Version",
            value=BOT_VERSION,
            inline=True
        )
        
        embed.add_field(
            name="Server Count",
            value=f"{len(self.bot.guilds)} servers",
            inline=True
        )
        
        embed.add_field(
            name="User Count",
            value=f"{len(self.bot.users)} users",
            inline=True
        )
        
        # Add disclaimer
        embed.add_field(
            name="Important Notice",
            value=DISCLAIMER,
            inline=False
        )
        
        # Add developer information
        embed.add_field(
            name="Developer",
            value="This bot was created as a demonstration of programming skills and is not affiliated with any game developers.",
            inline=False
        )
        
        embed.set_footer(text="Made with ❤️ for the Avatar Realms Collide community")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="info")
    async def info(self, ctx):
        """Show technical information about the bot."""
        embed = EmbedGenerator.create_embed(
            title="Bot Information",
            description="Technical details about the bot",
            color=discord.Color.blue()
        )
        
        # System information
        embed.add_field(
            name="Python Version",
            value=f"{discord.__version__}",
            inline=True
        )
        
        embed.add_field(
            name="Discord.py Version",
            value=discord.__version__,
            inline=True
        )
        
        embed.add_field(
            name="Uptime",
            value="Calculating...",  # You could add uptime tracking here
            inline=True
        )
        
        # Memory usage (if available)
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            embed.add_field(
                name="Memory Usage",
                value=f"{memory_mb:.1f} MB",
                inline=True
            )
        except ImportError:
            embed.add_field(
                name="Memory Usage",
                value="Not available",
                inline=True
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="invite")
    async def invite(self, ctx):
        """Get the bot's invite link."""
        embed = EmbedGenerator.create_embed(
            title="Invite Link",
            description="Click the link below to invite this bot to your server!",
            color=discord.Color.green()
        )
        
        # Generate invite link (you'll need to replace with your bot's client ID)
        client_id = self.bot.user.id
        invite_link = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot"
        
        embed.add_field(
            name="Invite Link",
            value=f"[Click here to invite the bot]({invite_link})",
            inline=False
        )
        
        embed.add_field(
            name="Required Permissions",
            value="• Send Messages\n• Embed Links\n• Read Message History\n• Use Slash Commands",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="support")
    async def support(self, ctx):
        """Show support information."""
        embed = EmbedGenerator.create_embed(
            title="🆘 Support",
            description="Need help with the bot? Here's how to get support:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Discord Server",
            value="[Join our community server!](https://discord.gg/a3tGyAwVRc)\nGet help, report bugs, and chat with other users.",
            inline=False
        )
        
        embed.add_field(
            name="GitHub Issues",
            value="Report bugs or request features on our GitHub repository.",
            inline=False
        )
        
        embed.add_field(
            name="Commands",
            value="Use `!help` to see all available commands\nUse `!help <command>` for detailed command information",
            inline=False
        )
        
        embed.add_field(
            name="Bot Status",
            value=f"**Version**: {BOT_VERSION} (Beta)\n**Status**: Online and ready to help!",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name="server")
    async def server(self, ctx):
        """Get the Discord server invite link."""
        embed = EmbedGenerator.create_embed(
            title="🎮 Join Our Community!",
            description="Connect with other Avatar Realms Collide players and get bot support.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Discord Server",
            value="[Click here to join!](https://discord.gg/a3tGyAwVRc)",
            inline=False
        )
        
        embed.add_field(
            name="What you'll find:",
            value="• Bot support and help\n• Game discussions\n• Character builds and strategies\n• Event coordination\n• Community features",
            inline=False
        )
        
        embed.add_field(
            name="Bot Features",
            value="• Character information and talent trees\n• Event tracking and notifications\n• User profiles and preferences\n• Search and comparison tools",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Utility(bot)) 