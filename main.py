"""
Avatar Realms Collide Discord Bot
Main entry point for the Discord bot application.

This bot provides information and tools for the Avatar Realms Collide community.
Note: This is an unofficial, fan-made bot and is not affiliated with the game developers.
"""

import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AvatarRealmsBot(commands.Bot):
    """Main bot class with custom functionality."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,  # We'll create a custom help command
            description="Avatar Realms Collide Community Bot"
        )
        
        self.logger = logger
        
    async def setup_hook(self):
        """Setup hook called when the bot is starting up."""
        self.logger.info("Setting up bot...")
        
        # Load all cogs
        cog_files = [
            'cogs.utility',
            'cogs.game_info', 
            'cogs.player_tools',
            'cogs.events',
            'cogs.moderation'
        ]
        
        for cog in cog_files:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                self.logger.error(f"Failed to load cog {cog}: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        self.logger.info(f"Bot is ready! Logged in as {self.user}")
        self.logger.info(f"Bot ID: {self.user.id}")
        self.logger.info(f"Connected to {len(self.guilds)} guilds")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="Avatar Realms Collide"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found",
                description=f"The command `{ctx.invoked_with}` was not found.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Help",
                value="Use `!help` to see all available commands.",
                inline=False
            )
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Argument",
                description=f"You're missing a required argument: `{error.param.name}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
        else:
            self.logger.error(f"Unhandled command error: {error}")
            embed = discord.Embed(
                title="Error",
                description="An unexpected error occurred. Please try again later.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

def main():
    """Main function to run the bot."""
    # Check for required environment variables
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please create a .env file with your Discord bot token.")
        return
    
    # Create and run the bot
    bot = AvatarRealmsBot()
    
    try:
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        logger.error("Failed to login: Invalid token provided.")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    main() 