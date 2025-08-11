"""
Hero Information command module for Avatar Realms Collide Discord Bot.
Provides comprehensive information about heroes, their rarity, and unlock methods.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional
from utils.embed_generator import EmbedGenerator

class HeroInfoSystem(commands.Cog):
    """Hero Information command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        
        # Hero Information Data from heroinfo.txt
        self.hero_data = {
            "legendary": {
                "Aang": {
                    "sources": ["Hall of Avatars", "Daily Deals", "The Greatest Leader", "Trail Shop"],
                    "description": "The last Airbender and Avatar of the world"
                },
                "Amon": {
                    "sources": ["Daily Deals", "The Greatest Leader"],
                    "description": "Equalist leader and revolutionary"
                },
                "Azula": {
                    "sources": ["Top Up Rewards", "VIP Chests"],
                    "description": "Firebending prodigy and Fire Nation princess"
                },
                "Bumi": {
                    "sources": ["Expedition", "Golden Scroll", "Login Event", "Trail Shop"],
                    "description": "Eccentric Airbending master and king"
                },
                "King Bumi": {
                    "sources": ["Wheel of Fate"],
                    "description": "Earthbending king and master strategist"
                },
                "Korra": {
                    "sources": ["Hall of Avatars", "Daily Deals", "The Greatest Leader"],
                    "description": "Water Tribe Avatar of the modern era"
                },
                "Kuvira": {
                    "sources": ["Currently unavailable"],
                    "description": "Great Uniter and Metalbending master"
                },
                "Kyoshi": {
                    "sources": ["Daily Deals", "The Greatest Leader"],
                    "description": "Legendary Earth Kingdom Avatar of justice"
                },
                "Lin Beifong": {
                    "sources": ["Wheel of Fate"],
                    "description": "Metalbending police chief and protector"
                },
                "Mako": {
                    "sources": ["Currently unavailable"],
                    "description": "Pro-bending champion and Firebender"
                },
                "Painted Lady Katara": {
                    "sources": ["Wheel of Fate"],
                    "description": "Katara as the mysterious Painted Lady"
                },
                "Roku": {
                    "sources": ["Daily Deals", "The Greatest Leader"],
                    "description": "Fire Nation Avatar of balance and wisdom"
                },
                "Unalaq": {
                    "sources": ["Daily Deals", "Unalaq Pass (26 days after server start)"],
                    "description": "Dark Waterbending master and spiritual leader"
                },
                "Uncle Iroh": {
                    "sources": ["Golden Scroll", "Wheel of Fate"],
                    "description": "Wise Firebending master and Dragon of the West"
                },
                "Yangchen": {
                    "sources": ["Daily Deals", "The Greatest Leader"],
                    "description": "Ancient Air Nomad Avatar of wisdom"
                }
            },
            "epic": {
                "Asami Sato": {
                    "sources": ["Scrolls"],
                    "description": "Genius inventor and Fire Nation engineer"
                },
                "Borte": {
                    "sources": ["Borte's Scheme"],
                    "description": "Water Tribe warrior and fierce protector"
                },
                "Katara": {
                    "sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Water)", "Trail Shop"],
                    "description": "Master Waterbender and skilled healer"
                },
                "Sokka": {
                    "sources": ["First Hero you unlock", "Scrolls"],
                    "description": "Strategic warrior and tactical leader"
                },
                "Suki": {
                    "sources": ["Scrolls", "Rookie Leader Event"],
                    "description": "Kyoshi Warrior leader and skilled fighter"
                },
                "Tenzin": {
                    "sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Air)", "Trail Shop"],
                    "description": "Airbending master and spiritual teacher"
                },
                "Teo": {
                    "sources": ["Expedition", "Scrolls"],
                    "description": "Air Nomad inventor and mechanical genius"
                },
                "Toph": {
                    "sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Earth)", "Trail Shop"],
                    "description": "Blind Earthbending master and Metalbender"
                },
                "Zuko": {
                    "sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Fire)", "Trail Shop"],
                    "description": "Fire Nation prince and Firebending master"
                }
            },
            "rare": {
                "Kuei": {
                    "sources": ["Silver Scroll"],
                    "description": "Earth Kingdom king and diplomatic leader"
                },
                "Meelo": {
                    "sources": ["Silver Scroll"],
                    "description": "Young Airbending prodigy and energetic warrior"
                },
                "Piandao": {
                    "sources": ["Silver Scroll"],
                    "description": "Master swordsman and Fire Nation instructor"
                },
                "Yue": {
                    "sources": ["Silver Scroll"],
                    "description": "Moon spirit and Water Tribe princess"
                }
            },
            "future": {
                "Blue Spirit": {
                    "sources": ["Future Release"],
                    "description": "Mysterious masked warrior"
                },
                "Bolin": {
                    "sources": ["Future Release"],
                    "description": "Pro-bending champion and Earthbender"
                },
                "Jinora": {
                    "sources": ["Future Release"],
                    "description": "Spiritual Airbender and Tenzin's daughter"
                },
                "Melon Lord": {
                    "sources": ["Future Release"],
                    "description": "Mysterious figure from the Avatar universe"
                },
                "Ozai": {
                    "sources": ["Future Release"],
                    "description": "Fire Lord and master Firebender"
                },
                "Sozin": {
                    "sources": ["Future Release"],
                    "description": "Ancient Fire Lord and Firebending master"
                }
            }
        }

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
    
    @app_commands.command(name="hero_info", description="Hero information and unlock methods")
    @app_commands.checks.cooldown(1, 5.0)
    @app_commands.describe(
        type="Information type to view"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="overview", value="overview"),
        app_commands.Choice(name="legendary", value="legendary"),
        app_commands.Choice(name="epic", value="epic"),
        app_commands.Choice(name="rare", value="rare"),
        app_commands.Choice(name="future", value="future"),
        app_commands.Choice(name="sources", value="sources")
    ])
    async def hero_info(self, interaction: discord.Interaction, type: str):
        """Main Hero Information command with organized information."""
        if type == "overview":
            await self.show_hero_overview(interaction)
        elif type == "legendary":
            await self.show_legendary_heroes(interaction)
        elif type == "epic":
            await self.show_epic_heroes(interaction)
        elif type == "rare":
            await self.show_rare_heroes(interaction)
        elif type == "future":
            await self.show_future_heroes(interaction)
        elif type == "sources":
            await self.show_unlock_sources(interaction)
    
    async def show_hero_overview(self, interaction: discord.Interaction):
        """Show hero information overview."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "hero_information_title"),
            description=self.get_text(interaction.user.id, "hero_information_desc"),
            color=discord.Color.gold()
        )
        
        # Count heroes by rarity
        legendary_count = len(self.hero_data["legendary"])
        epic_count = len(self.hero_data["epic"])
        rare_count = len(self.hero_data["rare"])
        future_count = len(self.hero_data["future"])
        
        embed.add_field(
            name=self.get_text(interaction.user.id, "hero_counts"),
            value=(
                f"{self.get_text(interaction.user.id, 'legendary')}: {legendary_count}\n"
                f"{self.get_text(interaction.user.id, 'epic')}: {epic_count}\n"
                f"{self.get_text(interaction.user.id, 'rare')}: {rare_count}\n"
                f"{self.get_text(interaction.user.id, 'future')}: {future_count}"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Quick Commands",
            value=(
                "`/hero_info legendary` • `/hero_info epic` • `/hero_info rare` • `/hero_info future`\n"
                "`/hero_info sources` for unlock methods"
            ),
            inline=False
        )

        embed.add_field(name="Unlock Requirement", value="10 shards (all heroes)", inline=False)
        
        embed.add_field(
            name="Tips",
            value=(
                "Start with accessible heroes (Sokka, Katara, Toph, Zuko, Tenzin).\n"
                "Legendaries usually come from events or shops.\n"
                "Use `/hero_search <name>` for specifics."
            ),
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def show_legendary_heroes(self, interaction: discord.Interaction):
        """Show legendary heroes information."""
        embed = EmbedGenerator.create_embed(
            title="Legendary Heroes",
            description="Top-tier heroes. Unlock requirement: 10 shards.",
            color=discord.Color.orange()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["legendary"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(name="Heroes & Sources", value=heroes_text, inline=False)
        
        embed.add_field(
            name="Notes",
            value=(
                "Common sources: Hall of Avatars, Wheel of Fate, event shops, Daily Deals."),
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def show_epic_heroes(self, interaction: discord.Interaction):
        """Show epic heroes information."""
        embed = EmbedGenerator.create_embed(
            title="Epic Heroes",
            description="Strong heroes with various unlock methods. Unlock requirement: 10 shards.",
            color=discord.Color.purple()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["epic"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(name="Heroes & Sources", value=heroes_text, inline=False)
        
        embed.add_field(
            name="Notes",
            value="Many epics are available via scrolls and exchanges; starter options are solid early picks.",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def show_rare_heroes(self, interaction: discord.Interaction):
        """Show rare heroes information."""
        embed = EmbedGenerator.create_embed(
            title="Rare Heroes",
            description="Accessible heroes typically via Silver Scrolls. Unlock requirement: 10 shards.",
            color=discord.Color.blue()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["rare"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(name="Heroes & Sources", value=heroes_text, inline=False)
        
        embed.add_field(name="Notes", value="Cost-effective choices for early progression.", inline=False)
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def show_future_heroes(self, interaction: discord.Interaction):
        """Show future heroes information."""
        embed = EmbedGenerator.create_embed(
            title="Future Heroes",
            description="Confirmed heroes coming in future updates.",
            color=discord.Color.light_grey()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["future"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(name="Planned", value=heroes_text, inline=False)
        
        embed.add_field(name="Notes", value="Plan resources and teams ahead of release.", inline=False)
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def show_unlock_sources(self, interaction: discord.Interaction):
        """Show all unlock sources and methods."""
        embed = EmbedGenerator.create_embed(
            title="Hero Unlock Sources",
            description="Overview of unlock methods. All heroes require 10 shards to unlock.",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🏛️ Special Sources",
            value="• **Hall of Avatars**: Aang, Korra\n• **Wheel of Fate**: King Bumi, Lin Beifong, Painted Lady Katara\n• **VIP Chests**: Azula\n• **Top Up Rewards**: Azula\n• **Unalaq Pass**: Unalaq (26 days after server start)",
            inline=False
        )
        
        embed.add_field(
            name="📜 Scroll Sources",
            value="• **Golden Scroll**: Bumi, Uncle Iroh\n• **Silver Scroll**: Kuei, Meelo, Piandao, Yue\n• **Regular Scrolls**: Most Epic heroes",
            inline=False
        )
        
        embed.add_field(
            name="🎪 Event Sources",
            value="• **Daily Deals**: Most Legendary heroes\n• **The Greatest Leader**: Aang, Amon, Korra, Kyoshi, Roku, Yangchen\n• **Borte's Scheme**: Borte\n• **Rookie Leader Event**: Suki\n• **Avatar Day Exchange**: Katara, Tenzin, Toph, Zuko",
            inline=False
        )
        
        embed.add_field(
            name="🎁 Other Sources",
            value="• **Expedition**: Bumi, Teo\n• **Login Event**: Bumi\n• **Trail Shop**: Aang, Bumi, Katara, Tenzin, Toph, Zuko\n• **Starter Heroes**: Sokka (first), Katara (Water), Toph (Earth), Zuko (Fire), Tenzin (Air)",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="hero_search", description="Search for specific hero information")
    @app_commands.checks.cooldown(1, 5.0)
    @app_commands.describe(
        hero_name="Name of the hero to search for"
    )
    async def hero_search(self, interaction: discord.Interaction, hero_name: str):
        """Search for specific hero information."""
        hero_name_lower = hero_name.lower()
        found_hero = None
        found_rarity = None
        
        # Search through all rarities
        for rarity, heroes in self.hero_data.items():
            for hero, info in heroes.items():
                if hero.lower() == hero_name_lower:
                    found_hero = hero
                    found_rarity = rarity
                    break
            if found_hero:
                break
        
        if not found_hero:
            # Try partial matching
            for rarity, heroes in self.hero_data.items():
                for hero, info in heroes.items():
                    if hero_name_lower in hero.lower():
                        found_hero = hero
                        found_rarity = rarity
                        break
                if found_hero:
                    break
        
        if not found_hero:
            embed = discord.Embed(
                title="❌ Hero Not Found",
                description=f"Could not find hero '{hero_name}'. Use `/hero_info overview` to see all available heroes.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Create hero info embed
        hero_info = self.hero_data[found_rarity][found_hero]
        rarity_colors = {
            "legendary": discord.Color.orange(),
            "epic": discord.Color.purple(),
            "rare": discord.Color.blue(),
            "future": discord.Color.light_grey()
        }
        
        embed = EmbedGenerator.create_embed(
            title=f"{found_hero}",
            description=hero_info["description"],
            color=rarity_colors.get(found_rarity, discord.Color.default())
        )
        
        embed.add_field(name="Rarity", value=f"{found_rarity.title()}", inline=True)
        
        embed.add_field(name="Unlock Sources", value=", ".join(hero_info["sources"]), inline=False)
        embed.add_field(name="Unlock Requirement", value="10 shards", inline=True)
        
        # Add rarity-specific tips
        if found_rarity == "legendary":
            embed.add_field(name="Notes", value="Commonly via events or shops.", inline=False)
        elif found_rarity == "epic":
            embed.add_field(name="Notes", value="Often available via scrolls and exchanges.", inline=False)
        elif found_rarity == "rare":
            embed.add_field(name="Notes", value="Accessible and cost-effective.", inline=False)
        elif found_rarity == "future":
            embed.add_field(name="Notes", value="Not yet available; plan ahead.", inline=False)
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(HeroInfoSystem(bot)) 