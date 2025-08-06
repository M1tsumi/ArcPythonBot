"""
Troop Calculator Cog
Provides tools to calculate troop recruitment costs and requirements.
"""

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Select
import asyncio
from typing import Dict, List, Optional, Tuple
from utils.data_parser import DataParser
import re

class TroopCalculatorView(View):
    """Interactive view for troop calculator."""
    
    def __init__(self, data_parser: DataParser):
        super().__init__(timeout=300)
        self.data_parser = data_parser
        self.troops_data = data_parser.get_troops_data()
        self.selected_element = None
        self.selected_tier = None
        self.quantity = 1
        
    @discord.ui.select(
        placeholder="Choose an element...",
        options=[
            discord.SelectOption(label="💧 Water", value="Water", emoji="💧"),
            discord.SelectOption(label="🌍 Earth", value="Earth", emoji="🌍"),
            discord.SelectOption(label="🔥 Fire", value="Fire", emoji="🔥"),
            discord.SelectOption(label="💨 Air", value="Air", emoji="💨")
        ]
    )
    async def element_select(self, interaction: discord.Interaction, select: Select):
        """Handle element selection."""
        self.selected_element = select.values[0]
        self.selected_tier = None
        
        # Update tier options based on selected element
        tier_options = []
        if self.selected_element in self.troops_data:
            for tier in self.troops_data[self.selected_element].keys():
                troop = self.troops_data[self.selected_element][tier]
                tier_options.append(
                    discord.SelectOption(
                        label=f"{tier} - {troop['unit_name']}",
                        value=tier,
                        description=f"Power: {troop['power']} | ATK: {troop['atk']} | DEF: {troop['def']}"
                    )
                )
        
        # Create new tier select
        tier_select = Select(
            placeholder=f"Choose a {self.selected_element} tier...",
            options=tier_options
        )
        
        # Replace the tier select in the view
        for child in self.children:
            if isinstance(child, Select) and child.placeholder and "tier" in child.placeholder:
                self.remove_item(child)
                break
        
        tier_select.callback = self.tier_select_callback
        self.add_item(tier_select)
        
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def tier_select_callback(self, interaction: discord.Interaction):
        """Handle tier selection."""
        self.selected_tier = interaction.data["values"][0]
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="➕ Increase Quantity", style=discord.ButtonStyle.primary, emoji="➕")
    async def increase_quantity(self, interaction: discord.Interaction, button: Button):
        """Increase troop quantity."""
        self.quantity = min(self.quantity + 1, 10000)
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="➖ Decrease Quantity", style=discord.ButtonStyle.secondary, emoji="➖")
    async def decrease_quantity(self, interaction: discord.Interaction, button: Button):
        """Decrease troop quantity."""
        self.quantity = max(self.quantity - 1, 1)
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔢 Set Quantity", style=discord.ButtonStyle.success, emoji="🔢")
    async def set_quantity(self, interaction: discord.Interaction, button: Button):
        """Set custom quantity."""
        await interaction.response.send_modal(QuantityModal(self))
    
    def create_calculator_embed(self) -> discord.Embed:
        """Create the calculator embed."""
        embed = discord.Embed(
            title="⚔️ Troop Calculator",
            description="Calculate recruitment costs for troops",
            color=discord.Color.blue()
        )
        
        if not self.selected_element:
            embed.add_field(
                name="📋 Instructions",
                value="1. Select an element (Water, Earth, Fire, Air)\n"
                      "2. Choose a tier (T1-T6)\n"
                      "3. Adjust quantity as needed\n"
                      "4. View calculated costs below",
                inline=False
            )
            return embed
        
        if not self.selected_tier:
            embed.add_field(
                name=f"Selected Element: {self.selected_element}",
                value="Please select a tier to continue...",
                inline=False
            )
            return embed
        
        # Get troop data
        troop = self.troops_data[self.selected_element][self.selected_tier]
        costs = troop['recruitment_costs']
        
        # Calculate total costs
        total_food = costs['food'] * self.quantity
        total_wood = costs['wood'] * self.quantity
        total_stone = costs['stone'] * self.quantity
        total_gold = costs['gold'] * self.quantity
        
        # Format costs
        cost_text = f"**Food**: {total_food:,}\n"
        cost_text += f"**Wood**: {total_wood:,}\n"
        if total_stone > 0:
            cost_text += f"**Stone**: {total_stone:,}\n"
        if total_gold > 0:
            cost_text += f"**Gold**: {total_gold:,}\n"
        
        # Calculate total time
        time_per_unit = self.parse_time(costs['time'])
        total_seconds = time_per_unit * self.quantity
        total_time = self.format_time(total_seconds)
        
        cost_text += f"**Time**: {total_time}"
        
        embed.add_field(
            name=f"📊 {self.selected_tier} {troop['unit_name']} ({self.selected_element})",
            value=f"**Quantity**: {self.quantity:,}\n"
                  f"**Power**: {troop['power']}\n"
                  f"**ATK**: {troop['atk']}\n"
                  f"**DEF**: {troop['def']}\n"
                  f"**Health**: {troop['health']}\n"
                  f"**Speed**: {troop['speed']}\n"
                  f"**Load**: {troop['load']}",
            inline=True
        )
        
        embed.add_field(
            name="💰 Total Costs",
            value=cost_text,
            inline=True
        )
        
        # Add per-unit costs
        per_unit_text = f"**Food**: {costs['food']:,}\n"
        per_unit_text += f"**Wood**: {costs['wood']:,}\n"
        if costs['stone'] > 0:
            per_unit_text += f"**Stone**: {costs['stone']:,}\n"
        if costs['gold'] > 0:
            per_unit_text += f"**Gold**: {costs['gold']:,}\n"
        per_unit_text += f"**Time**: {costs['time']}"
        
        embed.add_field(
            name="📈 Per Unit Costs",
            value=per_unit_text,
            inline=True
        )
        
        return embed
    
    def parse_time(self, time_str: str) -> int:
        """Parse time string to seconds."""
        total_seconds = 0
        if 'm' in time_str:
            minutes = int(time_str.split('m')[0])
            total_seconds += minutes * 60
        if 's' in time_str:
            seconds = int(time_str.split('m ')[1].split('s')[0])
            total_seconds += seconds
        return total_seconds
    
    def format_time(self, total_seconds: int) -> str:
        """Format seconds to time string."""
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

