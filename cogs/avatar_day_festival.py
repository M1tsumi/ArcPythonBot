"""
Avatar Day Festival commands cog for the Avatar Realms Collide Discord Bot.
Provides comprehensive information about the Avatar Day Festival event.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator

class AvatarDayFestivalView(discord.ui.View):
    """Interactive view for Avatar Day Festival details with buttons."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
    
    @discord.ui.button(label="Event Tasks", style=discord.ButtonStyle.primary, emoji="📋")
    async def show_tasks(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event tasks for each day."""
        embed = discord.Embed(
            title=self.get_text(interaction.user.id, "avatar_day_festival_tasks_title"),
            description=self.get_text(interaction.user.id, "avatar_day_festival_tasks_desc"),
            color=discord.Color.gold()
        )
        
        # Day 1 Tasks
        day1_text = """**Day 1 - Login & Recruitment**
• Login 1 Day: 1x Aang Cookie, 1x Book of Experience (1.000), Resources
• Login 2 Days: 2x Aang Cookie, 2x Book of Experience (1.000), Resources
• Login 3 Days: 3x Aang Cookie, 1x Book of Experience (5.000), Resources
• Login 4 Days: 4x Aang Cookie, 1x Silver Scroll, Resources
• Login 5 Days: 5x Aang Cookie, 1x Golden Scroll, Resources
• Recruit 3.000 Benders: 1x Aang Cookie, Speedups, Resources
• Recruit 6.000 Benders: 3x Aang Cookie, Speedups, Resources
• Recruit 12.000 Benders: 5x Aang Cookie, 1x Silver Scroll, Speedups, Resources
• Recruit 20.000 Benders: 5x Aang Cookie, 1x Golden Scroll, Speedups, Resources"""
        
        embed.add_field(name="📅 Day 1", value=day1_text, inline=False)
        
        # Day 2 Tasks
        day2_text = """**Day 2 - AP Usage & Gathering**
• Use 500 AP: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Use 1.000 AP: 3x Aang Cookie, 1x Silver Scroll, Resources
• Use 2.000 AP: 5x Aang Cookie, 1x Golden Scroll, Resources
• Gather 100.000 resources: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Gather 200.000 resources: 2x Aang Cookie, 1x Silver Scroll, Speedups
• Gather 400.000 resources: 3x Aang Cookie, 1x Golden Scroll, Speedups
• Gather 800.000 resources: 5x Aang Cookie, 2x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 2", value=day2_text, inline=False)
        
        # Day 3 Tasks
        day3_text = """**Day 3 - Construction & Expeditions**
• Increase Power by 40.000 with Construction: 1x Aang Cookie, Speedups
• Increase Power by 80.000 with Construction: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 120.000 with Construction: 5x Aang Cookie, 1x Golden Scroll, Speedups
• Complete 10 Expedition missions: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Complete 20 Expedition missions: 3x Aang Cookie, 1x Silver Scroll, Resources
• Complete 30 Expedition missions: 5x Aang Cookie, 1x Golden Scroll, Resources"""
        
        embed.add_field(name="📅 Day 3", value=day3_text, inline=False)
        
        # Day 4 Tasks
        day4_text = """**Day 4 - Harvesting & Research**
• Harvest 10.000 resources in city: 1x Aang Cookie, 2x Book of Experience (1.000), Resources
• Harvest 50.000 resources in city: 2x Aang Cookie, 1x Book of Experience (5.000), Resources
• Harvest 100.000 resources in city: 3x Aang Cookie, 1x Silver Scroll, Resources
• Harvest 150.000 resources in city: 5x Aang Cookie, 1x Golden Scroll, Resources
• Increase Power by 20.000 with Research: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Increase Power by 40.000 with Research: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 60.000 with Research: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 4", value=day4_text, inline=False)
        
        # Day 5 Tasks
        day5_text = """**Day 5 - Shattered Skulls & Scrolls**
• Defeat Shattered Skulls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 10 times: 3x Aang Cookie, 2x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 20 times: 5x Aang Cookie, 1x Silver Scroll, Resources
• Defeat Shattered Skulls 30 times: 7x Aang Cookie, 1x Golden Scroll, Resources
• Use any Scrolls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Use any Scrolls 10 times: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Use any Scrolls 15 times: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 5", value=day5_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Exchange Shop", style=discord.ButtonStyle.secondary, emoji="🛒")
    async def show_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show the Avatar Day Festival Exchange Shop."""
        embed = discord.Embed(
            title="🛒 Avatar Day Festival Exchange Shop",
            description="Exchange your Aang Cookies for amazing rewards!",
            color=discord.Color.green()
        )
        
        # Basic Items (1 Cookie)
        basic_items = """**1 Cookie Items (10x each)**
