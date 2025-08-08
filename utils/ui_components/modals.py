"""
Modal components for Avatar Realms Collide Discord Bot.
Contains interactive modal forms for user input.
"""

import discord
from typing import Dict

class TownHallModal(discord.ui.Modal, title="Town Hall Level"):
    """Modal for town hall level input."""
    
    level_input = discord.ui.TextInput(
        label="Enter Town Hall Level (3-30)",
        placeholder="e.g., 15",
        min_length=1,
        max_length=2,
        required=True
    )
    
    def __init__(self):
        super().__init__()
        self.town_hall_data = {
            3: {"food": "2.3K", "wood": "2.3K", "stone": "700", "time": "15s"},
            4: {"food": "3.7K", "wood": "3.7K", "stone": "1.0K", "time": "40s"},
            5: {"food": "6.7K", "wood": "6.7K", "stone": "3.0K", "time": "2m"},
            6: {"food": "12.0K", "wood": "12.0K", "stone": "7.2K", "time": "5m"},
            7: {"food": "16.8K", "wood": "16.8K", "stone": "10.1K", "time": "50m"},
            8: {"food": "23.5K", "wood": "23.5K", "stone": "14.1K", "time": "2h 30m"},
            9: {"food": "32.9K", "wood": "32.9K", "stone": "19.7K", "time": "5h"},
            10: {"food": "47.4K", "wood": "47.4K", "stone": "28.4K", "time": "7h 20m"},
            11: {"food": "68.3K", "wood": "68.3K", "stone": "41.0K", "time": "12h"},
            12: {"food": "98.4K", "wood": "98.4K", "stone": "59.0K", "time": "13h 12m"},
            13: {"food": "142.0K", "wood": "142.0K", "stone": "85.2K", "time": "14h 31m 10s"},
            14: {"food": "204.0K", "wood": "204.0K", "stone": "122.0K", "time": "1d 3h 35m 10s"},
            15: {"food": "298.0K", "wood": "298.0K", "stone": "179.0K", "time": "1d 9h 6m 10s"},
            16: {"food": "435.0K", "wood": "435.0K", "stone": "261.0K", "time": "1d 15h 43m 20s"},
            17: {"food": "635.0K", "wood": "635.0K", "stone": "381.0K", "time": "1d 19h 41m 40s"},
            18: {"food": "927.0K", "wood": "927.0K", "stone": "556.0K", "time": "2d 3m 50s"},
            19: {"food": "1.4M", "wood": "1.4M", "stone": "840.0K", "time": "2d 4h 52m 10s"},
            20: {"food": "2.0M", "wood": "2.0M", "stone": "1.2M", "time": "3d 2h 1m"},
            21: {"food": "2.9M", "wood": "2.9M", "stone": "1.7M", "time": "3d 16h 49m 10s"},
            22: {"food": "4.3M", "wood": "4.3M", "stone": "2.6M", "time": "4d 10h 35m"},
            23: {"food": "6.3M", "wood": "6.3M", "stone": "3.8M", "time": "5d 7h 54m"},
            24: {"food": "9.3M", "wood": "9.3M", "stone": "5.6M", "time": "6d 9h 28m 50s"},
            25: {"food": "13.7M", "wood": "13.7M", "stone": "8.2M", "time": "8d 22h 52m 20s"},
            26: {"food": "20.3M", "wood": "20.3M", "stone": "12.2M", "time": "16d 2h 46m 10s"},
            27: {"food": "30.0M", "wood": "30.0M", "stone": "18.0M", "time": "20d 22h 48m"},
            28: {"food": "44.4M", "wood": "44.4M", "stone": "26.6M", "time": "27d 5h 38m 20s"},
            29: {"food": "65.7M", "wood": "65.7M", "stone": "39.4M", "time": "46d 7h 11m 10s"},
            30: {"food": "98.6M", "wood": "98.6M", "stone": "59.2M", "time": "148d 3h 47m 40s"}
        }
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            level = int(self.level_input.value)
            
            if level < 3 or level > 30:
                embed = discord.Embed(
                    title="❌ Invalid Level",
                    description="Please enter a level between 3 and 30.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            data = self.town_hall_data.get(level)
            
            if not data:
                embed = discord.Embed(
                    title="❌ Level Not Found",
                    description=f"Town Hall level {level} information is not available.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"🏛️ Town Hall {level}",
                description=f"Requirements for upgrading to Town Hall level {level}",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="🌾 Food",
                value=f"**{data['food']}**",
                inline=True
            )
            
            embed.add_field(
                name="🪵 Wood",
                value=f"**{data['wood']}**",
                inline=True
            )
            
            embed.add_field(
                name="🪨 Stone",
                value=f"**{data['stone']}**",
                inline=True
            )
            
            embed.add_field(
                name="⏰ Base Time",
                value=f"**{data['time']}**",
                inline=False
            )
            
            embed.add_field(
                name="📝 Note",
                value="*Times shown do not include research and town hall buffs for time reduction*",
                inline=False
            )
            
            embed.set_footer(text="Provided by Deng (@2rk) • Town Hall requirements")
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid Input",
                description="Please enter a valid number between 3 and 30.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True) 