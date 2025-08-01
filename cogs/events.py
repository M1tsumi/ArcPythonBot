"""
Events commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES

class Events(commands.Cog):
    """Event-related commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @commands.command(name="events")
    async def list_events(self, ctx, event_type: Optional[str] = "current"):
        """List current and upcoming events."""
        if event_type not in ["current", "past", "all"]:
            embed = EmbedGenerator.create_error_embed(
                "Invalid event type. Use 'current', 'past', or 'all'."
            )
            await ctx.send(embed=embed)
            return
        
        events = self.data_parser.get_events(event_type)
        
        if not events:
            embed = EmbedGenerator.create_embed(
                title="No Events Found",
                description=f"No {event_type} events found in the database.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
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
            value="Use `!event_details <name>` to get detailed information about a specific event.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="event_details")
    async def event_details(self, ctx, *, event_name: str):
        """Get detailed information about a specific event."""
        event = self.data_parser.get_event(event_name)
        
        if not event:
            embed = EmbedGenerator.create_error_embed(
                f"Event '{event_name}' not found. Use `!events` to see available events."
            )
            await ctx.send(embed=embed)
            return
        
        # Create detailed event embed
        embed = EmbedGenerator.create_event_embed(event)
        
        # Add additional information
        if 'type' in event:
            embed.add_field(name="Event Type", value=event['type'], inline=True)
        
        if 'difficulty' in event:
            embed.add_field(name="Difficulty", value=event['difficulty'], inline=True)
        
        if 'duration' in event:
            embed.add_field(name="Duration", value=event['duration'], inline=True)
        
        # Add special mechanics
        if 'mechanics' in event:
            mechanics_text = ""
            for mechanic in event['mechanics']:
                mechanics_text += f"• {mechanic}\n"
            embed.add_field(name="Special Mechanics", value=mechanics_text, inline=False)
        
        # Add tips
        if 'tips' in event:
            tips_text = ""
            for tip in event['tips']:
                tips_text += f"💡 {tip}\n"
            embed.add_field(name="Tips", value=tips_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="upcoming")
    async def upcoming_events(self, ctx):
        """Show upcoming events only."""
        events = self.data_parser.get_events("current")
        
        if not events:
            embed = EmbedGenerator.create_embed(
                title="No Upcoming Events",
                description="There are no upcoming events at this time.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
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
            value="Use `!event_details <name>` to get detailed information about a specific event.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="event_search")
    async def search_events(self, ctx, *, search_term: str):
        """Search for events by name or description."""
        if len(search_term) < 2:
            embed = EmbedGenerator.create_error_embed("Search term must be at least 2 characters long.")
            await ctx.send(embed=embed)
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
            await ctx.send(embed=embed)
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
            value="Use `!event_details <name>` to get detailed information about an event.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="event_rewards")
    async def event_rewards(self, ctx, *, event_name: str):
        """Show rewards for a specific event."""
        event = self.data_parser.get_event(event_name)
        
        if not event:
            embed = EmbedGenerator.create_error_embed(
                f"Event '{event_name}' not found."
            )
            await ctx.send(embed=embed)
            return
        
        if 'rewards' not in event or not event['rewards']:
            embed = EmbedGenerator.create_error_embed(
                f"No rewards information available for event '{event_name}'."
            )
            await ctx.send(embed=embed)
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
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Events(bot)) 