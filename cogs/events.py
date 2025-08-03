"""
Events commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES

class EventDetailsView(discord.ui.View):
    """Interactive view for event details with buttons."""
    
    def __init__(self, event_data: dict, data_parser: DataParser):
        super().__init__(timeout=300)  # 5 minute timeout
        self.event_data = event_data
        self.data_parser = data_parser
    
    @discord.ui.button(label="Rewards", style=discord.ButtonStyle.primary, emoji="🏆")
    async def show_rewards(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show detailed rewards information."""
        embed = discord.Embed(
            title=f"{self.event_data['name']} - Rewards",
            description="Detailed reward information:",
            color=discord.Color.gold()
        )
        
        if 'rewards' in self.event_data and self.event_data['rewards']:
            if isinstance(self.event_data['rewards'], list) and len(self.event_data['rewards']) > 0 and isinstance(self.event_data['rewards'][0], dict):
                # New format with point tiers
                for reward_tier in self.event_data['rewards']:
                    points = reward_tier.get('points', 0)
                    rewards = reward_tier.get('rewards', [])
                    
                    tier_text = ""
                    for reward in rewards:
                        tier_text += f"🏆 {reward}\n"
                    
                    embed.add_field(
                        name=f"🎯 {points} Points",
                        value=tier_text,
                        inline=False
                    )
            else:
                # Old format (simple list)
                rewards_text = ""
                for reward in self.event_data['rewards']:
                    rewards_text += f"🏆 {reward}\n"
                embed.add_field(name="Rewards", value=rewards_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Mechanics", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def show_mechanics(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event mechanics."""
        embed = discord.Embed(
            title=f"{self.event_data['name']} - Event Mechanics",
            description="How to participate and earn points:",
            color=discord.Color.blue()
        )
        
        if 'mechanics' in self.event_data and self.event_data['mechanics']:
            mechanics_text = ""
            for mechanic in self.event_data['mechanics']:
                mechanics_text += f"⚙️ {mechanic}\n"
            embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Tips", style=discord.ButtonStyle.success, emoji="💡")
    async def show_tips(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show event tips and strategies."""
        embed = discord.Embed(
            title=f"{self.event_data['name']} - Tips & Strategy",
            description="Helpful tips to maximize your event performance:",
            color=discord.Color.green()
        )
        
        if 'tips' in self.event_data and self.event_data['tips']:
            tips_text = ""
            for tip in self.event_data['tips']:
                tips_text += f"💡 {tip}\n"
            embed.add_field(name="Tips", value=tips_text, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="⬅️")
    async def go_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to main event overview."""
        embed = discord.Embed(
            title=f"Event: {self.event_data.get('name', 'Unknown')}",
            description=self.event_data.get('description', ''),
            color=discord.Color.gold()
        )
        
        # Add basic event details
        if 'start_date' in self.event_data:
            embed.add_field(name="Start Date", value=self.event_data['start_date'], inline=True)
        
        if 'end_date' in self.event_data:
            embed.add_field(name="End Date", value=self.event_data['end_date'], inline=True)
        
        if 'type' in self.event_data:
            embed.add_field(name="Event Type", value=self.event_data['type'], inline=True)
        
        if 'difficulty' in self.event_data:
            embed.add_field(name="Difficulty", value=self.event_data['difficulty'], inline=True)
        
        if 'duration' in self.event_data:
            embed.add_field(name="Duration", value=self.event_data['duration'], inline=True)
        
        # Add requirements if available
        if 'requirements' in self.event_data and self.event_data['requirements']:
            req_text = ""
            for req in self.event_data['requirements']:
                req_text += f"📋 {req}\n"
            embed.add_field(name="Requirements", value=req_text, inline=False)
        
        # Add basic rewards info
        if 'rewards' in self.event_data and self.event_data['rewards']:
            if isinstance(self.event_data['rewards'], list) and len(self.event_data['rewards']) > 0 and isinstance(self.event_data['rewards'][0], dict):
                # New format with point tiers
                reward_tiers = len(self.event_data['rewards'])
                max_points = max(tier.get('points', 0) for tier in self.event_data['rewards'])
                embed.add_field(
                    name="Rewards",
                    value=f"🎯 {reward_tiers} reward tiers available\n🏆 Max points needed: {max_points}\n\nClick **Rewards** button for details!",
                    inline=False
                )
            else:
                # Old format (simple list)
                embed.add_field(
                    name="Rewards",
                    value=f"🏆 {len(self.event_data['rewards'])} rewards available\n\nClick **Rewards** button for details!",
                    inline=False
                )
        
        await interaction.response.edit_message(embed=embed, view=self)

class Events(commands.Cog):
    """Event-related commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @app_commands.command(name="events", description="List current and upcoming events")
    @app_commands.describe(event_type="Type of events to show (current, past, or all)")
    @app_commands.choices(event_type=[
        app_commands.Choice(name="Current Events", value="current"),
        app_commands.Choice(name="Past Events", value="past"),
        app_commands.Choice(name="All Events", value="all")
    ])
    async def list_events(self, interaction: discord.Interaction, event_type: str = "current"):
        """List current and upcoming events."""
        if event_type not in ["current", "past", "all"]:
            embed = EmbedGenerator.create_error_embed(
                "Invalid event type. Use 'current', 'past', or 'all'."
            )
            await interaction.response.send_message(embed=embed)
            return
        
        events = self.data_parser.get_events(event_type)
        
        if not events:
            embed = EmbedGenerator.create_embed(
                title="No Events Found",
                description=f"No {event_type} events found in the database.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Create events list embed
        embed = EmbedGenerator.create_embed(
            title=f"{event_type.title()} Events",
            description=f"Found {len(events)} {event_type} events:",
            color=discord.Color.green()
        )
        
        for event in events:
            name = event.get('name', 'Unknown Event')
            description = event.get('description', 'No description')
            start_date = event.get('start_date', 'Unknown')
            
            # Truncate description if too long
            if len(description) > 100:
                description = description[:97] + "..."
            
            embed.add_field(
                name=f"📅 {name}",
                value=f"**Start**: {start_date}\n{description}",
                inline=False
            )
        
        embed.add_field(
            name="Usage",
            value="Use `/event_details <name>` to get detailed information about a specific event.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="event_details", description="Get detailed information about a specific event")
    @app_commands.describe(event_name="Name of the event to get details for")
    async def event_details(self, interaction: discord.Interaction, event_name: str):
        """Get detailed information about a specific event."""
        event = self.data_parser.get_event(event_name)
        
        if not event:
            embed = EmbedGenerator.create_error_embed(
                f"Event '{event_name}' not found. Use `/events` to see available events."
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Create compact event embed
        embed = discord.Embed(
            title=f"Event: {event.get('name', 'Unknown')}",
            description=event.get('description', ''),
            color=discord.Color.gold()
        )
        
        # Add basic event details
        if 'start_date' in event:
            embed.add_field(name="Start Date", value=event['start_date'], inline=True)
        
        if 'end_date' in event:
            embed.add_field(name="End Date", value=event['end_date'], inline=True)
        
        if 'type' in event:
            embed.add_field(name="Event Type", value=event['type'], inline=True)
        
        if 'difficulty' in event:
            embed.add_field(name="Difficulty", value=event['difficulty'], inline=True)
        
        if 'duration' in event:
            embed.add_field(name="Duration", value=event['duration'], inline=True)
        
        # Add requirements if available
        if 'requirements' in event and event['requirements']:
            req_text = ""
            for req in event['requirements']:
                req_text += f"📋 {req}\n"
            embed.add_field(name="Requirements", value=req_text, inline=False)
        
        # Add basic rewards info
        if 'rewards' in event and event['rewards']:
            if isinstance(event['rewards'], list) and len(event['rewards']) > 0 and isinstance(event['rewards'][0], dict):
                # New format with point tiers
                reward_tiers = len(event['rewards'])
                max_points = max(tier.get('points', 0) for tier in event['rewards'])
                embed.add_field(
                    name="Rewards",
                    value=f"🎯 {reward_tiers} reward tiers available\n🏆 Max points needed: {max_points}\n\nClick **Rewards** button for details!",
                    inline=False
                )
            else:
                # Old format (simple list)
                embed.add_field(
                    name="Rewards",
                    value=f"🏆 {len(event['rewards'])} rewards available\n\nClick **Rewards** button for details!",
                    inline=False
                )
        
        # Create buttons for detailed information
        view = EventDetailsView(event, self.data_parser)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="upcoming", description="Show upcoming events only")
    async def upcoming_events(self, interaction: discord.Interaction):
        """Show upcoming events only."""
        events = self.data_parser.get_events("current")
        
        if not events:
            embed = EmbedGenerator.create_embed(
                title="No Upcoming Events",
                description="There are no upcoming events at this time.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Filter for upcoming events (you could add date logic here)
        upcoming_events = events  # For now, show all current events
        
        embed = EmbedGenerator.create_embed(
            title="🎯 Upcoming Events",
            description=f"Found {len(upcoming_events)} upcoming events:",
            color=discord.Color.green()
        )
        
        for event in upcoming_events:
            name = event.get('name', 'Unknown Event')
            start_date = event.get('start_date', 'Unknown')
            end_date = event.get('end_date', 'Unknown')
            
            embed.add_field(
                name=f"📅 {name}",
                value=f"**Start**: {start_date}\n**End**: {end_date}",
                inline=False
            )
        
        embed.add_field(
            name="More Information",
            value="Use `/event_details <name>` to get detailed information about a specific event.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="event_search", description="Search for events by name or description")
    @app_commands.describe(search_term="Search term to find events")
    async def search_events(self, interaction: discord.Interaction, search_term: str):
        """Search for events by name or description."""
        if len(search_term) < 2:
            embed = EmbedGenerator.create_error_embed("Search term must be at least 2 characters long.")
            await interaction.response.send_message(embed=embed)
            return
        
        events = self.data_parser.get_events("all")
        search_term = search_term.lower()
        matches = []
        
        for event in events:
            name = event.get('name', '').lower()
            description = event.get('description', '').lower()
            
            if search_term in name or search_term in description:
                matches.append(event)
        
        if not matches:
            embed = EmbedGenerator.create_error_embed(
                f"No events found matching '{search_term}'."
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Create search results embed
        embed = EmbedGenerator.create_embed(
            title=f"Search Results for '{search_term}'",
            description=f"Found {len(matches)} matching events:",
            color=discord.Color.green()
        )
        
        for event in matches:
            name = event.get('name', 'Unknown')
            description = event.get('description', 'No description')
            start_date = event.get('start_date', 'Unknown')
            
            # Truncate description if too long
            if len(description) > 100:
                description = description[:97] + "..."
            
            embed.add_field(
                name=f"📅 {name}",
                value=f"**Start**: {start_date}\n{description}",
                inline=False
            )
        
        embed.add_field(
            name="Usage",
            value="Use `/event_details <name>` to get detailed information about an event.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="event_rewards", description="Show rewards for a specific event")
    @app_commands.describe(event_name="Name of the event to show rewards for")
    async def event_rewards(self, interaction: discord.Interaction, event_name: str):
        """Show rewards for a specific event."""
        event = self.data_parser.get_event(event_name)
        
        if not event:
            embed = EmbedGenerator.create_error_embed(
                f"Event '{event_name}' not found."
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if 'rewards' not in event or not event['rewards']:
            embed = EmbedGenerator.create_error_embed(
                f"No rewards information available for event '{event_name}'."
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Create rewards embed
        embed = EmbedGenerator.create_embed(
            title=f"{event['name']} - Rewards",
            description="Rewards available for this event:",
            color=discord.Color.gold()
        )
        
        # Handle new rewards structure with point tiers
        if isinstance(event['rewards'], list) and len(event['rewards']) > 0 and isinstance(event['rewards'][0], dict):
            # New format with point tiers
            for reward_tier in event['rewards']:
                points = reward_tier.get('points', 0)
                rewards = reward_tier.get('rewards', [])
                
                tier_text = f"**{points} Points Required:**\n"
                for reward in rewards:
                    tier_text += f"🏆 {reward}\n"
                
                embed.add_field(
                    name=f"🎯 {points} Points",
                    value=tier_text,
                    inline=False
                )
        else:
            # Old format (simple list)
            rewards_text = ""
            for reward in event['rewards']:
                rewards_text += f"🏆 {reward}\n"
            embed.add_field(name="Rewards", value=rewards_text, inline=False)
        
        # Add requirements if available
        if 'requirements' in event and event['requirements']:
            req_text = ""
            for req in event['requirements']:
                req_text += f"📋 {req}\n"
            embed.add_field(name="Requirements", value=req_text, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Events(bot)) 