• Speedup 60m
• 50.000 Food
• 50.000 Wood
• 50.000 Stone
• 25.000 Gold"""
        
        embed.add_field(name="🍪 1 Cookie", value=basic_items, inline=False)
        
        # Rare Items (2 Cookies)
        rare_items = """**2 Cookie Items (10x each)**
• Rare Spirit Shard
• Rare Spirit Badge
• Silver Scroll"""
        
        embed.add_field(name="🍪🍪 2 Cookies", value=rare_items, inline=False)
        
        # Spirit Shards (8 Cookies)
        spirit_shards = """**8 Cookie Items (10x each)**
• Spirit Shard: Zuko
• Spirit Shard: Katara
• Spirit Shard: Toph
• Spirit Shard: Tenzin"""
        
        embed.add_field(name="🍪🍪🍪🍪🍪🍪🍪🍪 8 Cookies", value=spirit_shards, inline=False)
        
        # Premium Items (10+ Cookies)
        premium_items = """**Premium Items**
• Golden Scroll (10 Cookies, 10x)
• Reset Talents (10 Cookies, 1x)
• Legendary Spirit Shard (30 Cookies, 2x)
• Legendary Spirit Badge (30 Cookies, 2x)"""
        
        embed.add_field(name="💎 Premium Items", value=premium_items, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Event Guide", style=discord.ButtonStyle.success, emoji="📖")
    async def show_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event guide and tips."""
        embed = discord.Embed(
            title="📖 Avatar Day Festival Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.blue()
        )
        
        guide_text = """**🎭 Event Overview**
• Duration: 7 Days (Shop only on the last day)
• Main Currency: Aang Cookies
• Goal: Complete daily tasks and exchange cookies for rewards

**📋 How to Participate**
1. **Daily Tasks**: Complete different goals each day
2. **Earn Cookies**: Receive Aang Cookies for completing tasks
3. **Exchange Rewards**: Use cookies at the Festival Exchange Shop
4. **Shop Access**: Exchange shop opens on the last day

**💡 Tips & Strategy**
• **Plan Ahead**: Check daily tasks and prepare resources
• **Focus on High-Value Tasks**: Prioritize tasks with Golden Scrolls
• **Resource Management**: Stock up on resources for construction/research tasks
• **AP Efficiency**: Use AP strategically for day 2 tasks
• **Expedition Preparation**: Have expedition missions ready for day 3
• **Scroll Usage**: Save scrolls for day 5 tasks
• **Cookie Exchange**: Plan which shop items to prioritize

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Legendary Spirit Shards/Badges (30 cookies each)
• Spirit Shards for specific heroes (8 cookies each)
• Reset Talents (10 cookies, limited quantity)"""
        
        from utils.embed_generator import EmbedGenerator
        EmbedGenerator.add_safe_field(embed, "Event Guide", guide_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="⬅️")
    async def go_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to main event overview."""
        embed = discord.Embed(
            title="🎭 Avatar Day Festival",
            description="Join in the festivities honoring avatars and enjoy amazing rewards!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="7 Days (Shop only on the last day)",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Weekly Festival",
            inline=True
        )
        
        embed.add_field(
            name="🍪 Main Currency",
            value="Aang Cookies",
            inline=True
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="Different goals each day throughout the festival",
            inline=False
        )
        
        embed.add_field(
            name="🛒 Exchange Shop",
            value="Trade Aang Cookies for amazing rewards including Spirit Shards, Scrolls, and more!",
            inline=False
        )
        
        embed.add_field(
            name="💡 Quick Tips",
            value="• Complete daily tasks to earn Aang Cookies\n• Plan your resource usage strategically\n• Exchange cookies for the best rewards on the final day\n• Focus on tasks with Golden Scroll rewards",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)

class AvatarDayFestival(commands.Cog):
    """Avatar Day Festival commands cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

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
    
    @app_commands.command(name="avatar_day_festival", description="Get comprehensive information about the Avatar Day Festival")
    async def avatar_day_festival(self, interaction: discord.Interaction):
        """Main command for Avatar Day Festival information."""
        embed = discord.Embed(
            title="🎭 Avatar Day Festival",
            description="Join in the festivities honoring avatars and enjoy amazing rewards!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="7 Days (Shop only on the last day)",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Weekly Festival",
            inline=True
        )
        
        embed.add_field(
            name="🍪 Main Currency",
            value="Aang Cookies",
            inline=True
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="Different goals each day throughout the festival",
            inline=False
        )
        
        embed.add_field(
            name="🛒 Exchange Shop",
            value="Trade Aang Cookies for amazing rewards including Spirit Shards, Scrolls, and more!",
            inline=False
        )
        
        embed.add_field(
            name="💡 Quick Tips",
            value="• Complete daily tasks to earn Aang Cookies\n• Plan your resource usage strategically\n• Exchange cookies for the best rewards on the final day\n• Focus on tasks with Golden Scroll rewards",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        # Create interactive view
        view = AvatarDayFestivalView()
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="festival_tasks", description="View all Avatar Day Festival tasks by day")
    async def festival_tasks(self, interaction: discord.Interaction):
        """Show all festival tasks organized by day."""
        embed = discord.Embed(
            title="📋 Avatar Day Festival - All Tasks",
            description="Complete these tasks to earn Aang Cookies!",
            color=discord.Color.blue()
        )
        
        # Day 1 Tasks
        day1_text = """**Day 1 - Login & Recruitment**
• Login 1 Day: 1x Aang Cookie, 1x Book of Experience (1.000), Resources
• Login 2 Days: 2x Aang Cookie, 2x Book of Experience (1.000), Resources
• Login 3 Days: 3x Aang Cookie, 1x Book of Experience (5.000), Resources
• Login 4 Days: 4x Aang Cookie, 1x Silver Scroll, Resources
• Login 5 Days: 5x Aang Cookie, 1x Golden Scroll, Resources
• Recruit 3.000 Benders: 1x Aang Cookie, Speedups, Resources
• Recruit 6.000 Benders: 3x Aang Cookie, Speedups, Resources
• Recruit 12.000 Benders: 5x Aang Cookie, 1x Silver Scroll, Speedups, Resources
• Recruit 20.000 Benders: 5x Aang Cookie, 1x Golden Scroll, Speedups, Resources"""
        
        embed.add_field(name="📅 Day 1", value=day1_text, inline=False)
        
        # Day 2 Tasks
        day2_text = """**Day 2 - AP Usage & Gathering**
• Use 500 AP: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Use 1.000 AP: 3x Aang Cookie, 1x Silver Scroll, Resources
• Use 2.000 AP: 5x Aang Cookie, 1x Golden Scroll, Resources
• Gather 100.000 resources: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Gather 200.000 resources: 2x Aang Cookie, 1x Silver Scroll, Speedups
• Gather 400.000 resources: 3x Aang Cookie, 1x Golden Scroll, Speedups
• Gather 800.000 resources: 5x Aang Cookie, 2x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 2", value=day2_text, inline=False)
        
        # Day 3 Tasks
        day3_text = """**Day 3 - Construction & Expeditions**
