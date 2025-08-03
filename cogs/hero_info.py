"""
Hero Information command module for Avatar Realms Collide Discord Bot.
Provides comprehensive information about heroes, their rarity, and unlock methods.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional

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
    
    @app_commands.command(name="hero_info", description="Hero information and unlock methods")
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
        embed = discord.Embed(
            title="🏆 Hero Information & Unlock Methods",
            description="Complete guide to all heroes and how to obtain their shards",
            color=discord.Color.gold()
        )
        
        # Count heroes by rarity
        legendary_count = len(self.hero_data["legendary"])
        epic_count = len(self.hero_data["epic"])
        rare_count = len(self.hero_data["rare"])
        future_count = len(self.hero_data["future"])
        
        embed.add_field(
            name="📊 Hero Statistics",
            value=f"• **🟠 Legendary Heroes**: {legendary_count}\n• **🟣 Epic Heroes**: {epic_count}\n• **🔵 Rare Heroes**: {rare_count}\n• **⚪ Future Heroes**: {future_count}",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Quick Commands",
            value="• `/hero_info legendary` - Legendary heroes\n• `/hero_info epic` - Epic heroes\n• `/hero_info rare` - Rare heroes\n• `/hero_info future` - Future heroes\n• `/hero_info sources` - Unlock methods",
            inline=False
        )
        
        embed.add_field(
            name="💡 Tips",
            value="• Focus on starter heroes first (Sokka, Katara, Toph, Zuko, Tenzin)\n• Legendary heroes require specific events and sources\n• Daily Deals and The Greatest Leader are key for legendaries\n• Use `/hero_search <name>` to find specific heroes",
            inline=False
        )
        
        embed.set_footer(text="Use specific commands for detailed information about each rarity tier!")
        await interaction.response.send_message(embed=embed)
    
    async def show_legendary_heroes(self, interaction: discord.Interaction):
        """Show legendary heroes information."""
        embed = discord.Embed(
            title="🟠 Legendary Heroes",
            description="The most powerful heroes in the game",
            color=discord.Color.orange()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["legendary"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(
            name="🏆 Legendary Heroes & Sources",
            value=heroes_text,
            inline=False
        )
        
        embed.add_field(
            name="💡 Legendary Tips",
            value="• **Hall of Avatars**: Aang, Korra\n• **Daily Deals**: Most legendaries\n• **The Greatest Leader**: Event rewards\n• **Wheel of Fate**: King Bumi, Lin Beifong, Painted Lady Katara\n• **VIP/Top Up**: Azula, premium sources",
            inline=False
        )
        
        embed.set_footer(text="Legendary heroes are the most powerful but hardest to obtain!")
        await interaction.response.send_message(embed=embed)
    
    async def show_epic_heroes(self, interaction: discord.Interaction):
        """Show epic heroes information."""
        embed = discord.Embed(
            title="🟣 Epic Heroes",
            description="Strong heroes with various unlock methods",
            color=discord.Color.purple()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["epic"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(
            name="⚔️ Epic Heroes & Sources",
            value=heroes_text,
            inline=False
        )
        
        embed.add_field(
            name="💡 Epic Tips",
            value="• **Starter Heroes**: Sokka (first), Katara (Water), Toph (Earth), Zuko (Fire), Tenzin (Air)\n• **Scrolls**: Most epics available through scrolls\n• **Avatar Day Exchange**: Katara, Tenzin, Toph, Zuko\n• **Events**: Borte's Scheme, Rookie Leader Event",
            inline=False
        )
        
        embed.set_footer(text="Epic heroes are great for building strong teams!")
        await interaction.response.send_message(embed=embed)
    
    async def show_rare_heroes(self, interaction: discord.Interaction):
        """Show rare heroes information."""
        embed = discord.Embed(
            title="🔵 Rare Heroes",
            description="Solid heroes available through Silver Scrolls",
            color=discord.Color.blue()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["rare"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(
            name="📚 Rare Heroes & Sources",
            value=heroes_text,
            inline=False
        )
        
        embed.add_field(
            name="💡 Rare Tips",
            value="• **Silver Scrolls**: All rare heroes available\n• **Easy to Obtain**: Great for new players\n• **Good Support**: Useful for team composition\n• **Affordable**: Lower resource requirements",
            inline=False
        )
        
        embed.set_footer(text="Rare heroes are perfect for new players and team building!")
        await interaction.response.send_message(embed=embed)
    
    async def show_future_heroes(self, interaction: discord.Interaction):
        """Show future heroes information."""
        embed = discord.Embed(
            title="⚪ Future Heroes",
            description="Confirmed heroes coming in future updates",
            color=discord.Color.light_grey()
        )
        
        heroes_text = ""
        for hero_name, hero_info in self.hero_data["future"].items():
            sources = ", ".join(hero_info["sources"])
            heroes_text += f"• **{hero_name}**: {sources}\n"
        
        embed.add_field(
            name="🔮 Future Heroes",
            value=heroes_text,
            inline=False
        )
        
        embed.add_field(
            name="💡 Future Tips",
            value="• **Confirmed**: These heroes are officially announced\n• **Save Resources**: Prepare for their release\n• **Stay Updated**: Follow official announcements\n• **Plan Ahead**: Consider team compositions",
            inline=False
        )
        
        embed.set_footer(text="Future heroes are confirmed but not yet available!")
        await interaction.response.send_message(embed=embed)
    
    async def show_unlock_sources(self, interaction: discord.Interaction):
        """Show all unlock sources and methods."""
        embed = discord.Embed(
            title="🎯 Hero Unlock Sources",
            description="Complete guide to all hero unlock methods",
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
        
        embed.set_footer(text="Focus on available sources for your target heroes!")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="hero_search", description="Search for specific hero information")
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
        
        embed = discord.Embed(
            title=f"🏆 {found_hero}",
            description=hero_info["description"],
            color=rarity_colors.get(found_rarity, discord.Color.default())
        )
        
        embed.add_field(
            name="📊 Rarity",
            value=f"**{found_rarity.title()}**",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Unlock Sources",
            value=", ".join(hero_info["sources"]),
            inline=False
        )
        
        # Add rarity-specific tips
        if found_rarity == "legendary":
            embed.add_field(
                name="💡 Legendary Tips",
                value="• Focus on Daily Deals and events\n• Save resources for these heroes\n• Consider VIP/Top Up for Azula\n• Hall of Avatars for Aang/Korra",
                inline=False
            )
        elif found_rarity == "epic":
            embed.add_field(
                name="💡 Epic Tips",
                value="• Available through scrolls and events\n• Good balance of power and accessibility\n• Great for team building\n• Focus on starter heroes first",
                inline=False
            )
        elif found_rarity == "rare":
            embed.add_field(
                name="💡 Rare Tips",
                value="• Easy to obtain through Silver Scrolls\n• Perfect for new players\n• Good support heroes\n• Affordable resource requirements",
                inline=False
            )
        elif found_rarity == "future":
            embed.add_field(
                name="💡 Future Tips",
                value="• Not yet available in the game\n• Save resources for their release\n• Stay updated on announcements\n• Plan team compositions ahead",
                inline=False
            )
        
        embed.set_footer(text=f"Use `/hero_info {found_rarity}` to see all {found_rarity} heroes!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(HeroInfoSystem(bot)) 