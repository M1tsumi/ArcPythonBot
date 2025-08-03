"""
TGL (The Greatest Leader) command module for Avatar Realms Collide Discord Bot.
Provides organized and concise TGL event information and tools.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional

class TGLSystem(commands.Cog):
    """TGL (The Greatest Leader) command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        
        # TGL Event Data
        self.tgl_data = {
            "single_server": {
                "duration": "5 Days",
                "repeats": "2 Weeks",
                "stages": {
                    "stage_1": {
                        "name": "Resource Gathering & Research",
                        "tasks": {
                            "Gather 100 Food": 3,
                            "Gather 100 Wood": 3,
                            "Gather 100 Stone": 3,
                            "Gather 50 Gold": 3,
                            "Increase Power by 1 (Research)": 25,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_2": {
                        "name": "Bender Recruitment",
                        "tasks": {
                            "Tier 1 Bender": 25,
                            "Tier 2 Bender": 50,
                            "Tier 3 Bender": 75,
                            "Tier 4 Bender": 100,
                            "Tier 5 Bender": 150,
                            "Tier 6 Bender": 350,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_3": {
                        "name": "Hero Growth",
                        "tasks": {
                            "Silver Scroll": 750,
                            "Golden Scroll": 1500,
                            "Rare Hero Spirit Shard": 250,
                            "Epic Hero Spirit Shard": 1250,
                            "Legendary Hero Spirit Shard": 50000,
                            "Rare Hero Spirit Badge": 250,
                            "Epic Hero Spirit Badge": 1250,
                            "Legendary Hero Spirit Badge": 50000,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_4": {
                        "name": "Shattered Skulls & Construction",
                        "tasks": {
                            "Skull Levels 1-5": 1500,
                            "Skull Levels 6-10": 1800,
                            "Skull Levels 11-15": 2100,
                            "Skull Levels 16-20": 2400,
                            "Skull Levels 21-25": 2700,
                            "Skull Levels 26-30": 3000,
                            "Fortress Level 1": 10000,
                            "Fortress Level 2": 12000,
                            "Fortress Level 3": 14000,
                            "Fortress Level 4": 16000,
                            "Increase Power by 1 (Construction)": 25
                        }
                    },
                    "stage_5": {
                        "name": "Power Increase",
                        "tasks": {
                            "Increase Power by 1": 20
                        }
                    }
                }
            },
            "cross_server": {
                "duration": "5 Days",
                "repeats": "2 Weeks",
                "stages": {
                    "stage_1": {
                        "name": "Resource Gathering & Research",
                        "tasks": {
                            "Gather 100 Food": 3,
                            "Gather 100 Wood": 3,
                            "Gather 100 Stone": 3,
                            "Gather 50 Gold": 3,
                            "Increase Power by 1 (Research)": 25,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_2": {
                        "name": "Bender Recruitment",
                        "tasks": {
                            "Tier 1 Bender": 25,
                            "Tier 2 Bender": 50,
                            "Tier 3 Bender": 75,
                            "Tier 4 Bender": 100,
                            "Tier 5 Bender": 150,
                            "Tier 6 Bender": 350,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_3": {
                        "name": "Hero Growth",
                        "tasks": {
                            "Silver Scroll": 750,
                            "Golden Scroll": 1500,
                            "Rare Hero Spirit Shard": 250,
                            "Epic Hero Spirit Shard": 1250,
                            "Legendary Hero Spirit Shard": 50000,
                            "Rare Hero Spirit Badge": 250,
                            "Epic Hero Spirit Badge": 1250,
                            "Legendary Hero Spirit Badge": 50000,
                            "Lucky Ticket": 150000
                        }
                    },
                    "stage_4": {
                        "name": "Shattered Skulls & Construction",
                        "tasks": {
                            "Skull Levels 1-5": 1500,
                            "Skull Levels 6-10": 1800,
                            "Skull Levels 11-15": 2100,
                            "Skull Levels 16-20": 2400,
                            "Skull Levels 21-25": 2700,
                            "Skull Levels 26-30": 3000,
                            "Fortress Level 1": 10000,
                            "Fortress Level 2": 12000,
                            "Fortress Level 3": 14000,
                            "Fortress Level 4": 16000,
                            "Increase Power by 1 (Construction)": 25
                        }
                    },
                    "stage_5": {
                        "name": "Power Increase",
                        "tasks": {
                            "Increase Power by 1": 20
                        }
                    }
                }
            }
        }
    
    @app_commands.command(name="tgl", description="The Greatest Leader event information")
    @app_commands.describe(
        type="Event type to view",
        stage="Specific stage to view (optional)"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="overview", value="overview"),
        app_commands.Choice(name="single_server", value="single_server"),
        app_commands.Choice(name="cross_server", value="cross_server"),
        app_commands.Choice(name="rewards", value="rewards"),
        app_commands.Choice(name="tips", value="tips")
    ])
    async def tgl(self, interaction: discord.Interaction, type: str, stage: Optional[int] = None):
        """Main TGL command with organized information."""
        if type == "overview":
            await self.show_tgl_overview(interaction)
        elif type == "single_server":
            await self.show_tgl_single_server(interaction, stage)
        elif type == "cross_server":
            await self.show_tgl_cross_server(interaction, stage)
        elif type == "rewards":
            await self.show_tgl_rewards(interaction)
        elif type == "tips":
            await self.show_tgl_tips(interaction)
    
    async def show_tgl_overview(self, interaction: discord.Interaction):
        """Show TGL event overview."""
        embed = discord.Embed(
            title="🏆 The Greatest Leader Event",
            description="Prove you are the greatest leader in the world!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="⏰ Event Details",
            value="• **Duration**: 5 Days\n• **Repeats**: Every 2 Weeks\n• **Type**: Single Server → Cross Server",
            inline=False
        )
        
        embed.add_field(
            name="📋 Daily Stages",
            value="• **Day 1**: Resource Gathering & Research\n• **Day 2**: Bender Recruitment\n• **Day 3**: Hero Growth\n• **Day 4**: Shattered Skulls & Construction\n• **Day 5**: Power Increase",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Quick Commands",
            value="• `/tgl single_server` - Single server details\n• `/tgl cross_server` - Cross server details\n• `/tgl rewards` - Ranking rewards\n• `/tgl tips` - Event strategies",
            inline=False
        )
        
        embed.set_footer(text="Use specific commands for detailed information")
        await interaction.response.send_message(embed=embed)
    
    async def show_tgl_single_server(self, interaction: discord.Interaction, stage: Optional[int] = None):
        """Show single server TGL information."""
        if stage and 1 <= stage <= 5:
            await self.show_specific_stage(interaction, "single_server", stage)
        else:
            embed = discord.Embed(
                title="🏆 TGL Single Server",
                description="Single server event details",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📊 Event Structure",
                value="• **Duration**: 5 Days\n• **Repeats**: Every 2 Weeks\n• **Scope**: Single Server Only",
                inline=False
            )
            
            embed.add_field(
            name="🎯 Available Commands",
            value="• `/tgl single_server 1` - Resource Gathering\n• `/tgl single_server 2` - Bender Recruitment\n• `/tgl single_server 3` - Hero Growth\n• `/tgl single_server 4` - Shattered Skulls\n• `/tgl single_server 5` - Power Increase",
            inline=False
        )
            
            embed.set_footer(text="Use stage numbers (1-5) for specific details")
            await interaction.response.send_message(embed=embed)
    
    async def show_tgl_cross_server(self, interaction: discord.Interaction, stage: Optional[int] = None):
        """Show cross server TGL information."""
        if stage and 1 <= stage <= 5:
            await self.show_specific_stage(interaction, "cross_server", stage)
        else:
            embed = discord.Embed(
                title="🏆 TGL Cross Server",
                description="Cross server event details",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="📊 Event Structure",
                value="• **Duration**: 5 Days\n• **Repeats**: Every 2 Weeks\n• **Scope**: Multiple Servers",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Available Commands",
                value="• `/tgl cross_server 1` - Resource Gathering\n• `/tgl cross_server 2` - Bender Recruitment\n• `/tgl cross_server 3` - Hero Growth\n• `/tgl cross_server 4` - Shattered Skulls\n• `/tgl cross_server 5` - Power Increase",
                inline=False
            )
            
            embed.set_footer(text="Use stage numbers (1-5) for specific details")
            await interaction.response.send_message(embed=embed)
    
    async def show_specific_stage(self, interaction: discord.Interaction, event_type: str, stage: int):
        """Show specific stage information."""
        stage_key = f"stage_{stage}"
        stage_data = self.tgl_data[event_type]["stages"][stage_key]
        
        embed = discord.Embed(
            title=f"🏆 TGL {event_type.replace('_', ' ').title()} - Stage {stage}",
            description=f"**{stage_data['name']}**",
            color=discord.Color.gold()
        )
        
        # Create task list
        tasks_text = ""
        for task, points in stage_data['tasks'].items():
            tasks_text += f"• **{task}**: {points:,} points\n"
        
        embed.add_field(
            name="📋 Tasks & Points",
            value=tasks_text,
            inline=False
        )
        
        embed.set_footer(text=f"Stage {stage} of 5 • {event_type.replace('_', ' ').title()}")
        await interaction.response.send_message(embed=embed)
    
    async def show_tgl_rewards(self, interaction: discord.Interaction):
        """Show TGL ranking rewards."""
        embed = discord.Embed(
            title="🏆 TGL Ranking Rewards",
            description="Daily and Overall rewards",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📅 Daily Rewards (Top 3)",
            value="• **1st**: 10-20x Hero Shard, 500x Gem, Resources\n• **2nd**: 5-10x Hero Shard, 300x Gem, Resources\n• **3rd**: 2-5x Hero Shard, 200x Gem, Resources",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Overall Rewards (Top 3)",
            value="• **1st**: 200-250x Hero Shard, 2,000-2,500x Gem\n• **2nd**: 150-200x Hero Shard, 1,500-2,000x Gem\n• **3rd**: 100-150x Hero Shard, 1,000-1,500x Gem",
            inline=False
        )
        
        embed.add_field(
            name="💎 Hero Shards",
            value="Rotates between: Aang, Amon, Korra, Kyoshi, Yangchen, Roku",
            inline=False
        )
        
        embed.set_footer(text="Rewards vary between Single Server and Cross Server")
        await interaction.response.send_message(embed=embed)
    
    async def show_tgl_tips(self, interaction: discord.Interaction):
        """Show TGL event tips and strategies."""
        embed = discord.Embed(
            title="💡 TGL Event Tips",
            description="Strategies for The Greatest Leader event",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎯 General Strategy",
            value="• Focus on high-point activities\n• Use Lucky Tickets strategically\n• Plan resource gathering efficiently\n• Coordinate with alliance members",
            inline=False
        )
        
        embed.add_field(
            name="📊 Point Optimization",
            value="• **Day 1**: Focus on research power increases\n• **Day 2**: Recruit higher tier benders\n• **Day 3**: Use scrolls and shards strategically\n• **Day 4**: Target higher level skulls and fortresses\n• **Day 5**: Maximize construction power gains",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Quick Tips",
            value="• Construction power only counts while online\n• Hero power is excluded from final day\n• Cross-server events have better rewards\n• Coordinate with your alliance for maximum efficiency",
            inline=False
        )
        
        embed.set_footer(text="Plan ahead and coordinate with your alliance!")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="tgl_calc", description="Calculate TGL points for activities")
    @app_commands.describe(
        activity="Activity type",
        quantity="Number of activities"
    )
    @app_commands.choices(activity=[
        app_commands.Choice(name="Resource Gathering (Food/Wood/Stone/Gold)", value="resource_gathering"),
        app_commands.Choice(name="Research Power +1", value="research_power"),
        app_commands.Choice(name="Tier 1-2 Bender", value="tier_1_2_bender"),
        app_commands.Choice(name="Tier 3-4 Bender", value="tier_3_4_bender"),
        app_commands.Choice(name="Tier 5-6 Bender", value="tier_5_6_bender"),
        app_commands.Choice(name="Silver Scroll", value="silver_scroll"),
        app_commands.Choice(name="Golden Scroll", value="golden_scroll"),
        app_commands.Choice(name="Rare Hero Spirit Shard", value="rare_shard"),
        app_commands.Choice(name="Epic Hero Spirit Shard", value="epic_shard"),
        app_commands.Choice(name="Legendary Hero Spirit Shard", value="legendary_shard"),
        app_commands.Choice(name="Rare Hero Spirit Badge", value="rare_badge"),
        app_commands.Choice(name="Epic Hero Spirit Badge", value="epic_badge"),
        app_commands.Choice(name="Legendary Hero Spirit Badge", value="legendary_badge"),
        app_commands.Choice(name="Skull Levels 1-10", value="skull_1_10"),
        app_commands.Choice(name="Skull Levels 11-20", value="skull_11_20"),
        app_commands.Choice(name="Skull Levels 21-30", value="skull_21_30"),
        app_commands.Choice(name="Fortress Level 1-2", value="fortress_1_2"),
        app_commands.Choice(name="Fortress Level 3-4", value="fortress_3_4"),
        app_commands.Choice(name="Construction Power +1", value="construction_power"),
        app_commands.Choice(name="General Power +1", value="general_power"),
        app_commands.Choice(name="Lucky Ticket", value="lucky_ticket")
    ])
    async def tgl_calc(self, interaction: discord.Interaction, activity: str, quantity: int):
        """Calculate TGL points for specific activities."""
        # Point values mapping
        point_values = {
            "resource_gathering": 3,  # Average of all resource gathering activities
            "research_power": 25,
            "tier_1_2_bender": 37,  # Average of tier 1 (25) and tier 2 (50)
            "tier_3_4_bender": 87,  # Average of tier 3 (75) and tier 4 (100)
            "tier_5_6_bender": 250,  # Average of tier 5 (150) and tier 6 (350)
            "silver_scroll": 750,
            "golden_scroll": 1500,
            "rare_shard": 250,
            "epic_shard": 1250,
            "legendary_shard": 50000,
            "rare_badge": 250,
            "epic_badge": 1250,
            "legendary_badge": 50000,
            "skull_1_10": 1650,  # Average of skull 1-5 (1500) and 6-10 (1800)
            "skull_11_20": 2250,  # Average of skull 11-15 (2100) and 16-20 (2400)
            "skull_21_30": 2850,  # Average of skull 21-25 (2700) and 26-30 (3000)
            "fortress_1_2": 11000,  # Average of fortress 1 (10000) and 2 (12000)
            "fortress_3_4": 15000,  # Average of fortress 3 (14000) and 4 (16000)
            "construction_power": 25,
            "general_power": 20,
            "lucky_ticket": 150000
        }
        
        if activity not in point_values:
            await interaction.response.send_message("❌ Invalid activity selected.", ephemeral=True)
            return
        
        points_per = point_values[activity]
        total_points = points_per * quantity
        
        # Activity name mapping for display
        activity_names = {
            "resource_gathering": "Resource Gathering (Food/Wood/Stone/Gold)",
            "research_power": "Research Power +1",
            "tier_1_2_bender": "Tier 1-2 Bender",
            "tier_3_4_bender": "Tier 3-4 Bender",
            "tier_5_6_bender": "Tier 5-6 Bender",
            "silver_scroll": "Silver Scroll",
            "golden_scroll": "Golden Scroll",
            "rare_shard": "Rare Hero Spirit Shard",
            "epic_shard": "Epic Hero Spirit Shard",
            "legendary_shard": "Legendary Hero Spirit Shard",
            "rare_badge": "Rare Hero Spirit Badge",
            "epic_badge": "Epic Hero Spirit Badge",
            "legendary_badge": "Legendary Hero Spirit Badge",
            "skull_1_10": "Skull Levels 1-10",
            "skull_11_20": "Skull Levels 11-20",
            "skull_21_30": "Skull Levels 21-30",
            "fortress_1_2": "Fortress Level 1-2",
            "fortress_3_4": "Fortress Level 3-4",
            "construction_power": "Construction Power +1",
            "general_power": "General Power +1",
            "lucky_ticket": "Lucky Ticket"
        }
        
        embed = discord.Embed(
            title="🧮 TGL Points Calculator",
            description=f"Calculating points for {activity_names[activity]}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Calculation",
            value=f"• **Activity**: {activity_names[activity]}\n• **Quantity**: {quantity:,}\n• **Points Per**: {points_per:,}\n• **Total Points**: {total_points:,}",
            inline=False
        )
        
        embed.set_footer(text="Use this to plan your TGL strategy!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TGLSystem(bot)) 