• Increase Power by 40.000 with Construction: 1x Aang Cookie, Speedups
• Increase Power by 80.000 with Construction: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 120.000 with Construction: 5x Aang Cookie, 1x Golden Scroll, Speedups
• Complete 10 Expedition missions: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Complete 20 Expedition missions: 3x Aang Cookie, 1x Silver Scroll, Resources
• Complete 30 Expedition missions: 5x Aang Cookie, 1x Golden Scroll, Resources"""
        
        embed.add_field(name="📅 Day 3", value=day3_text, inline=False)
        
        # Day 4 Tasks
        day4_text = """**Day 4 - Harvesting & Research**
• Harvest 10.000 resources in city: 1x Aang Cookie, 2x Book of Experience (1.000), Resources
• Harvest 50.000 resources in city: 2x Aang Cookie, 1x Book of Experience (5.000), Resources
• Harvest 100.000 resources in city: 3x Aang Cookie, 1x Silver Scroll, Resources
• Harvest 150.000 resources in city: 5x Aang Cookie, 1x Golden Scroll, Resources
• Increase Power by 20.000 with Research: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Increase Power by 40.000 with Research: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 60.000 with Research: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 4", value=day4_text, inline=False)
        
        # Day 5 Tasks
        day5_text = """**Day 5 - Shattered Skulls & Scrolls**
• Defeat Shattered Skulls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 10 times: 3x Aang Cookie, 2x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 20 times: 5x Aang Cookie, 1x Silver Scroll, Resources
• Defeat Shattered Skulls 30 times: 7x Aang Cookie, 1x Golden Scroll, Resources
• Use any Scrolls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Use any Scrolls 10 times: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Use any Scrolls 15 times: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 5", value=day5_text, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="festival_shop", description="View the Avatar Day Festival Exchange Shop")
    async def festival_shop(self, interaction: discord.Interaction):
        """Show the Avatar Day Festival Exchange Shop items."""
        embed = discord.Embed(
            title="🛒 Avatar Day Festival Exchange Shop",
            description="Exchange your Aang Cookies for amazing rewards!",
            color=discord.Color.green()
        )
        
        # Basic Items (1 Cookie)
        basic_items = """**1 Cookie Items (10x each)**
