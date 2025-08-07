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

class TroopQuantityModal(discord.ui.Modal, title="Set Troop Quantity"):
    """Modal for setting troop quantity like townhall level input."""
    
    quantity_input = discord.ui.TextInput(
        label="Enter Quantity",
        placeholder="e.g., 100",
        min_length=1,
        max_length=10,
        required=True
    )
    
    def __init__(self, calculator_view):
        super().__init__()
        self.calculator_view = calculator_view
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle quantity submission."""
        try:
            quantity = int(self.quantity_input.value)
            if quantity >= 1:
                self.calculator_view.quantity = quantity
                embed = self.calculator_view.create_calculator_embed()
                await interaction.response.edit_message(embed=embed, view=self.calculator_view)
            else:
                embed = discord.Embed(
                    title="❌ Invalid Quantity",
                    description="Please enter a quantity of 1 or greater.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid Input",
                description="Please enter a valid number.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

class TroopCalculatorView(View):
    """Interactive view for troop calculator."""
    
    def __init__(self, data_parser: DataParser):
        super().__init__(timeout=300)
        self.data_parser = data_parser
        self.troops_data = data_parser.get_troops_data_fixed()
        self.selected_element = None
        self.selected_tier = None
        self.quantity = 1
        
    @discord.ui.select(
        placeholder="Choose an element...",
        options=[
            discord.SelectOption(label="Water", value="Water"),
            discord.SelectOption(label="Earth", value="Earth"),
            discord.SelectOption(label="Fire", value="Fire"),
            discord.SelectOption(label="Air", value="Air")
        ]
    )
    async def element_select(self, interaction: discord.Interaction, select: Select):
        """Handle element selection."""
        self.selected_element = select.values[0]
        self.selected_tier = None
        
        # Update tier options based on selected element
        tier_options = []
        if self.selected_element in self.troops_data:
            for tier in sorted(self.troops_data[self.selected_element].keys()):
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
    
    @discord.ui.button(label="Increase Quantity", style=discord.ButtonStyle.primary)
    async def increase_quantity(self, interaction: discord.Interaction, button: Button):
        """Increase troop quantity."""
        self.quantity += 1
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Decrease Quantity", style=discord.ButtonStyle.secondary)
    async def decrease_quantity(self, interaction: discord.Interaction, button: Button):
        """Decrease troop quantity."""
        self.quantity = max(self.quantity - 1, 1)
        embed = self.create_calculator_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Set Quantity", style=discord.ButtonStyle.success)
    async def set_quantity(self, interaction: discord.Interaction, button: Button):
        """Set custom quantity using modal."""
        await interaction.response.send_modal(TroopQuantityModal(self))
    
    def create_calculator_embed(self) -> discord.Embed:
        """Create the calculator embed."""
        embed = discord.Embed(
            title="Troop Calculator",
            description="Calculate recruitment costs for troops",
            color=discord.Color.blue()
        )
        
        if not self.selected_element:
            embed.add_field(
                name="Instructions",
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
        
        # Calculate total time
        time_per_unit = self.parse_time(costs['time'])
        total_seconds = time_per_unit * self.quantity
        total_time = self.format_time(total_seconds)
        
        # Use the embed generator for clean formatting
        from utils.embed_generator import EmbedGenerator
        total_costs = {
            'food': total_food,
            'wood': total_wood,
            'stone': total_stone,
            'gold': total_gold
        }
        
        return EmbedGenerator.create_troop_calculator_embed(
            troop_data=troop,
            quantity=self.quantity,
            total_costs=total_costs,
            total_time=total_time
        )
    
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
            troops_data = self.data_parser.get_troops_data_fixed()
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
            if quantity < 1:
                await interaction.response.send_message("❌ Quantity must be 1 or greater!", ephemeral=True)
                return
            
            troops_data = self.data_parser.get_troops_data_fixed()
            
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
            
            # Use the embed generator for clean formatting
            from utils.embed_generator import EmbedGenerator
            total_costs = {
                'food': total_food,
                'wood': total_wood,
                'stone': total_stone,
                'gold': total_gold
            }
            
            embed = EmbedGenerator.create_troop_calculator_embed(
                troop_data=troop,
                quantity=quantity,
                total_costs=total_costs,
                total_time=total_time
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
