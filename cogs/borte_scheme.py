"""
Borte's Scheme commands cog for the Avatar Realms Collide Discord Bot.
Provides comprehensive information about the Borte's Scheme event.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class BorteSchemeView(discord.ui.View):
    """Interactive view for Borte's Scheme details with buttons."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
    
    @discord.ui.button(label="Event Mechanics", style=discord.ButtonStyle.primary, emoji="⚙️")
    async def show_mechanics(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event mechanics and how to participate."""
        embed = discord.Embed(
            title=self.get_text(interaction.user.id, "borte_scheme_mechanics_title"),
            description=self.get_text(interaction.user.id, "borte_scheme_mechanics_desc"),
            color=discord.Color.purple()
        )
        
        mechanics_text = """**⚙️ Event Mechanics**
1. **Defeat Shattered Skulls**: During the event period, defeating Shattered Skulls on the field will grant you Borte's Drum and Beads
2. **Use Borte's Drum**: Using Borte's Drum from your inventory will summon Borte's Berserkers
3. **Use Borte's Beads**: Using Borte's Beads will summon Elite Borte's Berserkers on the field
4. **Rally Battles**: Defeat Borte in rallies alongside alliance members to obtain Spirit Shard: Borte
5. **Performance Rewards**: Spirit Shard: Borte will be distributed differentially based on performance in rally battles"""
        
        embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        embed.add_field(
            name="💡 Strategy Tips",
            value="• Coordinate with your alliance for rally battles\n• Only put 1 hero in your rallies so that as many people as possible can join\n• Use drums and beads strategically\n• Focus on high-performance rally participation\n• Plan your resource usage for battles",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Event Rewards", style=discord.ButtonStyle.secondary, emoji="🏆")
    async def show_rewards(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event rewards."""
        embed = discord.Embed(
            title="🏆 Borte's Scheme - Event Rewards",
            description="Rewards for participating in Borte's Scheme",
            color=discord.Color.gold()
        )
        
        rewards_text = """**🏆 Event Rewards**
• 3x Spirit Shard: Borte
• 2x Research Speedup 5m
• 2x Recruitment Speedup 5m
• 1x 50.000 Food
• 1x 50.000 Wood

**💎 Spirit Shard Distribution**
• Spirit Shard: Borte is distributed based on rally battle performance
• Higher performance = more spirit shards
• Coordinate with alliance for maximum rewards"""
        
        embed.add_field(name="Event Rewards", value=rewards_text, inline=False)
        
        embed.add_field(
            name="🎯 Performance Tips",
            value="• Only put 1 hero in your rallies so that as many people as possible can join\n• Participate actively in rally battles\n• Coordinate with alliance members\n• Use strategic timing for battles\n• Focus on high-damage output",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Event Guide", style=discord.ButtonStyle.success, emoji="📖")
    async def show_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event guide and lore."""
        embed = discord.Embed(
            title="📖 Borte's Scheme Guide",
            description="The story and strategy behind Borte's Scheme",
            color=discord.Color.blue()
        )
        
        # Break the guide into multiple fields to avoid Discord's 1024 character limit
        lore_text = """**🎭 Event Lore**
Borte was once a slave girl offered as a sacrifice to Father Glowworm, but through her cunning and deceit, she rose to become the corrupt high priestess of a temple that guides fanatics. However, her thirst for Power knows no bounds. It seems she now seeks to oust Chanyu and even aims for the mocking throne. They say the enemy of your enemy is your friend. Leveraging Borte's insatiable greed might just aid in purging the corruption entrenched in this land."""
        
        participation_text = """**📋 How to Participate**
1. **Field Combat**: Defeat Shattered Skulls on the field to earn Borte's Drum and Beads
2. **Summon Allies**: Use drums and beads to summon Borte's Berserkers and Elite Berserkers
3. **Rally Battles**: Join alliance rallies to defeat Borte herself
4. **Earn Rewards**: Receive Spirit Shard: Borte based on rally performance"""
        
        tips_text = """**💡 Tips & Strategy**
• **Alliance Coordination**: Work closely with your alliance for rally battles
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **Resource Management**: Use drums and beads strategically
• **Timing**: Choose the right moments to summon berserkers
• **Performance**: Focus on high-damage output in rally battles
• **Communication**: Coordinate rally timing with alliance members"""
        
        strategy_text = """**🏆 Best Strategy**
• **Active Participation**: Join as many rally battles as possible
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **High Performance**: Maximize your damage output in battles
• **Alliance Support**: Help coordinate rally timing and strategy
• **Resource Efficiency**: Use drums and beads at optimal times"""
        
        embed.add_field(name="Event Lore", value=lore_text, inline=False)
        embed.add_field(name="How to Participate", value=participation_text, inline=False)
        embed.add_field(name="Tips & Strategy", value=tips_text, inline=False)
        embed.add_field(name="Best Strategy", value=strategy_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="⬅️")
    async def go_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to main event overview."""
        embed = discord.Embed(
            title="🎭 Borte's Scheme",
            description="Borte, a slave girl who was almost sacrificed to Father Glowworm, has now become a high priest of the Shattered Skulls and is seeking the throne of Murong. Harnessing her lust for power, she may be able to help purify the land.",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="2 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Main Goal",
            value="Defeat Borte in rallies alongside alliance members",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• 3x Spirit Shard: Borte\n• Speedups (Research, Recruitment)\n• Resources (Food, Wood)\n• Performance-based distribution",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)

class BorteScheme(commands.Cog):
    """Borte's Scheme commands cog."""
    
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
    
    @app_commands.command(name="borte_scheme", description="Get comprehensive information about Borte's Scheme event")
    async def borte_scheme(self, interaction: discord.Interaction):
        """Main command for Borte's Scheme information."""
        embed = discord.Embed(
            title="🎭 Borte's Scheme",
            description="Borte, a slave girl who was almost sacrificed to Father Glowworm, has now become a high priest of the Shattered Skulls and is seeking the throne of Murong. Harnessing her lust for power, she may be able to help purify the land.",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="2 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Main Goal",
            value="Defeat Borte in rallies alongside alliance members",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• 3x Spirit Shard: Borte\n• Speedups (Research, Recruitment)\n• Resources (Food, Wood)\n• Performance-based distribution",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        # Create interactive view
        view = BorteSchemeView()
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="borte_mechanics", description="View Borte's Scheme event mechanics")
    async def borte_mechanics(self, interaction: discord.Interaction):
        """Show Borte's Scheme event mechanics."""
        embed = discord.Embed(
            title="⚙️ Borte's Scheme - Event Mechanics",
            description="How to participate in Borte's Scheme event",
            color=discord.Color.purple()
        )
        
        mechanics_text = """**⚙️ Event Mechanics**
1. **Defeat Shattered Skulls**: During the event period, defeating Shattered Skulls on the field will grant you Borte's Drum and Beads
2. **Use Borte's Drum**: Using Borte's Drum from your inventory will summon Borte's Berserkers
3. **Use Borte's Beads**: Using Borte's Beads will summon Elite Borte's Berserkers on the field
4. **Rally Battles**: Defeat Borte in rallies alongside alliance members to obtain Spirit Shard: Borte
5. **Performance Rewards**: Spirit Shard: Borte will be distributed differentially based on performance in rally battles"""
        
        embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        embed.add_field(
            name="💡 Strategy Tips",
            value="• Coordinate with your alliance for rally battles\n• Only put 1 hero in your rallies so that as many people as possible can join\n• Use drums and beads strategically\n• Focus on high-performance rally participation\n• Plan your resource usage for battles",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="borte_rewards", description="View Borte's Scheme event rewards")
    async def borte_rewards(self, interaction: discord.Interaction):
        """Show Borte's Scheme event rewards."""
        embed = discord.Embed(
            title="🏆 Borte's Scheme - Event Rewards",
            description="Rewards for participating in Borte's Scheme",
            color=discord.Color.gold()
        )
        
        rewards_text = """**🏆 Event Rewards**
• 3x Spirit Shard: Borte
• 2x Research Speedup 5m
• 2x Recruitment Speedup 5m
• 1x 50.000 Food
• 1x 50.000 Wood

**💎 Spirit Shard Distribution**
• Spirit Shard: Borte is distributed based on rally battle performance
• Higher performance = more spirit shards
• Coordinate with alliance for maximum rewards"""
        
        embed.add_field(name="Event Rewards", value=rewards_text, inline=False)
        
        embed.add_field(
            name="🎯 Performance Tips",
            value="• Only put 1 hero in your rallies so that as many people as possible can join\n• Participate actively in rally battles\n• Coordinate with alliance members\n• Use strategic timing for battles\n• Focus on high-damage output",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="borte_guide", description="Get tips and strategy for Borte's Scheme")
    async def borte_guide(self, interaction: discord.Interaction):
        """Show comprehensive Borte's Scheme guide and tips."""
        embed = discord.Embed(
            title="📖 Borte's Scheme Guide",
            description="The story and strategy behind Borte's Scheme",
            color=discord.Color.blue()
        )
        
        # Break the guide into multiple fields to avoid Discord's 1024 character limit
        lore_text = """**🎭 Event Lore**
Borte was once a slave girl offered as a sacrifice to Father Glowworm, but through her cunning and deceit, she rose to become the corrupt high priestess of a temple that guides fanatics. However, her thirst for Power knows no bounds. It seems she now seeks to oust Chanyu and even aims for the mocking throne. They say the enemy of your enemy is your friend. Leveraging Borte's insatiable greed might just aid in purging the corruption entrenched in this land."""
        
        participation_text = """**📋 How to Participate**
1. **Field Combat**: Defeat Shattered Skulls on the field to earn Borte's Drum and Beads
2. **Summon Allies**: Use drums and beads to summon Borte's Berserkers and Elite Berserkers
3. **Rally Battles**: Join alliance rallies to defeat Borte herself
4. **Earn Rewards**: Receive Spirit Shard: Borte based on rally performance"""
        
        tips_text = """**💡 Tips & Strategy**
• **Alliance Coordination**: Work closely with your alliance for rally battles
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **Resource Management**: Use drums and beads strategically
• **Timing**: Choose the right moments to summon berserkers
• **Performance**: Focus on high-damage output in rally battles
• **Communication**: Coordinate rally timing with alliance members"""
        
        strategy_text = """**🏆 Best Strategy**
• **Active Participation**: Join as many rally battles as possible
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **High Performance**: Maximize your damage output in battles
• **Alliance Support**: Help coordinate rally timing and strategy
• **Resource Efficiency**: Use drums and beads at optimal times"""
        
        priority_text = """**📊 Performance Priority**
1. **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
2. **Rally Participation**: Join all available rally battles
3. **Damage Output**: Maximize your contribution in battles
4. **Alliance Coordination**: Work with alliance for optimal timing
5. **Resource Usage**: Use drums and beads efficiently"""
        
        embed.add_field(name="Event Lore", value=lore_text, inline=False)
        embed.add_field(name="How to Participate", value=participation_text, inline=False)
        embed.add_field(name="Tips & Strategy", value=tips_text, inline=False)
        embed.add_field(name="Best Strategy", value=strategy_text, inline=False)
        embed.add_field(name="Performance Priority", value=priority_text, inline=False)
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    # Traditional prefix commands
    @commands.command(name="borte_scheme", description="Get comprehensive information about Borte's Scheme event")
    async def borte_scheme_prefix(self, ctx):
        """Traditional prefix command for Borte's Scheme information."""
        embed = discord.Embed(
            title="🎭 Borte's Scheme",
            description="Borte, a slave girl who was almost sacrificed to Father Glowworm, has now become a high priest of the Shattered Skulls and is seeking the throne of Murong. Harnessing her lust for power, she may be able to help purify the land.",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="⏳ Duration",
            value="2 Days",
            inline=True
        )
        
        embed.add_field(
            name="🔁 Repeats",
            value="Periodic Event",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Main Goal",
            value="Defeat Borte in rallies alongside alliance members",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Rewards",
            value="• 3x Spirit Shard: Borte\n• Speedups (Research, Recruitment)\n• Resources (Food, Wood)\n• Performance-based distribution",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="borte_mechanics", description="View Borte's Scheme event mechanics")
    async def borte_mechanics_prefix(self, ctx):
        """Traditional prefix command to show Borte's Scheme event mechanics."""
        embed = discord.Embed(
            title="⚙️ Borte's Scheme - Event Mechanics",
            description="How to participate in Borte's Scheme event",
            color=discord.Color.purple()
        )
        
        mechanics_text = """**⚙️ Event Mechanics**
1. **Defeat Shattered Skulls**: During the event period, defeating Shattered Skulls on the field will grant you Borte's Drum and Beads
2. **Use Borte's Drum**: Using Borte's Drum from your inventory will summon Borte's Berserkers
3. **Use Borte's Beads**: Using Borte's Beads will summon Elite Borte's Berserkers on the field
4. **Rally Battles**: Defeat Borte in rallies alongside alliance members to obtain Spirit Shard: Borte
5. **Performance Rewards**: Spirit Shard: Borte will be distributed differentially based on performance in rally battles"""
        
        embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        embed.add_field(
            name="💡 Strategy Tips",
            value="• Coordinate with your alliance for rally battles\n• Only put 1 hero in your rallies so that as many people as possible can join\n• Use drums and beads strategically\n• Focus on high-performance rally participation\n• Plan your resource usage for battles",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="borte_rewards", description="View Borte's Scheme event rewards")
    async def borte_rewards_prefix(self, ctx):
        """Traditional prefix command to show Borte's Scheme event rewards."""
        embed = discord.Embed(
            title="🏆 Borte's Scheme - Event Rewards",
            description="Rewards for participating in Borte's Scheme",
            color=discord.Color.gold()
        )
        
        rewards_text = """**🏆 Event Rewards**
• 3x Spirit Shard: Borte
• 2x Research Speedup 5m
• 2x Recruitment Speedup 5m
• 1x 50.000 Food
• 1x 50.000 Wood

**💎 Spirit Shard Distribution**
• Spirit Shard: Borte is distributed based on rally battle performance
• Higher performance = more spirit shards
• Coordinate with alliance for maximum rewards"""
        
        embed.add_field(name="Event Rewards", value=rewards_text, inline=False)
        
        embed.add_field(
            name="🎯 Performance Tips",
            value="• Only put 1 hero in your rallies so that as many people as possible can join\n• Participate actively in rally battles\n• Coordinate with alliance members\n• Use strategic timing for battles\n• Focus on high-damage output",
            inline=False
        )
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="borte_guide", description="Get tips and strategy for Borte's Scheme")
    async def borte_guide_prefix(self, ctx):
        """Traditional prefix command to show comprehensive Borte's Scheme guide and tips."""
        embed = discord.Embed(
            title="📖 Borte's Scheme Guide",
            description="The story and strategy behind Borte's Scheme",
            color=discord.Color.blue()
        )
        
        # Break the guide into multiple fields to avoid Discord's 1024 character limit
        lore_text = """**🎭 Event Lore**
Borte was once a slave girl offered as a sacrifice to Father Glowworm, but through her cunning and deceit, she rose to become the corrupt high priestess of a temple that guides fanatics. However, her thirst for Power knows no bounds. It seems she now seeks to oust Chanyu and even aims for the mocking throne. They say the enemy of your enemy is your friend. Leveraging Borte's insatiable greed might just aid in purging the corruption entrenched in this land."""
        
        participation_text = """**📋 How to Participate**
1. **Field Combat**: Defeat Shattered Skulls on the field to earn Borte's Drum and Beads
2. **Summon Allies**: Use drums and beads to summon Borte's Berserkers and Elite Berserkers
3. **Rally Battles**: Join alliance rallies to defeat Borte herself
4. **Earn Rewards**: Receive Spirit Shard: Borte based on rally performance"""
        
        tips_text = """**💡 Tips & Strategy**
• **Alliance Coordination**: Work closely with your alliance for rally battles
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **Resource Management**: Use drums and beads strategically
• **Timing**: Choose the right moments to summon berserkers
• **Performance**: Focus on high-damage output in rally battles
• **Communication**: Coordinate rally timing with alliance members"""
        
        strategy_text = """**🏆 Best Strategy**
• **Active Participation**: Join as many rally battles as possible
• **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
• **High Performance**: Maximize your damage output in battles
• **Alliance Support**: Help coordinate rally timing and strategy
• **Resource Efficiency**: Use drums and beads at optimal times"""
        
        priority_text = """**📊 Performance Priority**
1. **Rally Strategy**: Only put 1 hero in your rallies so that as many people as possible can join
2. **Rally Participation**: Join all available rally battles
3. **Damage Output**: Maximize your contribution in battles
4. **Alliance Coordination**: Work with alliance for optimal timing
5. **Resource Usage**: Use drums and beads efficiently"""
        
        embed.add_field(name="Event Lore", value=lore_text, inline=False)
        embed.add_field(name="How to Participate", value=participation_text, inline=False)
        embed.add_field(name="Tips & Strategy", value=tips_text, inline=False)
        embed.add_field(name="Best Strategy", value=strategy_text, inline=False)
        embed.add_field(name="Performance Priority", value=priority_text, inline=False)
        
        embed.add_field(
            name="📝 Information Source",
            value="Event information gathered by **Lycaris** (@lycaris_1)",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function for the cog."""
    await bot.add_cog(BorteScheme(bot)) 