• Speedup 60m
• 50.000 Food
• 50.000 Wood
• 50.000 Stone
• 25.000 Gold"""
        
        embed.add_field(name="🍪 1 Cookie", value=basic_items, inline=False)
        
        # Rare Items (2 Cookies)
        rare_items = """**2 Cookie Items (10x each)**
• Rare Spirit Shard
• Rare Spirit Badge
• Silver Scroll"""
        
        embed.add_field(name="🍪🍪 2 Cookies", value=rare_items, inline=False)
        
        # Spirit Shards (8 Cookies)
        spirit_shards = """**8 Cookie Items (10x each)**
• Spirit Shard: Zuko
• Spirit Shard: Katara
• Spirit Shard: Toph
• Spirit Shard: Tenzin"""
        
        embed.add_field(name="🍪🍪🍪🍪🍪🍪🍪🍪 8 Cookies", value=spirit_shards, inline=False)
        
        # Premium Items (10+ Cookies)
        premium_items = """**Premium Items**
• Golden Scroll (10 Cookies, 10x)
• Reset Talents (10 Cookies, 1x)
• Legendary Spirit Shard (30 Cookies, 2x)
• Legendary Spirit Badge (30 Cookies, 2x)"""
        
        embed.add_field(name="💎 Premium Items", value=premium_items, inline=False)
        
        embed.add_field(
            name="💡 Shop Tips",
            value="• Shop opens on the last day of the festival\n• Plan your cookie spending in advance\n• Legendary items are limited quantity\n• Spirit Shards are great for specific hero progression",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="festival_guide", description="Get tips and strategy for the Avatar Day Festival")
    async def festival_guide(self, interaction: discord.Interaction):
        """Show comprehensive festival guide and tips."""
        embed = discord.Embed(
            title="📖 Avatar Day Festival Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.blue()
        )
        
        guide_text = """**🎭 Event Overview**
• Duration: 7 Days (Shop only on the last day)
• Main Currency: Aang Cookies
• Goal: Complete daily tasks and exchange cookies for rewards

**📋 How to Participate**
1. **Daily Tasks**: Complete different goals each day
2. **Earn Cookies**: Receive Aang Cookies for completing tasks
3. **Exchange Rewards**: Use cookies at the Festival Exchange Shop
4. **Shop Access**: Exchange shop opens on the last day

**💡 Tips & Strategy**
• **Plan Ahead**: Check daily tasks and prepare resources
• **Focus on High-Value Tasks**: Prioritize tasks with Golden Scrolls
• **Resource Management**: Stock up on resources for construction/research tasks
• **AP Efficiency**: Use AP strategically for day 2 tasks
• **Expedition Preparation**: Have expedition missions ready for day 3
• **Scroll Usage**: Save scrolls for day 5 tasks
• **Cookie Exchange**: Plan which shop items to prioritize

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Legendary Spirit Shards/Badges (30 cookies each)
• Spirit Shards for specific heroes (8 cookies each)
• Reset Talents (10 cookies, limited quantity)

**📊 Task Priority**
1. **Golden Scroll Tasks**: Highest priority for valuable rewards
2. **Silver Scroll Tasks**: Good secondary priority
3. **Resource Tasks**: Complete for basic progression
4. **Speedup Tasks**: Useful for ongoing development"""
        
        embed.add_field(name="Event Guide", value=guide_text, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="festival_rewards", description="View all possible rewards from the Avatar Day Festival")
    async def festival_rewards(self, interaction: discord.Interaction):
        """Show all possible rewards from the festival."""
        embed = discord.Embed(
            title="🏆 Avatar Day Festival - All Rewards",
            description="Complete tasks and exchange cookies for these amazing rewards!",
            color=discord.Color.gold()
        )
        
        # Task Rewards
        task_rewards = """**📋 Task Completion Rewards**
