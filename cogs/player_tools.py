"""
Player tools commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from typing import Optional, Dict, Any
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
import json
import os
from pathlib import Path

class PlayerTools(commands.Cog):
    """Player-specific tools and features."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
        
        # Create data directory for user profiles
        self.profiles_dir = Path("data/users/profiles")
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def get_text(self, user_id: int, key: str, **kwargs) -> str:
        """Get translated text for a user using the language system."""
        try:
            # Get the language system cog
            language_cog = self.bot.get_cog('LanguageSystem')
            if language_cog:
                return language_cog.get_text(user_id, key, **kwargs)
            else:
                # Fallback to English if language system not available
                return f"[{key}]"
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
            return f"[Translation error: {key}]"
    
    def _load_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Load user profile from file."""
        profile_file = self.profiles_dir / f"{user_id}.json"
        
        if profile_file.exists():
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading profile for user {user_id}: {e}")
        
        # Return default profile
        return {
            "user_id": user_id,
            "favorite_character": None,
            "server_id": None,
            "preferences": {},
            "created_at": None
        }
    
    def _save_user_profile(self, user_id: int, profile: Dict[str, Any]):
        """Save user profile to file."""
        profile_file = self.profiles_dir / f"{user_id}.json"
        
        try:
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
        except IOError as e:
            self.logger.error(f"Error saving profile for user {user_id}: {e}")
    
    @commands.command(name="myprofile")
    async def my_profile(self, ctx):
        """Show your user profile."""
        user_id = ctx.author.id
        profile = self._load_user_profile(user_id)
        
        embed = EmbedGenerator.create_embed(
            title=f"Profile: {ctx.author.display_name}",
            description="Your personal profile information",
            color=discord.Color.blue()
        )
        
        # Add profile information
        if profile.get('favorite_character'):
            embed.add_field(
                name="Favorite Character",
                value=profile['favorite_character'],
                inline=True
            )
        
        if profile.get('server_id'):
            embed.add_field(
                name="Server ID",
                value=profile['server_id'],
                inline=True
            )
        
        if profile.get('created_at'):
            embed.add_field(
                name="Profile Created",
                value=profile['created_at'],
                inline=True
            )
        
        # Add preferences
        if profile.get('preferences'):
            prefs_text = ""
            for key, value in profile['preferences'].items():
                prefs_text += f"• **{key}**: {value}\n"
            embed.add_field(name="Preferences", value=prefs_text, inline=False)
        
        embed.add_field(
            name="Commands",
            value="Use `!setfavorite <character>` to set your favorite character\n"
                  "Use `!setpreference <key> <value>` to set preferences",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="setfavorite")
    async def set_favorite_character(self, ctx, *, character_name: str):
        """Set your favorite character."""
        # Check if character exists
        character = self.data_parser.get_character(character_name)
        if not character:
            embed = EmbedGenerator.create_error_embed(
                f"Character '{character_name}' not found. Use `!characters` to see available characters."
            )
            await ctx.send(embed=embed)
            return
        
        # Update profile
        user_id = ctx.author.id
        profile = self._load_user_profile(user_id)
        profile['favorite_character'] = character['name']
        profile['user_id'] = user_id
        
        if not profile.get('created_at'):
            profile['created_at'] = str(discord.utils.utcnow())
        
        self._save_user_profile(user_id, profile)
        
        embed = EmbedGenerator.create_success_embed(
            f"Your favorite character has been set to **{character['name']}**!"
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="setpreference")
    async def set_preference(self, ctx, key: str, *, value: str):
        """Set a user preference."""
        if len(key) > 20:
            embed = EmbedGenerator.create_error_embed("Preference key must be 20 characters or less.")
            await ctx.send(embed=embed)
            return
        
        if len(value) > 100:
            embed = EmbedGenerator.create_error_embed("Preference value must be 100 characters or less.")
            await ctx.send(embed=embed)
            return
        
        # Update profile
        user_id = ctx.author.id
        profile = self._load_user_profile(user_id)
        
        if 'preferences' not in profile:
            profile['preferences'] = {}
        
        profile['preferences'][key] = value
        profile['user_id'] = user_id
        
        if not profile.get('created_at'):
            profile['created_at'] = str(discord.utils.utcnow())
        
        self._save_user_profile(user_id, profile)
        
        embed = EmbedGenerator.create_success_embed(
            f"Preference '{key}' has been set to '{value}'!"
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="clearfavorite")
    async def clear_favorite_character(self, ctx):
        """Clear your favorite character."""
        user_id = ctx.author.id
        profile = self._load_user_profile(user_id)
        
        if profile.get('favorite_character'):
            old_favorite = profile['favorite_character']
            profile['favorite_character'] = None
            self._save_user_profile(user_id, profile)
            
            embed = EmbedGenerator.create_success_embed(
                f"Your favorite character '{old_favorite}' has been cleared."
            )
        else:
            embed = EmbedGenerator.create_error_embed("You don't have a favorite character set.")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="clearpreference")
    async def clear_preference(self, ctx, key: str):
        """Clear a specific preference."""
        user_id = ctx.author.id
        profile = self._load_user_profile(user_id)
        
        if profile.get('preferences', {}).get(key):
            del profile['preferences'][key]
            self._save_user_profile(user_id, profile)
            
            embed = EmbedGenerator.create_success_embed(
                f"Preference '{key}' has been cleared."
            )
        else:
            embed = EmbedGenerator.create_error_embed(f"No preference found with key '{key}'.")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, leaderboard_type: Optional[str] = "characters"):
        """Show a leaderboard (placeholder functionality)."""
        embed = EmbedGenerator.create_embed(
            title=f"Leaderboard: {leaderboard_type.title()}",
            description="This is a placeholder leaderboard. In a real implementation, this would show actual game data.",
            color=discord.Color.gold()
        )
        
        # Mock leaderboard data
        if leaderboard_type.lower() == "characters":
            embed.add_field(
                name="Most Popular Characters",
                value="1. **Fire Mage** - 1,234 players\n"
                      "2. **Ice Warrior** - 987 players\n"
                      "3. **Lightning Archer** - 756 players\n"
                      "4. **Earth Guardian** - 543 players\n"
                      "5. **Wind Assassin** - 432 players",
                inline=False
            )
        elif leaderboard_type.lower() == "events":
            embed.add_field(
                name="Event Participation",
                value="1. **Summer Festival** - 2,345 participants\n"
                      "2. **Winter Tournament** - 1,876 participants\n"
                      "3. **Spring Challenge** - 1,543 participants\n"
                      "4. **Autumn Quest** - 1,234 participants\n"
                      "5. **Holiday Special** - 987 participants",
                inline=False
            )
        else:
            embed.add_field(
                name="Available Leaderboards",
                value="• `!leaderboard characters` - Most popular characters\n"
                      "• `!leaderboard events` - Event participation",
                inline=False
            )
        
        embed.add_field(
            name="Note",
            value="This is mock data for demonstration purposes. Real leaderboards would require game API integration.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="stats")
    async def player_stats(self, ctx):
        """Show player statistics (placeholder)."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(ctx.author.id, "player_statistics_title"),
            description=self.get_text(ctx.author.id, "player_statistics_desc"),
            color=discord.Color.blue()
        )
        
        # Mock statistics
        embed.add_field(
            name="Server Statistics",
            value=f"• **Total Members**: {ctx.guild.member_count}\n"
                  f"• **Online Members**: {len([m for m in ctx.guild.members if m.status != discord.Status.offline])}\n"
                  f"• **Bot Commands Used**: 1,234\n"
                  f"• **Most Active Channel**: #general",
            inline=False
        )
        
        embed.add_field(
            name="Bot Usage",
            value="• **Commands Today**: 156\n"
                  "• **Most Used Command**: !character\n"
                  "• **Total Characters Queried**: 2,345\n"
                  "• **Total Events Viewed**: 1,234",
            inline=False
        )
        
        embed.add_field(
            name="Note",
            value="These are mock statistics for demonstration purposes.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="compare")
    async def compare_characters(self, ctx, character1: str, character2: str):
        """Compare two characters."""
        char1 = self.data_parser.get_character(character1)
        char2 = self.data_parser.get_character(character2)
        
        if not char1:
            embed = EmbedGenerator.create_error_embed(
                f"Character '{character1}' not found."
            )
            await ctx.send(embed=embed)
            return
        
        if not char2:
            embed = EmbedGenerator.create_error_embed(
                f"Character '{character2}' not found."
            )
            await ctx.send(embed=embed)
            return
        
        # Create comparison embed
        embed = EmbedGenerator.create_embed(
            title=f"Character Comparison: {char1['name']} vs {char2['name']}",
            description="Comparing character attributes and abilities",
            color=discord.Color.purple()
        )
        
        # Compare basic info
        embed.add_field(
            name=f"{char1['name']}",
            value=f"**Element**: {char1.get('element', 'Unknown')}\n"
                  f"**Weapon**: {char1.get('weapon_type', 'Unknown')}\n"
                  f"**Rarity**: {char1.get('rarity', 'Unknown')}",
            inline=True
        )
        
        embed.add_field(
            name=f"{char2['name']}",
            value=f"**Element**: {char2.get('element', 'Unknown')}\n"
                  f"**Weapon**: {char2.get('weapon_type', 'Unknown')}\n"
                  f"**Rarity**: {char2.get('rarity', 'Unknown')}",
            inline=True
        )
        
        # Compare stats if available
        if 'stats' in char1 and 'stats' in char2:
            stats_text = ""
            for stat in char1['stats']:
                if stat in char2['stats']:
                    val1 = char1['stats'][stat]
                    val2 = char2['stats'][stat]
                    stats_text += f"**{stat.title()}**: {val1} vs {val2}\n"
            
            if stats_text:
                embed.add_field(name="Stats Comparison", value=stats_text, inline=False)
        
        embed.add_field(
            name="More Information",
            value=f"Use `!character {char1['name']}` for detailed info\n"
                  f"Use `!character {char2['name']}` for detailed info",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(PlayerTools(bot)) 