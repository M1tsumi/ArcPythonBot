"""
Troops command cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES
from pathlib import Path

class TroopsView(discord.ui.View):
    """View for selecting troops with element and tier selection."""
    
    def __init__(self, data_parser: DataParser):
        super().__init__(timeout=60)
        self.data_parser = data_parser
        self.selected_element = None
        
    @discord.ui.button(label="Water", style=discord.ButtonStyle.primary, emoji="💧", custom_id="water")
    async def water_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.select_element(interaction, "Water")
        
    @discord.ui.button(label="Earth", style=discord.ButtonStyle.success, emoji="🌍", custom_id="earth")
    async def earth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.select_element(interaction, "Earth")
        
    @discord.ui.button(label="Fire", style=discord.ButtonStyle.danger, emoji="🔥", custom_id="fire")
    async def fire_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.select_element(interaction, "Fire")
        
    @discord.ui.button(label="Air", style=discord.ButtonStyle.secondary, emoji="💨", custom_id="air")
    async def air_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.select_element(interaction, "Air")
        
    async def select_element(self, interaction: discord.Interaction, element: str):
        """Handle element selection and show tier options."""
        self.selected_element = element
        
        # Create tier selection view
        tier_view = TroopTierView(self.data_parser, element)
        
        embed = discord.Embed(
            title=f"🎖️ {element} Troops",
            description=f"Choose a tier to view detailed troop information:",
            color=self.get_element_color(element)
        )
        
        # Add element-specific description
        element_descriptions = {
            "Water": "💧 **Water troops** are versatile and balanced, excelling in both offense and defense.",
            "Earth": "🌍 **Earth troops** are defensive specialists with high durability and protection.",
            "Fire": "🔥 **Fire troops** are aggressive attackers with high damage output and speed.",
            "Air": "💨 **Air troops** are swift and agile, focusing on mobility and tactical advantages."
        }
        
        embed.add_field(
            name="Element Overview",
            value=element_descriptions.get(element, ""),
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=tier_view)

    def get_element_color(self, element: str) -> discord.Color:
        """Get color based on element."""
        colors = {
            "Water": discord.Color.from_rgb(0, 150, 255),  # Bright blue
            "Earth": discord.Color.from_rgb(34, 139, 34),   # Forest green
            "Fire": discord.Color.from_rgb(255, 69, 0),     # Red-orange
            "Air": discord.Color.from_rgb(176, 196, 222)    # Light steel blue
        }
        return colors.get(element, discord.Color.default())

class TroopTierView(discord.ui.View):
    """View for selecting troop tiers."""
    
    def __init__(self, data_parser: DataParser, element: str):
        super().__init__(timeout=60)
        self.data_parser = data_parser
        self.element = element
        
        # Add tier buttons (T1-T6) with better styling
        tier_colors = [
            discord.ButtonStyle.secondary,  # T1 - Gray
            discord.ButtonStyle.primary,    # T2 - Blue
            discord.ButtonStyle.success,    # T3 - Green
            discord.ButtonStyle.danger,     # T4 - Red
            discord.ButtonStyle.primary,    # T5 - Blue
            discord.ButtonStyle.success     # T6 - Green
        ]
        
        for tier in range(1, 7):
            tier_str = f"T{tier}"
            button = discord.ui.Button(
                label=f"Tier {tier}",
                style=tier_colors[tier-1],
                custom_id=f"tier_{tier}",
                emoji="⚔️"
            )
            button.callback = self.create_tier_callback(tier_str)
            self.add_item(button)
            
    def create_tier_callback(self, tier: str):
        """Create a callback function for a tier button."""
        async def callback(interaction: discord.Interaction):
            await self.show_troop_info(interaction, tier)
        return callback
        
    async def show_troop_info(self, interaction: discord.Interaction, tier: str):
        """Show troop information for the selected tier."""
        troops_data = self.data_parser.get_troops_data()
        
        if self.element not in troops_data or tier not in troops_data[self.element]:
            embed = discord.Embed(
                title="❌ Troop Not Found",
                description=f"Sorry! No data found for {self.element} {tier} troops.",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        troop_data = troops_data[self.element][tier]
        
        # Create troop information embed with better design
        embed = discord.Embed(
            title=f"🎖️ {self.element} {tier} Troops",
            description=f"**{troop_data['unit_name']}** - {self.get_troop_description(tier)}",
            color=self.get_element_color(self.element)
        )
        
        # Add troop overview
        embed.add_field(
            name="📋 Troop Overview",
            value=self.get_troop_overview(tier),
            inline=False
        )
        
        # Recruitment costs with better formatting
        rec_costs = troop_data['recruitment_costs']
        rec_text = self.format_costs(rec_costs, "Recruitment")
        
        embed.add_field(
            name="⚔️ Recruitment Costs",
            value=rec_text,
            inline=True
        )
        

        
        # Stats with better formatting
        stats_text = self.format_stats(troop_data)
        
        embed.add_field(
            name="📊 Combat Statistics",
            value=stats_text,
            inline=False
        )
        
        embed.set_footer(text=f"🎖️ {self.element} {tier} • {troop_data['unit_name']}")
        
        # Add back button with better styling
        back_view = TroopsView(self.data_parser)
        await interaction.response.edit_message(embed=embed, view=back_view)
    
    def get_troop_description(self, tier: str) -> str:
        """Get description for troop tier."""
        descriptions = {
            "T1": "Basic infantry units - the foundation of your army",
            "T2": "Skilled warriors - improved combat capabilities",
            "T3": "Veteran soldiers - experienced and reliable",
            "T4": "Elite forces - highly trained specialists",
            "T5": "Master warriors - the pinnacle of conventional troops",
            "T6": "Legendary units - the most powerful troops available"
        }
        return descriptions.get(tier, "A formidable fighting force")
    
    def get_troop_overview(self, tier: str) -> str:
        """Get overview for troop tier."""
        overviews = {
            "T1": "🔰 **Basic Training** - Essential for any army",
            "T2": "⚔️ **Combat Ready** - Improved weapons and armor",
            "T3": "🛡️ **Battle Hardened** - Experienced in warfare",
            "T4": "🎖️ **Elite Status** - Specialized training and equipment",
            "T5": "👑 **Master Class** - Peak performance and skill",
            "T6": "🌟 **Legendary** - The ultimate fighting force"
        }
        return overviews.get(tier, "A powerful military unit")
    
    def format_costs(self, costs: dict, cost_type: str) -> str:
        """Format costs in a clean, readable way."""
        text = ""
        
        # Food and Wood (always present)
        text += f"🍖 **{costs['food']:,}** Food\n"
        text += f"🪵 **{costs['wood']:,}** Wood\n"
        
        # Stone (if present)
        if costs['stone'] > 0:
            text += f"🪨 **{costs['stone']:,}** Stone\n"
        
        # Gold (if present)
        if costs['gold'] > 0:
            text += f"💰 **{costs['gold']:,}** Gold\n"
        
        # Time
        text += f"⏱️ **{costs['time']}**"
        
        return text
    
    def format_stats(self, troop_data: dict) -> str:
        """Format stats in a clean, readable way."""
        stats = troop_data
        
        # Calculate power level for visual indicator
        power_level = "⚡" * min(stats['power'] // 20, 5)  # Max 5 stars
        
        text = f"{power_level} **Power Level {stats['power']:,}**\n\n"
        text += f"⚔️ **Attack**: {stats['atk']:,}\n"
        text += f"🛡️ **Defense**: {stats['def']:,}\n"
        text += f"❤️ **Health**: {stats['health']:,}\n"
        text += f"🏃 **Speed**: {stats['speed']:,}\n"
        text += f"📦 **Load**: {stats['load']:,}\n"
        text += f"📈 **Power Diff**: +{stats['power_diff']:,}"
        
        return text

    def get_element_color(self, element: str) -> discord.Color:
        """Get color based on element."""
        colors = {
            "Water": discord.Color.blue(),
            "Earth": discord.Color.green(),
            "Fire": discord.Color.red(),
            "Air": discord.Color.light_grey()
        }
        return colors.get(element, discord.Color.default())

class Troops(commands.Cog):
    """Troops information commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @commands.hybrid_command(name="troops", description="Show troops information with element and tier selection")
    async def troops_command(self, ctx):
        """Show troops information with element and tier selection."""
        troops_data = self.data_parser.get_troops_data()
        
        if not troops_data:
            embed = EmbedGenerator.create_error_embed("No troops data found. Please check the troops.txt file.")
            await ctx.send(embed=embed)
            return
        
        # Create initial embed with better design
        embed = discord.Embed(
            title="🎖️ Avatar Realms Collide Troops",
            description="Choose your element to explore the diverse troop types available in the game. Each element offers unique strengths and strategies.",
            color=discord.Color.from_rgb(70, 130, 180)  # Steel blue
        )
        
        # Add element descriptions with better formatting
        element_info = {
            "Water": "💧 **Water Troops** - Versatile and balanced, excelling in both offense and defense",
            "Earth": "🌍 **Earth Troops** - Defensive specialists with high durability and protection",
            "Fire": "🔥 **Fire Troops** - Aggressive attackers with high damage output and speed",
            "Air": "💨 **Air Troops** - Swift and agile, focusing on mobility and tactical advantages"
        }
        
        elements_text = ""
        for element in troops_data.keys():
            elements_text += f"{element_info.get(element, f'{self.get_element_emoji(element)} **{element} Troops**')}\n"
        
        embed.add_field(
            name="🌍 Available Elements",
            value=elements_text,
            inline=False
        )
        
        # Add troop tier information
        embed.add_field(
            name="⚔️ Troop Tiers",
            value="**T1-T6** - Each element has 6 tiers of troops, from basic infantry to legendary units. Higher tiers require more resources but offer superior combat capabilities.",
            inline=False
        )
        
        embed.set_footer(text="🎖️ Select an element to view detailed troop information")
        
        # Create view with element buttons
        view = TroopsView(self.data_parser)
        await ctx.send(embed=embed, view=view)
    
    def get_element_emoji(self, element: str) -> str:
        """Get emoji for element."""
        emojis = {
            "Water": "💧",
            "Earth": "🌍",
            "Fire": "🔥",
            "Air": "💨"
        }
        return emojis.get(element, "⚔️")

async def setup(bot):
    """Setup function for the troops cog."""
    await bot.add_cog(Troops(bot)) 