• **Aang Cookies**: Main currency for exchange shop
• **Books of Experience**: 1.000 and 5.000 XP variants
• **Silver Scrolls**: From high-tier tasks
• **Golden Scrolls**: From highest-tier tasks
• **Resources**: Food, Wood, Stone in various amounts
• **Speedups**: Construction, Recruitment, Research (5m and 60m)"""
        
        embed.add_field(name="Task Rewards", value=task_rewards, inline=False)
        
        # Exchange Shop Rewards
        shop_rewards = """**🛒 Exchange Shop Rewards**
• **Basic Items** (1 Cookie): Speedups, Resources, Gold
• **Rare Items** (2 Cookies): Rare Spirit Shards/Badges, Silver Scrolls
• **Hero Spirit Shards** (8 Cookies): Zuko, Katara, Toph, Tenzin
• **Premium Items** (10+ Cookies): Golden Scrolls, Reset Talents
• **Legendary Items** (30 Cookies): Legendary Spirit Shards/Badges"""
        
        embed.add_field(name="Shop Rewards", value=shop_rewards, inline=False)
        
        # Value Analysis
        value_analysis = """**💎 Highest Value Rewards**
• **Legendary Spirit Shards/Badges**: 30 cookies (limited quantity)
• **Reset Talents**: 10 cookies (limited quantity)
• **Golden Scrolls**: 10 cookies (multiple available)
• **Hero Spirit Shards**: 8 cookies (specific hero progression)
• **Silver Scrolls**: 2 cookies (good value for progression)"""
        
        embed.add_field(name="Value Analysis", value=value_analysis, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    # Traditional prefix commands
    @commands.command(name="avatar_day_festival", description="Get comprehensive information about the Avatar Day Festival")
    async def avatar_day_festival_prefix(self, ctx):
        """Traditional prefix command for Avatar Day Festival information."""
        embed = discord.Embed(
            title="🎭 Avatar Day Festival",
            description="Join in the festivities honoring avatars and enjoy amazing rewards!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="7 Days (Shop only on the last day)",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Weekly Festival",
            inline=True
        )
        
        embed.add_field(
            name="🍪 Main Currency",
            value="Aang Cookies",
            inline=True
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="Different goals each day throughout the festival",
            inline=False
        )
        
        embed.add_field(
            name="🛒 Exchange Shop",
            value="Trade Aang Cookies for amazing rewards including Spirit Shards, Scrolls, and more!",
            inline=False
        )
        
        embed.add_field(
            name="💡 Quick Tips",
            value="• Complete daily tasks to earn Aang Cookies\n• Plan your resource usage strategically\n• Exchange cookies for the best rewards on the final day\n• Focus on tasks with Golden Scroll rewards",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="festival_tasks", description="View all Avatar Day Festival tasks by day")
    async def festival_tasks_prefix(self, ctx):
        """Traditional prefix command to show all festival tasks organized by day."""
        embed = discord.Embed(
            title="📋 Avatar Day Festival - All Tasks",
            description="Complete these tasks to earn Aang Cookies!",
            color=discord.Color.blue()
        )
        
        # Day 1 Tasks
        day1_text = """**Day 1 - Login & Recruitment**
• Login 1 Day: 1x Aang Cookie, 1x Book of Experience (1.000), Resources
• Login 2 Days: 2x Aang Cookie, 2x Book of Experience (1.000), Resources
• Login 3 Days: 3x Aang Cookie, 1x Book of Experience (5.000), Resources
• Login 4 Days: 4x Aang Cookie, 1x Silver Scroll, Resources
• Login 5 Days: 5x Aang Cookie, 1x Golden Scroll, Resources
• Recruit 3.000 Benders: 1x Aang Cookie, Speedups, Resources
• Recruit 6.000 Benders: 3x Aang Cookie, Speedups, Resources
• Recruit 12.000 Benders: 5x Aang Cookie, 1x Silver Scroll, Speedups, Resources
• Recruit 20.000 Benders: 5x Aang Cookie, 1x Golden Scroll, Speedups, Resources"""
        
        embed.add_field(name="📅 Day 1", value=day1_text, inline=False)
        
        # Day 2 Tasks
        day2_text = """**Day 2 - AP Usage & Gathering**