class QuantityModal(discord.ui.Modal, title="Set Troop Quantity"):
    """Modal for setting custom quantity."""
    
    def __init__(self, calculator_view: TroopCalculatorView):
        super().__init__()
        self.calculator_view = calculator_view
    
    quantity_input = discord.ui.TextInput(
        label="Quantity",
        placeholder="Enter number of troops (1-10000)",
        min_length=1,
        max_length=5,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle quantity submission."""
        try:
            quantity = int(self.quantity_input.value)
            if 1 <= quantity <= 10000:
                self.calculator_view.quantity = quantity
                embed = self.calculator_view.create_calculator_embed()
                await interaction.response.edit_message(embed=embed, view=self.calculator_view)
            else:
                await interaction.response.send_message("❌ Quantity must be between 1 and 10,000!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)

class TroopCalculator(commands.Cog):
    """Troop Calculator commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data_parser = DataParser()
    
    @app_commands.command(name="troopcalc", description="Calculate troop recruitment costs")
    async def troop_calculator(self, interaction: discord.Interaction):
        """Main troop calculator command."""
        try:
            # Debug: Check if troops data is available
            troops_data = self.data_parser.get_troops_data()
            if not troops_data:
                await interaction.response.send_message("❌ Error: No troops data available. Please check the troops.txt file.", ephemeral=True)
                return
                
            view = TroopCalculatorView(self.data_parser)
            embed = view.create_calculator_embed()
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    
    @app_commands.command(name="quickcalc", description="Quick troop cost calculation")
    @app_commands.describe(
        element="Troop element (Water, Earth, Fire, Air)",
        tier="Troop tier (T1, T2, T3, T4, T5, T6)",
        quantity="Number of troops to recruit"
    )
    async def quick_calculator(
        self, 
        interaction: discord.Interaction, 
        element: str, 
        tier: str, 
        quantity: int
    ):
        """Quick calculation without interactive UI."""
        try:
            if quantity < 1 or quantity > 10000:
                await interaction.response.send_message("❌ Quantity must be between 1 and 10,000!", ephemeral=True)
                return
            
            troops_data = self.data_parser.get_troops_data()
            
            if element not in troops_data:
                await interaction.response.send_message(f"❌ Invalid element: {element}", ephemeral=True)
                return
            
            if tier not in troops_data[element]:
                await interaction.response.send_message(f"❌ Invalid tier: {tier}", ephemeral=True)
                return
            
            troop = troops_data[element][tier]
            costs = troop['recruitment_costs']
            
            # Calculate totals
            total_food = costs['food'] * quantity
            total_wood = costs['wood'] * quantity
            total_stone = costs['stone'] * quantity
            total_gold = costs['gold'] * quantity
            
            # Calculate time
            time_per_unit = self.parse_time(costs['time'])
            total_seconds = time_per_unit * quantity
            total_time = self.format_time(total_seconds)
            
            embed = discord.Embed(
                title=f"⚔️ Quick Calculation: {tier} {troop['unit_name']} ({element})",
                description=f"**Quantity**: {quantity:,}",
                color=discord.Color.green()
            )
            
            cost_text = f"**Food**: {total_food:,}\n"
            cost_text += f"**Wood**: {total_wood:,}\n"
            if total_stone > 0:
                cost_text += f"**Stone**: {total_stone:,}\n"
            if total_gold > 0:
                cost_text += f"**Gold**: {total_gold:,}\n"
            cost_text += f"**Time**: {total_time}"
            
            embed.add_field(
                name="💰 Total Costs",
                value=cost_text,
                inline=False
            )
            
            embed.add_field(
                name="📊 Troop Stats",
                value=f"**Power**: {troop['power']}\n"
                      f"**ATK**: {troop['atk']}\n"
                      f"**DEF**: {troop['def']}\n"
                      f"**Health**: {troop['health']}\n"
                      f"**Speed**: {troop['speed']}\n"
                      f"**Load**: {troop['load']}",
                inline=True
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    
    def parse_time(self, time_str: str) -> int:
        """Parse time string to seconds."""
        total_seconds = 0
        if 'm' in time_str:
            minutes = int(time_str.split('m')[0])
            total_seconds += minutes * 60
        if 's' in time_str:
            seconds = int(time_str.split('m ')[1].split('s')[0])
            total_seconds += seconds
        return total_seconds
    
    def format_time(self, total_seconds: int) -> str:
        """Format seconds to time string."""
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

async def setup(bot: commands.Bot):
    """Setup function for the cog."""
    await bot.add_cog(TroopCalculator(bot))
