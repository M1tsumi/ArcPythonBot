"""
Test script to check bot commands
"""

import discord
from discord.ext import commands
import asyncio

class TestBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Load the troop calculator cog and check commands."""
        try:
            await self.load_extension('cogs.troop_calculator')
            print("✅ Troop calculator cog loaded successfully")
            
            # Check what commands are registered
            print("\n📋 Registered commands:")
            for cmd in self.tree.get_commands():
                print(f"  - {cmd.name}: {cmd.description}")
            
            print(f"\n📊 Total commands: {len(self.tree.get_commands())}")
            
        except Exception as e:
            print(f"❌ Error loading cog: {e}")

async def main():
    bot = TestBot()
    await bot.start('your_token_here')  # Replace with actual token

if __name__ == "__main__":
    asyncio.run(main()) 