• Use 500 AP: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Use 1.000 AP: 3x Aang Cookie, 1x Silver Scroll, Resources
• Use 2.000 AP: 5x Aang Cookie, 1x Golden Scroll, Resources
• Gather 100.000 resources: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Gather 200.000 resources: 2x Aang Cookie, 1x Silver Scroll, Speedups
• Gather 400.000 resources: 3x Aang Cookie, 1x Golden Scroll, Speedups
• Gather 800.000 resources: 5x Aang Cookie, 2x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 2", value=day2_text, inline=False)
        
        # Day 3 Tasks
        day3_text = """**Day 3 - Construction & Expeditions**
• Increase Power by 40.000 with Construction: 1x Aang Cookie, Speedups
• Increase Power by 80.000 with Construction: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 120.000 with Construction: 5x Aang Cookie, 1x Golden Scroll, Speedups
• Complete 10 Expedition missions: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Complete 20 Expedition missions: 3x Aang Cookie, 1x Silver Scroll, Resources
• Complete 30 Expedition missions: 5x Aang Cookie, 1x Golden Scroll, Resources"""
        
        embed.add_field(name="📅 Day 3", value=day3_text, inline=False)
        
        # Day 4 Tasks
        day4_text = """**Day 4 - Harvesting & Research**
• Harvest 10.000 resources in city: 1x Aang Cookie, 2x Book of Experience (1.000), Resources
• Harvest 50.000 resources in city: 2x Aang Cookie, 1x Book of Experience (5.000), Resources
• Harvest 100.000 resources in city: 3x Aang Cookie, 1x Silver Scroll, Resources
• Harvest 150.000 resources in city: 5x Aang Cookie, 1x Golden Scroll, Resources
• Increase Power by 20.000 with Research: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Increase Power by 40.000 with Research: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Increase Power by 60.000 with Research: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 4", value=day4_text, inline=False)
        
        # Day 5 Tasks
        day5_text = """**Day 5 - Shattered Skulls & Scrolls**
• Defeat Shattered Skulls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 10 times: 3x Aang Cookie, 2x Book of Experience (5.000), Resources
• Defeat Shattered Skulls 20 times: 5x Aang Cookie, 1x Silver Scroll, Resources
• Defeat Shattered Skulls 30 times: 7x Aang Cookie, 1x Golden Scroll, Resources
• Use any Scrolls 5 times: 1x Aang Cookie, 1x Book of Experience (5.000), Speedups
• Use any Scrolls 10 times: 3x Aang Cookie, 1x Silver Scroll, Speedups
• Use any Scrolls 15 times: 5x Aang Cookie, 1x Golden Scroll, Speedups"""
        
        embed.add_field(name="📅 Day 5", value=day5_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="festival_shop", description="View the Avatar Day Festival Exchange Shop")
    async def festival_shop_prefix(self, ctx):
        """Traditional prefix command to show the Avatar Day Festival Exchange Shop items."""
        embed = discord.Embed(
            title="🛒 Avatar Day Festival Exchange Shop",
            description="Exchange your Aang Cookies for amazing rewards!",
            color=discord.Color.green()
        )
        
        # Basic Items (1 Cookie)
        basic_items = """**1 Cookie Items (10x each)**
• Speedup 60m
• 50.000 Food
• 50.000 Wood
• 50.000 Stone
• 25.000 Gold"""
        
        embed.add_field(name="🍪 1 Cookie", value=basic_items, inline=False)
        
        # Rare Items (2 Cookies)
        rare_items = """**2 Cookie Items (10x each)**
• Rare Spirit Shard
• Rare Spirit Badge
• Silver Scroll"""
        
        embed.add_field(name="🍪🍪 2 Cookies", value=rare_items, inline=False)
        
        # Spirit Shards (8 Cookies)
        spirit_shards = """**8 Cookie Items (10x each)**
• Spirit Shard: Zuko
• Spirit Shard: Katara
• Spirit Shard: Toph
• Spirit Shard: Tenzin"""
        
        embed.add_field(name="🍪🍪🍪🍪🍪🍪🍪🍪 8 Cookies", value=spirit_shards, inline=False)
        
        # Premium Items (10+ Cookies)
        premium_items = """**Premium Items**
