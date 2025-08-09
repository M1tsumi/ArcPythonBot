"""
Glorious Victory command module for Avatar Realms Collide Discord Bot.
Provides organized and concise Glorious Victory event information and tools.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional

class GloriousVictorySystem(commands.Cog):
    """Glorious Victory command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        
        # Glorious Victory Event Data
        self.gv_data = {
            "duration": "2 Days",
            "repeats": "Weekly",
            "description": "Shatter Skulls' Fortresses with your alliance and earn rewards.",
            "scoring": {
                "level_1": 10,
                "level_2": 20,
                "level_3": 30,
                "level_4": 45,
                "level_5": 60,
                "level_6": 75
            },
            "milestone_rewards": {
                30: {
                    "gems": 100,
                    "rare_shards": 3,
                    "rare_badges": 3,
                    "speedups": 1
                },
                70: {
                    "gems": 150,
                    "epic_shards": 1,
                    "epic_badges": 1,
                    "speedups": 3
                },
                120: {
                    "gems": 200,
                    "epic_shards": 3,
                    "epic_badges": 3,
                    "speedups": 5
                },
                200: {
                    "gems": 300,
                    "legendary_shards": 1,
                    "legendary_badges": 1,
                    "speedups": 10
                }
            },
            "ranking_rewards": {
                1: {
                    "epic_shards": 20,
                    "epic_badges": 20,
                    "speedups": 10,
                    "books": 20
                },
                2: {
                    "epic_shards": 15,
                    "epic_badges": 15,
                    "speedups": 5,
                    "books": 15
                },
                3: {
                    "epic_shards": 10,
                    "epic_badges": 10,
                    "speedups": 3,
                    "books": 10
                },
                "4-5": {
                    "epic_shards": 5,
                    "epic_badges": 5,
                    "speedups": 2,
                    "books": 5
                },
                "6-10": {
                    "epic_shards": 2,
                    "epic_badges": 2,
                    "speedups": 1,
                    "books": 2
                }
            }
        }
    
    @app_commands.command(name="glorious_victory", description="Glorious Victory event information")
    @app_commands.describe(
        type="Information type to view"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="overview", value="overview"),
        app_commands.Choice(name="scoring", value="scoring"),
        app_commands.Choice(name="milestones", value="milestones"),
        app_commands.Choice(name="rankings", value="rankings"),
        app_commands.Choice(name="guide", value="guide")
    ])
    async def glorious_victory(self, interaction: discord.Interaction, type: str):
        """Main Glorious Victory command with organized information."""
        if type == "overview":
            await self.show_gv_overview(interaction)
        elif type == "scoring":
            await self.show_gv_scoring(interaction)
        elif type == "milestones":
            await self.show_gv_milestones(interaction)
        elif type == "rankings":
            await self.show_gv_rankings(interaction)
        elif type == "guide":
            await self.show_gv_guide(interaction)
    
    async def show_gv_overview(self, interaction: discord.Interaction):
        """Show Glorious Victory event overview."""
        embed = discord.Embed(
            title="🏆 Glorious Victory Event",
            description="Shatter Skulls' Fortresses with your alliance and earn rewards!",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="⏰ Event Details",
            value=f"• **Duration**: {self.gv_data['duration']}\n• **Repeats**: {self.gv_data['repeats']}\n• **Minimum Points**: 200 for rewards",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Event Objective",
            value="• Destroy Shattered Skulls' Fortresses\n• Points depend on fortress level\n• Alliance cooperation required\n• Rank for amazing rewards",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Quick Commands",
            value="• `/glorious_victory scoring` - Point values\n• `/glorious_victory milestones` - Milestone rewards\n• `/glorious_victory rankings` - Ranking rewards\n• `/glorious_victory guide` - Event strategies",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        embed.set_footer(text="The joy of victory is doubled when shared!")
        await interaction.response.send_message(embed=embed)
    
    async def show_gv_scoring(self, interaction: discord.Interaction):
        """Show Glorious Victory scoring system."""
        embed = discord.Embed(
            title="📊 Glorious Victory Scoring",
            description="Points awarded for destroying Shattered Skulls' Fortresses",
            color=discord.Color.blue()
        )
        
        scoring_text = ""
        for level, points in self.gv_data['scoring'].items():
            level_num = level.split('_')[1]
            scoring_text += f"• **Level {level_num} Fortress**: {points:,} points\n"
        
        embed.add_field(
            name="🏰 Fortress Levels & Points",
            value=scoring_text,
            inline=False
        )
        
        embed.add_field(
            name="💡 Scoring Tips",
            value="• Higher level fortresses = more points\n• Coordinate with alliance members\n• Focus on level 4+ fortresses for efficiency\n• Minimum 200 points required for rewards",
            inline=False
        )
        
        embed.set_footer(text="Destroy higher level fortresses for maximum points!")
        await interaction.response.send_message(embed=embed)
    
    async def show_gv_milestones(self, interaction: discord.Interaction):
        """Show Glorious Victory milestone rewards."""
        embed = discord.Embed(
            title="🎁 Glorious Victory Milestone Rewards",
            description="Rewards for reaching point milestones",
            color=discord.Color.gold()
        )
        
        milestones_text = ""
        for points, rewards in self.gv_data['milestone_rewards'].items():
            milestones_text += f"• **{points:,} Points**: "
            rewards_list = []
            if rewards.get('gems'):
                rewards_list.append(f"{rewards['gems']}x Gem")
            if rewards.get('rare_shards'):
                rewards_list.append(f"{rewards['rare_shards']}x Rare Spirit Shard")
            if rewards.get('rare_badges'):
                rewards_list.append(f"{rewards['rare_badges']}x Rare Spirit Badge")
            if rewards.get('epic_shards'):
                rewards_list.append(f"{rewards['epic_shards']}x Epic Spirit Shard")
            if rewards.get('epic_badges'):
                rewards_list.append(f"{rewards['epic_badges']}x Epic Spirit Badge")
            if rewards.get('legendary_shards'):
                rewards_list.append(f"{rewards['legendary_shards']}x Legendary Spirit Shard")
            if rewards.get('legendary_badges'):
                rewards_list.append(f"{rewards['legendary_badges']}x Legendary Spirit Badge")
            if rewards.get('speedups'):
                rewards_list.append(f"{rewards['speedups']}x Research Speedup 60m")
            
            milestones_text += ", ".join(rewards_list) + "\n"
        
        embed.add_field(
            name="📋 Milestone Rewards",
            value=milestones_text,
            inline=False
        )
        
        embed.set_footer(text="Reach higher milestones for better rewards!")
        await interaction.response.send_message(embed=embed)
    
    async def show_gv_rankings(self, interaction: discord.Interaction):
        """Show Glorious Victory ranking rewards."""
        embed = discord.Embed(
            title="🏆 Glorious Victory Ranking Rewards",
            description="Rewards for top alliance rankings",
            color=discord.Color.gold()
        )
        
        rankings_text = ""
        for rank, rewards in self.gv_data['ranking_rewards'].items():
            rank_text = f"#{rank}" if isinstance(rank, int) else f"#{rank}"
            rankings_text += f"• **{rank_text}**: "
            rewards_list = []
            if rewards.get('epic_shards'):
                rewards_list.append(f"{rewards['epic_shards']}x Epic Spirit Shard")
            if rewards.get('epic_badges'):
                rewards_list.append(f"{rewards['epic_badges']}x Epic Spirit Badge")
            if rewards.get('speedups'):
                rewards_list.append(f"{rewards['speedups']}x Speedup 60m")
            if rewards.get('books'):
                rewards_list.append(f"{rewards['books']}x Book of Experience (5,000)")
            
            rankings_text += ", ".join(rewards_list) + "\n"
        
        embed.add_field(
            name="🏅 Ranking Rewards",
            value=rankings_text,
            inline=False
        )
        
        embed.add_field(
            name="📊 Requirements",
            value="• Minimum 200 points to qualify for ranking rewards\n• Alliance-based competition\n• Top 10 alliances receive rewards",
            inline=False
        )
        
        embed.set_footer(text="Compete with your alliance for top rankings!")
        await interaction.response.send_message(embed=embed)
    
    async def show_gv_guide(self, interaction: discord.Interaction):
        """Show Glorious Victory event guide and strategies."""
        embed = discord.Embed(
            title="💡 Glorious Victory Event Guide",
            description="Strategies for the Glorious Victory event",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎯 Event Strategy",
            value="• Coordinate with alliance members\n• Focus on higher level fortresses\n• Plan attacks efficiently\n• Share resources and information",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ Combat Tips",
            value="• Shattered Skulls' Fortresses are very powerful\n• Team up with alliance members\n• Use proper hero combinations\n• Time your attacks strategically",
            inline=False
        )
        
        embed.add_field(
            name="📈 Point Optimization",
            value="• **Level 4+ Fortresses**: Best point efficiency\n• **Alliance Coordination**: Essential for success\n• **Resource Management**: Plan your attacks\n• **Communication**: Keep alliance informed",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Quick Tips",
            value="• Minimum 200 points required for rewards\n• Higher level fortresses = more points\n• Alliance cooperation is key\n• Plan your fortress targets in advance",
            inline=False
        )
        
        embed.set_footer(text="The joy of victory is doubled when shared!")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="gv_calc", description="Calculate Glorious Victory points for fortress levels")
    @app_commands.describe(
        fortress_level="Fortress level to calculate",
        quantity="Number of fortresses destroyed"
    )
    @app_commands.choices(fortress_level=[
        app_commands.Choice(name="Level 1 Fortress", value="level_1"),
        app_commands.Choice(name="Level 2 Fortress", value="level_2"),
        app_commands.Choice(name="Level 3 Fortress", value="level_3"),
        app_commands.Choice(name="Level 4 Fortress", value="level_4"),
        app_commands.Choice(name="Level 5 Fortress", value="level_5"),
        app_commands.Choice(name="Level 6 Fortress", value="level_6")
    ])
    async def gv_calc(self, interaction: discord.Interaction, fortress_level: str, quantity: int):
        """Calculate Glorious Victory points for fortress destruction."""
        if fortress_level not in self.gv_data['scoring']:
            await interaction.response.send_message("❌ Invalid fortress level selected.", ephemeral=True)
            return
        
        points_per = self.gv_data['scoring'][fortress_level]
        total_points = points_per * quantity
        
        # Fortress level name mapping for display
        level_names = {
            "level_1": "Level 1 Fortress",
            "level_2": "Level 2 Fortress", 
            "level_3": "Level 3 Fortress",
            "level_4": "Level 4 Fortress",
            "level_5": "Level 5 Fortress",
            "level_6": "Level 6 Fortress"
        }
        
        embed = discord.Embed(
            title="🧮 Glorious Victory Points Calculator",
            description=f"Calculating points for {level_names[fortress_level]}",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="📊 Calculation",
            value=f"• **Fortress**: {level_names[fortress_level]}\n• **Quantity**: {quantity:,}\n• **Points Per**: {points_per:,}\n• **Total Points**: {total_points:,}",
            inline=False
        )
        
        # Add milestone information
        if total_points >= 200:
            embed.add_field(
                name="🎉 Milestone Achieved!",
                value="✅ You've reached the minimum 200 points required for rewards!",
                inline=False
            )
        else:
            points_needed = 200 - total_points
            embed.add_field(
                name="🎯 Progress to Milestone",
                value=f"📈 You need {points_needed:,} more points to reach the 200-point milestone for rewards.",
                inline=False
            )
        
        embed.set_footer(text="Use this to plan your fortress destruction strategy!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(GloriousVictorySystem(bot)) 