"""
Balance and Order commands cog for the Avatar Realms Collide Discord Bot.
Provides comprehensive information about the Balance and Order event.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class BalanceAndOrderView(discord.ui.View):
    """Interactive view for Balance and Order details with buttons."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
    
    @discord.ui.button(label="Event Tasks", style=discord.ButtonStyle.primary, emoji="📋")
    async def show_tasks(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event tasks and rewards."""
        embed = discord.Embed(
            title="⚖️ Balance and Order - Event Tasks",
            description="Complete these tasks to earn rewards!",
            color=discord.Color.blue()
        )
        
        tasks_text = """**📋 Available Tasks**
• Recruit 2.000 Benders: 1x Silver Scroll, 1x 10.000 Food, 1x 10.000 Wood, 1x 10.000 Stone
• Recruit 6.000 Benders: 1x Golden Scroll, 30x 10.000 Food, 3x 10.000 Wood, 3x 10.000 Stone
• Defeat Shattered Skulls 3 times: 1x Rare Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Defeat Shattered Skulls 10 times: 1x Epic Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Gather 100.000 resources from the field: 1x Silver Scroll, 1x Construction Speedup 5m, 1x Recruitment Speedup 5m, 1x Research Speedup 5m
• Gather 300.000 resources from the field: 1x Golden Scroll, 3x Construction Speedup 5m, 3x Recruitment Speedup 5m, 3x Research Speedup 5m"""
        
        embed.add_field(name="Event Tasks", value=tasks_text, inline=False)
        
        embed.add_field(
            name="💡 Important Note",
            value="**Unbreakable Will resets every day at 00:00 UTC**",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Event Guide", style=discord.ButtonStyle.success, emoji="📖")
    async def show_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event guide and tips."""
        embed = discord.Embed(
            title="📖 Balance and Order Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.green()
        )
        
        guide_text = """**⚖️ Event Overview**
• Duration: 3 Days
• Goal: Maintain balance and order through various activities
• Daily Reset: Unbreakable Will resets every day at 00:00 UTC

**📋 How to Participate**
1. **Resource Gathering**: Collect resources from the field
2. **Bender Recruitment**: Recruit benders to strengthen your forces
3. **Combat**: Defeat Shattered Skulls to prove your strength
4. **Complete Tasks**: Reach goals to earn rewards

**💡 Tips & Strategy**
• **Plan Daily**: Tasks reset daily, so plan your activities accordingly
• **Resource Management**: Focus on gathering resources efficiently
• **Combat Preparation**: Prepare for Shattered Skulls battles
• **Alliance Coordination**: Work with your alliance for better results
• **Time Management**: Take advantage of the daily reset system

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Epic Spirit Shards (from defeating Shattered Skulls)
• Silver Scrolls (from basic tasks)
• Speedups (for ongoing development)"""
        
        embed.add_field(name="Event Guide", value=guide_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="⬅️")
    async def go_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to main event overview."""
        embed = discord.Embed(
            title="⚖️ Balance and Order",
            description="You are the guardians of balance and order.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="3 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="💡 Daily Reset",
            value="Unbreakable Will resets every day at 00:00 UTC",
            inline=False
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="• Resource gathering from the field\n• Bender recruitment\n• Defeat Shattered Skulls\n• Complete goals for rewards",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• Silver and Golden Scrolls\n• Spirit Shards (Rare and Epic)\n• Resources (Food, Wood, Stone)\n• Speedups (Construction, Recruitment, Research)",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)

class BalanceAndOrder(commands.Cog):
    """Balance and Order commands cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @app_commands.command(name="balance_and_order", description="Get comprehensive information about the Balance and Order event")
    async def balance_and_order(self, interaction: discord.Interaction):
        """Main command for Balance and Order information."""
        embed = discord.Embed(
            title="⚖️ Balance and Order",
            description="You are the guardians of balance and order.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="3 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="💡 Daily Reset",
            value="Unbreakable Will resets every day at 00:00 UTC",
            inline=False
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="• Resource gathering from the field\n• Bender recruitment\n• Defeat Shattered Skulls\n• Complete goals for rewards",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• Silver and Golden Scrolls\n• Spirit Shards (Rare and Epic)\n• Resources (Food, Wood, Stone)\n• Speedups (Construction, Recruitment, Research)",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        # Create interactive view
        view = BalanceAndOrderView()
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="balance_tasks", description="View all Balance and Order event tasks")
    async def balance_tasks(self, interaction: discord.Interaction):
        """Show all Balance and Order event tasks."""
        embed = discord.Embed(
            title="📋 Balance and Order - Event Tasks",
            description="Complete these tasks to earn rewards!",
            color=discord.Color.blue()
        )
        
        tasks_text = """**📋 Available Tasks**
• Recruit 2.000 Benders: 1x Silver Scroll, 1x 10.000 Food, 1x 10.000 Wood, 1x 10.000 Stone
• Recruit 6.000 Benders: 1x Golden Scroll, 30x 10.000 Food, 3x 10.000 Wood, 3x 10.000 Stone
• Defeat Shattered Skulls 3 times: 1x Rare Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Defeat Shattered Skulls 10 times: 1x Epic Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Gather 100.000 resources from the field: 1x Silver Scroll, 1x Construction Speedup 5m, 1x Recruitment Speedup 5m, 1x Research Speedup 5m
• Gather 300.000 resources from the field: 1x Golden Scroll, 3x Construction Speedup 5m, 3x Recruitment Speedup 5m, 3x Research Speedup 5m"""
        
        embed.add_field(name="Event Tasks", value=tasks_text, inline=False)
        
        embed.add_field(
            name="💡 Important Note",
            value="**Unbreakable Will resets every day at 00:00 UTC**",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="balance_guide", description="Get tips and strategy for the Balance and Order event")
    async def balance_guide(self, interaction: discord.Interaction):
        """Show comprehensive Balance and Order guide and tips."""
        embed = discord.Embed(
            title="📖 Balance and Order Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.green()
        )
        
        guide_text = """**⚖️ Event Overview**
• Duration: 3 Days
• Goal: Maintain balance and order through various activities
• Daily Reset: Unbreakable Will resets every day at 00:00 UTC

**📋 How to Participate**
1. **Resource Gathering**: Collect resources from the field
2. **Bender Recruitment**: Recruit benders to strengthen your forces
3. **Combat**: Defeat Shattered Skulls to prove your strength
4. **Complete Tasks**: Reach goals to earn rewards

**💡 Tips & Strategy**
• **Plan Daily**: Tasks reset daily, so plan your activities accordingly
• **Resource Management**: Focus on gathering resources efficiently
• **Combat Preparation**: Prepare for Shattered Skulls battles
• **Alliance Coordination**: Work with your alliance for better results
• **Time Management**: Take advantage of the daily reset system

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Epic Spirit Shards (from defeating Shattered Skulls)
• Silver Scrolls (from basic tasks)
• Speedups (for ongoing development)

**📊 Task Priority**
1. **Golden Scroll Tasks**: Highest priority for valuable rewards
2. **Epic Spirit Shard Tasks**: Great for hero progression
3. **Silver Scroll Tasks**: Good secondary priority
4. **Resource Tasks**: Complete for basic progression"""
        
        embed.add_field(name="Event Guide", value=guide_text, inline=False)
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    # Traditional prefix commands
    @commands.command(name="balance_and_order", description="Get comprehensive information about the Balance and Order event")
    async def balance_and_order_prefix(self, ctx):
        """Traditional prefix command for Balance and Order information."""
        embed = discord.Embed(
            title="⚖️ Balance and Order",
            description="You are the guardians of balance and order.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="3 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="💡 Daily Reset",
            value="Unbreakable Will resets every day at 00:00 UTC",
            inline=False
        )
        
        embed.add_field(
            name="📋 Event Tasks",
            value="• Resource gathering from the field\n• Bender recruitment\n• Defeat Shattered Skulls\n• Complete goals for rewards",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• Silver and Golden Scrolls\n• Spirit Shards (Rare and Epic)\n• Resources (Food, Wood, Stone)\n• Speedups (Construction, Recruitment, Research)",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="balance_tasks", description="View all Balance and Order event tasks")
    async def balance_tasks_prefix(self, ctx):
        """Traditional prefix command to show all Balance and Order event tasks."""
        embed = discord.Embed(
            title="📋 Balance and Order - Event Tasks",
            description="Complete these tasks to earn rewards!",
            color=discord.Color.blue()
        )
        
        tasks_text = """**📋 Available Tasks**
• Recruit 2.000 Benders: 1x Silver Scroll, 1x 10.000 Food, 1x 10.000 Wood, 1x 10.000 Stone
• Recruit 6.000 Benders: 1x Golden Scroll, 30x 10.000 Food, 3x 10.000 Wood, 3x 10.000 Stone
• Defeat Shattered Skulls 3 times: 1x Rare Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Defeat Shattered Skulls 10 times: 1x Epic Spirit Shard, 1x 50.000 Food, 1x 50.000 Wood, 1x 50.000 Stone
• Gather 100.000 resources from the field: 1x Silver Scroll, 1x Construction Speedup 5m, 1x Recruitment Speedup 5m, 1x Research Speedup 5m
• Gather 300.000 resources from the field: 1x Golden Scroll, 3x Construction Speedup 5m, 3x Recruitment Speedup 5m, 3x Research Speedup 5m"""
        
        embed.add_field(name="Event Tasks", value=tasks_text, inline=False)
        
        embed.add_field(
            name="💡 Important Note",
            value="**Unbreakable Will resets every day at 00:00 UTC**",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="balance_guide", description="Get tips and strategy for the Balance and Order event")
    async def balance_guide_prefix(self, ctx):
        """Traditional prefix command to show comprehensive Balance and Order guide and tips."""
        embed = discord.Embed(
            title="📖 Balance and Order Guide",
            description="How to participate and maximize your rewards!",
            color=discord.Color.green()
        )
        
        guide_text = """**⚖️ Event Overview**
• Duration: 3 Days
• Goal: Maintain balance and order through various activities
• Daily Reset: Unbreakable Will resets every day at 00:00 UTC

**📋 How to Participate**
1. **Resource Gathering**: Collect resources from the field
2. **Bender Recruitment**: Recruit benders to strengthen your forces
3. **Combat**: Defeat Shattered Skulls to prove your strength
4. **Complete Tasks**: Reach goals to earn rewards

**💡 Tips & Strategy**
• **Plan Daily**: Tasks reset daily, so plan your activities accordingly
• **Resource Management**: Focus on gathering resources efficiently
• **Combat Preparation**: Prepare for Shattered Skulls battles
• **Alliance Coordination**: Work with your alliance for better results
• **Time Management**: Take advantage of the daily reset system

**🏆 Best Rewards**
• Golden Scrolls (from high-tier tasks)
• Epic Spirit Shards (from defeating Shattered Skulls)
• Silver Scrolls (from basic tasks)
• Speedups (for ongoing development)

**📊 Task Priority**
1. **Golden Scroll Tasks**: Highest priority for valuable rewards
2. **Epic Spirit Shard Tasks**: Great for hero progression
3. **Silver Scroll Tasks**: Good secondary priority
4. **Resource Tasks**: Complete for basic progression"""
        
        embed.add_field(name="Event Guide", value=guide_text, inline=False)
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(BalanceAndOrder(bot)) 