• Golden Scroll (10 Cookies, 10x)
• Reset Talents (10 Cookies, 1x)
• Legendary Spirit Shard (30 Cookies, 2x)
• Legendary Spirit Badge (30 Cookies, 2x)"""
        
        embed.add_field(name="💎 Premium Items", value=premium_items, inline=False)
        
        embed.add_field(
            name="💡 Shop Tips",
            value="• Shop opens on the last day of the festival\n• Plan your cookie spending in advance\n• Legendary items are limited quantity\n• Spirit Shards are great for specific hero progression",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="festival_guide", description="Get tips and strategy for the Avatar Day Festival")
    async def festival_guide_prefix(self, ctx):
        """Traditional prefix command to show comprehensive festival guide and tips."""
        embed = discord.Embed(
            title="📖 Avatar Day Festival Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.blue()
        )
        
        guide_text = """**🎭 Event Overview**
• Duration: 7 Days (Shop only on the last day)
• Main Currency: Aang Cookies
• Goal: Complete daily tasks and exchange cookies for rewards

**📋 How to Participate**
1. **Daily Tasks**: Complete different goals each day
2. **Earn Cookies**: Receive Aang Cookies for completing tasks
3. **Exchange Rewards**: Use cookies at the Festival Exchange Shop
4. **Shop Access**: Exchange shop opens on the last day

**💡 Tips & Strategy**
• **Plan Ahead**: Check daily tasks and prepare resources
• **Focus on High-Value Tasks**: Prioritize tasks with Golden Scrolls
• **Resource Management**: Stock up on resources for construction/research tasks
• **AP Efficiency**: Use AP strategically for day 2 tasks
• **Expedition Preparation**: Have expedition missions ready for day 3
• **Scroll Usage**: Save scrolls for day 5 tasks
• **Cookie Exchange**: Plan which shop items to prioritize

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Legendary Spirit Shards/Badges (30 cookies each)
• Spirit Shards for specific heroes (8 cookies each)
• Reset Talents (10 cookies, limited quantity)

**📊 Task Priority**
1. **Golden Scroll Tasks**: Highest priority for valuable rewards
2. **Silver Scroll Tasks**: Good secondary priority
3. **Resource Tasks**: Complete for basic progression
4. **Speedup Tasks**: Useful for ongoing development"""
        
        embed.add_field(name="Event Guide", value=guide_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="festival_rewards", description="View all possible rewards from the Avatar Day Festival")
    async def festival_rewards_prefix(self, ctx):
        """Traditional prefix command to show all possible rewards from the festival."""
        embed = discord.Embed(
            title="🏆 Avatar Day Festival - All Rewards",
            description="Complete tasks and exchange cookies for these amazing rewards!",
            color=discord.Color.gold()
        )
        
        # Task Rewards
        task_rewards = """**📋 Task Completion Rewards**
• **Aang Cookies**: Main currency for exchange shop
• **Books of Experience**: 1.000 and 5.000 XP variants
• **Silver Scrolls**: From high-tier tasks
• **Golden Scrolls**: From highest-tier tasks
• **Resources**: Food, Wood, Stone in various amounts
• **Speedups**: Construction, Recruitment, Research (5m and 60m)"""
        
        embed.add_field(name="Task Rewards", value=task_rewards, inline=False)
        
        # Exchange Shop Rewards
        shop_rewards = """**🛒 Exchange Shop Rewards**
• **Basic Items** (1 Cookie): Speedups, Resources, Gold
• **Rare Items** (2 Cookies): Rare Spirit Shards/Badges, Silver Scrolls
• **Hero Spirit Shards** (8 Cookies): Zuko, Katara, Toph, Tenzin
• **Premium Items** (10+ Cookies): Golden Scrolls, Reset Talents
• **Legendary Items** (30 Cookies): Legendary Spirit Shards/Badges"""
        
        embed.add_field(name="Shop Rewards", value=shop_rewards, inline=False)
        
        # Value Analysis
        value_analysis = """**💎 Highest Value Rewards**
• **Legendary Spirit Shards/Badges**: 30 cookies (limited quantity)
• **Reset Talents**: 10 cookies (limited quantity)
• **Golden Scrolls**: 10 cookies (multiple available)
• **Hero Spirit Shards**: 8 cookies (specific hero progression)
• **Silver Scrolls**: 2 cookies (good value for progression)"""
        
        embed.add_field(name="Value Analysis", value=value_analysis, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(AvatarDayFestival(bot)) 