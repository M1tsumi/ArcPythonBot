"""
TGL (The Greatest Leader) command module for Avatar Realms Collide Discord Bot.
Provides organized and concise TGL event information and tools.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional
from utils.embed_generator import EmbedGenerator

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
        """Show TGL event overview with interactive dropdown."""
        view = TGLOverviewView(self)
        embed = view._create_overview_embed()
        await interaction.response.send_message(embed=embed, view=view)
    
    async def show_tgl_single_server(self, interaction: discord.Interaction, stage: Optional[int] = None):
        """Show single server TGL information."""
        if stage and 1 <= stage <= 5:
            await self.show_specific_stage(interaction, "single_server", stage)
        else:
            embed = discord.Embed(
                title="ðŸ† TGL Single Server",
                description="Single server event details",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="ðŸ“Š Event Structure",
                value="â€¢ **Duration**: 5 Days\nâ€¢ **Repeats**: Every 2 Weeks\nâ€¢ **Scope**: Single Server Only",
                inline=False
            )
            
            embed.add_field(
            name="ðŸŽ¯ Available Commands",
            value="â€¢ `/tgl single_server 1` - Resource Gathering\nâ€¢ `/tgl single_server 2` - Bender Recruitment\nâ€¢ `/tgl single_server 3` - Hero Growth\nâ€¢ `/tgl single_server 4` - Shattered Skulls\nâ€¢ `/tgl single_server 5` - Power Increase",
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
                title="ðŸ† TGL Cross Server",
                description="Cross server event details",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="ðŸ“Š Event Structure",
                value="â€¢ **Duration**: 5 Days\nâ€¢ **Repeats**: Every 2 Weeks\nâ€¢ **Scope**: Multiple Servers",
                inline=False
            )
            
            embed.add_field(
                name="ðŸŽ¯ Available Commands",
                value="â€¢ `/tgl cross_server 1` - Resource Gathering\nâ€¢ `/tgl cross_server 2` - Bender Recruitment\nâ€¢ `/tgl cross_server 3` - Hero Growth\nâ€¢ `/tgl cross_server 4` - Shattered Skulls\nâ€¢ `/tgl cross_server 5` - Power Increase",
                inline=False
            )
            
            embed.set_footer(text="Use stage numbers (1-5) for specific details")
            await interaction.response.send_message(embed=embed)
    
    async def show_specific_stage(self, interaction: discord.Interaction, event_type: str, stage: int):
        """Show specific stage information."""
        stage_key = f"stage_{stage}"
        stage_data = self.tgl_data[event_type]["stages"][stage_key]
        
        embed = discord.Embed(
            title=f"ðŸ† TGL {event_type.replace('_', ' ').title()} - Stage {stage}",
            description=f"**{stage_data['name']}**",
            color=discord.Color.gold()
        )
        
        # Create task list
        tasks_text = ""
        for task, points in stage_data['tasks'].items():
            tasks_text += f"â€¢ **{task}**: {points:,} points\n"
        
        embed.add_field(
            name="ðŸ“‹ Tasks & Points",
            value=tasks_text,
            inline=False
        )
        
        embed.set_footer(text=f"Stage {stage} of 5 â€¢ {event_type.replace('_', ' ').title()}")
        await interaction.response.send_message(embed=embed)
    
    async def show_tgl_rewards(self, interaction: discord.Interaction):
        """Show TGL ranking rewards."""
        embed = discord.Embed(
            title="ðŸ† TGL Ranking Rewards",
            description="Daily and Overall rewards",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="ðŸ“… Daily Rewards (Top 3)",
            value="â€¢ **1st**: 10-20x Hero Shard, 500x Gem, Resources\nâ€¢ **2nd**: 5-10x Hero Shard, 300x Gem, Resources\nâ€¢ **3rd**: 2-5x Hero Shard, 200x Gem, Resources",
            inline=False
        )
        
        embed.add_field(
            name="ðŸ† Overall Rewards (Top 3)",
            value="â€¢ **1st**: 200-250x Hero Shard, 2,000-2,500x Gem\nâ€¢ **2nd**: 150-200x Hero Shard, 1,500-2,000x Gem\nâ€¢ **3rd**: 100-150x Hero Shard, 1,000-1,500x Gem",
            inline=False
        )
        
        embed.add_field(
            name="ðŸ’Ž Hero Shards",
            value="Rotates between: Aang, Amon, Korra, Kyoshi, Yangchen, Roku",
            inline=False
        )
        
        embed.set_footer(text="Rewards vary between Single Server and Cross Server")
        await interaction.response.send_message(embed=embed)
    
    async def show_tgl_tips(self, interaction: discord.Interaction):
        """Show TGL event tips and strategies."""
        embed = discord.Embed(
            title="ðŸ’¡ TGL Event Tips",
            description="Strategies for The Greatest Leader event",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="ðŸŽ¯ General Strategy",
            value="â€¢ Focus on high-point activities\nâ€¢ Use Lucky Tickets strategically\nâ€¢ Plan resource gathering efficiently\nâ€¢ Coordinate with alliance members",
            inline=False
        )
        
        embed.add_field(
            name="ðŸ“Š Point Optimization",
            value="â€¢ **Day 1**: Focus on research power increases\nâ€¢ **Day 2**: Recruit higher tier benders\nâ€¢ **Day 3**: Use scrolls and shards strategically\nâ€¢ **Day 4**: Target higher level skulls and fortresses\nâ€¢ **Day 5**: Maximize construction power gains",
            inline=False
        )
        
        embed.add_field(
            name="âš¡ Quick Tips",
            value="â€¢ Construction power only counts while online\nâ€¢ Hero power is excluded from final day\nâ€¢ Cross-server events have better rewards\nâ€¢ Coordinate with your alliance for maximum efficiency",
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
            await interaction.response.send_message("âŒ Invalid activity selected.", ephemeral=True)
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
            title="ðŸ§® TGL Points Calculator",
            description=f"Calculating points for {activity_names[activity]}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="ðŸ“Š Calculation",
            value=f"â€¢ **Activity**: {activity_names[activity]}\nâ€¢ **Quantity**: {quantity:,}\nâ€¢ **Points Per**: {points_per:,}\nâ€¢ **Total Points**: {total_points:,}",
            inline=False
        )
        
        embed.set_footer(text="Use this to plan your TGL strategy!")
        await interaction.response.send_message(embed=embed)

class TGLOverviewView(discord.ui.View):
    """Discord Components v2 view for TGL overview with daily stage dropdown."""
    
    def __init__(self, cog: "TGLSystem"):
        super().__init__(timeout=300)
        self.cog = cog
        self._setup_daily_stage_dropdown()
    
    def _setup_daily_stage_dropdown(self):
        """Setup the daily stages dropdown."""
        options = [
            discord.SelectOption(
                label="ðŸ“‹ Overview",
                value="overview",
                description="Main event overview and information",
                emoji="ðŸ“‹",
                default=True
            ),
            discord.SelectOption(
                label="Day 1: Resource Gathering & Research",
                value="stage_1",
                description="Gather resources and increase research power",
                emoji="â›ï¸"
            ),
            discord.SelectOption(
                label="Day 2: Bender Recruitment",
                value="stage_2", 
                description="Recruit benders from Tier 1 to Tier 6",
                emoji="ðŸ‘¥"
            ),
            discord.SelectOption(
                label="Day 3: Hero Growth",
                value="stage_3",
                description="Use scrolls and spirit shards/badges",
                emoji="âš¡"
            ),
            discord.SelectOption(
                label="Day 4: Shattered Skulls & Construction",
                value="stage_4",
                description="Clear skulls and build fortress levels",
                emoji="ðŸ—ï¸"
            ),
            discord.SelectOption(
                label="Day 5: Power Increase",
                value="stage_5",
                description="Final day - maximize power gains",
                emoji="ðŸ’ª"
            )
        ]
        
        select = discord.ui.Select(
            placeholder="ðŸŽ¯ Select a daily stage to view details...",
            options=options,
            custom_id="daily_stage_select"
        )
        select.callback = self._daily_stage_callback
        self.add_item(select)
    
    async def _daily_stage_callback(self, interaction: discord.Interaction):
        """Handle daily stage selection."""
        stage_value = interaction.data['values'][0]
        
        if stage_value == "overview":
            # Show main overview
            embed = self._create_overview_embed()
            
            # Update dropdown to show overview as selected
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    for option in item.options:
                        option.default = (option.value == "overview")
            
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            # Show specific stage
            stage_num = int(stage_value.split('_')[1])
            embed = await self._create_stage_embed(stage_num)
            
            # Update dropdown to show selected stage
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    for option in item.options:
                        option.default = (option.value == stage_value)
            
            await interaction.response.edit_message(embed=embed, view=self)
    
    def _create_overview_embed(self) -> discord.Embed:
        """Create the main overview embed."""
        embed = EmbedGenerator.create_embed(
            title="ðŸ† The Greatest Leader Event - Interactive Overview",
            description="ðŸŽ¯ **Prove you are the greatest leader in the world!**\nUse the dropdown below to explore each daily stage.",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="â° Event Details",
            value="â€¢ **Duration**: 5 Days\nâ€¢ **Repeats**: Every 2 Weeks\nâ€¢ **Type**: Single Server â†’ Cross Server",
            inline=True
        )
        
        embed.add_field(
            name="ðŸŽ® Event Types",
            value="â€¢ **Single Server**: Compete within your server\nâ€¢ **Cross Server**: Compete across multiple servers\nâ€¢ **Higher Rewards**: Cross-server events",
            inline=True
        )
        
        embed.add_field(
            name="ðŸ“‹ Daily Stages",
            value="ðŸ”¸ **Day 1**: Resource Gathering & Research\nðŸ”¸ **Day 2**: Bender Recruitment\nðŸ”¸ **Day 3**: Hero Growth\nðŸ”¸ **Day 4**: Shattered Skulls & Construction\nðŸ”¸ **Day 5**: Power Increase",
            inline=False
        )
        
        embed.add_field(
            name="ðŸŽ¯ Quick Commands",
            value="â€¢ `/tgl single_server` - Single server details\nâ€¢ `/tgl cross_server` - Cross server details\nâ€¢ `/tgl rewards` - Ranking rewards\nâ€¢ `/tgl tips` - Event strategies\nâ€¢ `/tgl_calc` - Points calculator",
            inline=False
        )
        
        embed.add_field(
            name="ðŸ’¡ Pro Tip",
            value="ðŸ“± **Use the dropdown above** to explore detailed information about each daily stage and plan your strategy!",
            inline=False
        )
        
        embed.add_field(
            name="ðŸ“ Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        embed.set_footer(text="ðŸŽ¯ Select a daily stage from the dropdown to view detailed tasks and points!")
        return EmbedGenerator.finalize_embed(embed)
    
    async def _create_stage_embed(self, stage_num: int) -> discord.Embed:
        """Create a detailed stage embed."""
        stage_key = f"stage_{stage_num}"
        
        # Use single_server data as the base (same for both types)
        stage_data = self.cog.tgl_data["single_server"]["stages"][stage_key]
        
        # Stage-specific emojis and colors
        stage_info = {
            1: {"emoji": "â›ï¸", "color": discord.Color.green()},
            2: {"emoji": "ðŸ‘¥", "color": discord.Color.blue()},
            3: {"emoji": "âš¡", "color": discord.Color.purple()},
            4: {"emoji": "ðŸ—ï¸", "color": discord.Color.orange()},
            5: {"emoji": "ðŸ’ª", "color": discord.Color.red()}
        }
        
        info = stage_info[stage_num]
        
        embed = EmbedGenerator.create_embed(
            title=f"{info['emoji']} Day {stage_num}: {stage_data['name']}",
            description=f"**Stage {stage_num} of 5** - Detailed tasks and point values",
            color=info['color']
        )
        
        # Create task list with better formatting
        tasks_text = ""
        total_possible_points = 0
        
        for task, points in stage_data['tasks'].items():
            if task == "Lucky Ticket":
                tasks_text += f"ðŸŽŸï¸ **{task}**: {points:,} points *(Special)*\n"
            else:
                tasks_text += f"â€¢ **{task}**: {points:,} points\n"
                if task != "Lucky Ticket":
                    total_possible_points += points
        
        embed.add_field(
            name="ðŸ“‹ Tasks & Points",
            value=tasks_text,
            inline=False
        )
        
        # Add strategic tips based on stage
        tips = {
            1: "ðŸŽ¯ Focus on research power increases for maximum points!\nResource gathering has lower points but is easier to complete.",
            2: "ðŸŽ¯ Higher tier benders give significantly more points!\nTier 6 benders are worth 350 points vs 25 for Tier 1.",
            3: "ðŸŽ¯ Legendary items give massive points (50,000 each)!\nSilver/Golden scrolls are more affordable options.",
            4: "ðŸŽ¯ Higher level skulls and fortress levels give more points!\nSkull levels 26-30 give 3,000 points each.",
            5: "ðŸŽ¯ Construction power only counts while online!\nHero power is excluded from this final day."
        }
        
        embed.add_field(
            name="ðŸ’¡ Strategy Tips",
            value=tips[stage_num],
            inline=False
        )
        
        # Add point summary
        embed.add_field(
            name="ðŸ“Š Point Summary",
            value=f"Regular tasks: **{total_possible_points:,}** points\nLucky Ticket: **150,000** points *(if available)*",
            inline=True
        )
        
        embed.add_field(
            name="ðŸ”„ Navigation",
            value="Use the dropdown above to explore other daily stages!",
            inline=True
        )
        
        embed.set_footer(text=f"Day {stage_num}/5 â€¢ Use /tgl_calc to calculate your potential points!")
        return EmbedGenerator.finalize_embed(embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TGLSystem(bot))
