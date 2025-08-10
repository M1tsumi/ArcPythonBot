"""
Optimized embed generator utility for creating consistent Discord embeds.
"""

import discord
from typing import Optional, List, Dict, Any
from config.settings import EMBED_COLORS, BOT_NAME
from pathlib import Path
import time

class EmbedGenerator:
    """Optimized utility class for generating consistent Discord embeds."""
    
    # Cache for frequently used embeds
    _embed_cache = {}
    _cache_timeout = 300  # 5 minutes
    
    @staticmethod
    def _get_cache_key(*args, **kwargs) -> str:
        """Generate a cache key for embed parameters."""
        return f"{hash(str(args) + str(sorted(kwargs.items())))}"
    
    @staticmethod
    def _is_cache_valid(timestamp: float) -> bool:
        """Check if cached embed is still valid."""
        return time.time() - timestamp < EmbedGenerator._cache_timeout
    
    @staticmethod
    def add_safe_field(embed: discord.Embed, name: str, value: str, inline: bool = False, max_length: int = 1024):
        """
        Safely add a field to an embed, splitting long values into multiple fields.
        
        Args:
            embed: The discord embed to add fields to
            name: The field name
            value: The field value
            inline: Whether the field should be inline
            max_length: Maximum length for each field value (Discord limit is 1024)
        """
        if len(value) <= max_length:
            embed.add_field(name=name, value=value, inline=inline)
        else:
            # Split the value into chunks
            chunks = []
            current_chunk = ""
            
            for line in value.split('\n'):
                if len(current_chunk) + len(line) + 1 <= max_length:
                    current_chunk += line + '\n'
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = line + '\n'
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Add the first chunk with the original name
            if chunks:
                embed.add_field(name=name, value=chunks[0], inline=inline)
                
                # Add remaining chunks with continuation names
                for i, chunk in enumerate(chunks[1:], 1):
                    embed.add_field(name=f"{name} (continued)", value=chunk, inline=inline)
    
    @staticmethod
    def create_embed(
        title: str,
        description: str = "",
        color: Optional[discord.Color] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer: Optional[str] = None,
        timestamp: Optional[bool] = True,
        use_cache: bool = True
    ) -> discord.Embed:
        """
        Create a standardized embed with consistent styling and optional caching.
        
        Args:
            title: The embed title
            description: The embed description
            color: The embed color (defaults to primary color)
            fields: List of field dictionaries with 'name', 'value', 'inline' keys
            thumbnail: URL for thumbnail image
            image: URL for main image
            footer: Footer text
            timestamp: Whether to add current timestamp
            use_cache: Whether to use caching for this embed
            
        Returns:
            discord.Embed: The created embed
        """
        # Check cache if enabled
        if use_cache:
            cache_key = EmbedGenerator._get_cache_key(title, description, color, fields, thumbnail, image, footer, timestamp)
            if cache_key in EmbedGenerator._embed_cache:
                cached_data = EmbedGenerator._embed_cache[cache_key]
                if EmbedGenerator._is_cache_valid(cached_data['timestamp']):
                    # Return a copy of the cached embed to prevent field duplication
                    cached_embed = cached_data['embed']
                    embed_copy = discord.Embed(
                        title=cached_embed.title,
                        description=cached_embed.description,
                        color=cached_embed.color,
                        timestamp=cached_embed.timestamp
                    )
                    
                    # Copy fields
                    for field in cached_embed.fields:
                        embed_copy.add_field(name=field.name, value=field.value, inline=field.inline)
                    
                    # Copy footer
                    if cached_embed.footer:
                        embed_copy.set_footer(text=cached_embed.footer.text, icon_url=cached_embed.footer.icon_url)
                    
                    # Copy thumbnail and image
                    if cached_embed.thumbnail:
                        embed_copy.set_thumbnail(url=cached_embed.thumbnail.url)
                    if cached_embed.image:
                        embed_copy.set_image(url=cached_embed.image.url)
                    
                    return embed_copy
        
        # Create new embed
        embed = discord.Embed(
            title=title,
            description=description,
            color=color or EMBED_COLORS["primary"]
        )
        
        if fields:
            for field in fields:
                EmbedGenerator.add_safe_field(
                    embed,
                    field.get("name", ""),
                    field.get("value", ""),
                    field.get("inline", True)
                )
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
            
        if image:
            embed.set_image(url=image)
            
        if footer:
            embed.set_footer(text=footer)
            
        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        # Apply standardized footer if none provided
        if not embed.footer or not embed.footer.text:
            embed.set_footer(text=f"{BOT_NAME}")
        
        # Cache the embed if enabled
        if use_cache:
            EmbedGenerator._embed_cache[cache_key] = {
                'embed': embed,
                'timestamp': time.time()
            }
            
        return embed

    @staticmethod
    def finalize_embed(embed: discord.Embed, *, default_footer: Optional[str] = None, ensure_timestamp: bool = True) -> discord.Embed:
        """Apply consistent professional styling to an existing embed.

        - Ensures a footer is set (uses BOT_NAME or provided default_footer)
        - Ensures a timestamp is present if ensure_timestamp is True
        """
        if ensure_timestamp and not embed.timestamp:
            embed.timestamp = discord.utils.utcnow()

        footer_text = (embed.footer.text if embed.footer else None)
        if not footer_text:
            embed.set_footer(text=default_footer or BOT_NAME)

        return embed
    
    @staticmethod
    def create_ping_embed(latency: float, api_latency: float, guild_count: int, user_count: int, command_count: int) -> discord.Embed:
        """
        Create a clean ping embed with minimal emoji usage.
        
        Args:
            latency: Response time in milliseconds
            api_latency: Discord API latency in milliseconds
            guild_count: Number of servers
            user_count: Number of users
            command_count: Number of commands
            
        Returns:
            discord.Embed: Ping status embed
        """
        embed = discord.Embed(
            title="Bot Status",
            description="Bot is online and responding",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Response Time",
            value=f"{latency:.1f}ms",
            inline=True
        )
        
        embed.add_field(
            name="API Latency",
            value=f"{api_latency}ms",
            inline=True
        )
        
        embed.add_field(
            name="Status",
            value="Online",
            inline=True
        )
        
        embed.add_field(
            name="Servers",
            value=f"{guild_count}",
            inline=True
        )
        
        embed.add_field(
            name="Users",
            value=f"{user_count}",
            inline=True
        )
        
        embed.add_field(
            name="Commands",
            value=f"{command_count}",
            inline=True
        )
        
        embed.set_footer(text="Avatar Realms Collide Bot • Developed by Quefep")
        
        return embed
    
    @staticmethod
    def create_troop_calculator_embed(troop_data: Dict[str, Any], quantity: int, total_costs: Dict[str, int], total_time: str) -> discord.Embed:
        """
        Create a clean troop calculator embed with organized information.
        
        Args:
            troop_data: Troop information dictionary
            quantity: Number of troops
            total_costs: Dictionary of total costs
            total_time: Formatted total time string
            
        Returns:
            discord.Embed: Troop calculator embed
        """
        embed = discord.Embed(
            title=f"{troop_data['tier']} {troop_data['unit_name']} ({troop_data['element']})",
            description=f"Quantity: {quantity:,}",
            color=discord.Color.blue()
        )
        
        # Troop stats
        stats_text = f"Power: {troop_data['power']}\n"
        stats_text += f"ATK: {troop_data['atk']}\n"
        stats_text += f"DEF: {troop_data['def']}\n"
        stats_text += f"Health: {troop_data['health']}\n"
        stats_text += f"Speed: {troop_data['speed']}\n"
        stats_text += f"Load: {troop_data['load']}"
        
        embed.add_field(
            name="Troop Stats",
            value=stats_text,
            inline=True
        )
        
        # Total costs
        cost_text = f"Food: {total_costs['food']:,}\n"
        cost_text += f"Wood: {total_costs['wood']:,}\n"
        if total_costs.get('stone', 0) > 0:
            cost_text += f"Stone: {total_costs['stone']:,}\n"
        if total_costs.get('gold', 0) > 0:
            cost_text += f"Gold: {total_costs['gold']:,}\n"
        cost_text += f"Time: {total_time}"
        
        embed.add_field(
            name="Total Costs",
            value=cost_text,
            inline=True
        )
        
        return embed
    
    @staticmethod
    def create_character_embed(character_data: Dict[str, Any], use_cache: bool = True) -> discord.Embed:
        """
        Create an optimized embed for character information.
        
        Args:
            character_data: Dictionary containing character information
            use_cache: Whether to use caching for this embed
            
        Returns:
            discord.Embed: Character information embed
        """
        character_name = character_data.get('name', 'Unknown')
        
        # Check cache first
        if use_cache:
            cache_key = f"character_{character_name}"
            if cache_key in EmbedGenerator._embed_cache:
                cached_data = EmbedGenerator._embed_cache[cache_key]
                if EmbedGenerator._is_cache_valid(cached_data['timestamp']):
                    return cached_data['embed']
        
        embed = discord.Embed(
            title=f"Character: {character_name}",
            description=character_data.get('description', ''),
            color=EMBED_COLORS["info"]
        )
        
        # Add character stats efficiently
        if 'stats' in character_data:
            stats_text = "\n".join([f"**{stat.title()}**: {value}" for stat, value in character_data['stats'].items()])
            embed.add_field(name="Stats", value=stats_text, inline=False)
        
        # Add character abilities efficiently
        if 'abilities' in character_data:
            abilities_text = "\n".join([f"• {ability}" for ability in character_data['abilities']])
            embed.add_field(name="Abilities", value=abilities_text, inline=False)
        
        # Add character image if available
        if 'image_url' in character_data:
            embed.set_thumbnail(url=character_data['image_url'])
        
        # Cache the embed
        if use_cache:
            EmbedGenerator._embed_cache[cache_key] = {
                'embed': embed,
                'timestamp': time.time()
            }
        
        return embed
    
    @staticmethod
    def create_skills_embed(character_name: str, skills_data: List[Dict[str, Any]], use_cache: bool = True) -> discord.Embed:
        """
        Create an optimized embed for character skills.
        
        Args:
            character_name: Name of the character
            skills_data: List of skill dictionaries
            use_cache: Whether to use caching for this embed
            
        Returns:
            discord.Embed: Skills information embed
        """
        # Check cache first
        if use_cache:
            cache_key = f"skills_{character_name}"
            if cache_key in EmbedGenerator._embed_cache:
                cached_data = EmbedGenerator._embed_cache[cache_key]
                if EmbedGenerator._is_cache_valid(cached_data['timestamp']):
                    return cached_data['embed']
        
        embed = discord.Embed(
            title=f"{character_name} - Skills",
            description=f"All skills for {character_name}",
            color=EMBED_COLORS["secondary"]
        )
        
        for skill in skills_data:
            skill_text = f"**Description**: {skill.get('description', 'No description')}\n"
            skill_text += f"**Cooldown**: {skill.get('cooldown', 'N/A')}\n"
            
            # Add skill levels efficiently
            if 'levels' in skill:
                levels_text = "\n".join([f"**Level {level}**: {details}" for level, details in skill['levels'].items()])
                skill_text += f"\n**Levels**:\n{levels_text}"
            
            embed.add_field(
                name=f"Skill: {skill.get('name', 'Unknown')}",
                value=skill_text,
                inline=False
            )
        
        # Cache the embed
        if use_cache:
            EmbedGenerator._embed_cache[cache_key] = {
                'embed': embed,
                'timestamp': time.time()
            }
        
        return embed
    
    @staticmethod
    def create_talent_embed(character_name: str, talent_data: Dict[str, Any], talent_type_info: Optional[Dict[str, Any]] = None, talent_images: Optional[Dict[str, str]] = None, use_cache: bool = True) -> discord.Embed:
        """
        Create an optimized embed for character talent tree.
        
        Args:
            character_name: Name of the character
            talent_data: Talent tree data
            talent_type_info: Talent type information
            talent_images: Dictionary with talent tree image paths
            use_cache: Whether to use caching for this embed
            
        Returns:
            discord.Embed: Talent tree embed
        """
        # Check cache first
        if use_cache:
            cache_key = f"talent_{character_name}"
            if cache_key in EmbedGenerator._embed_cache:
                cached_data = EmbedGenerator._embed_cache[cache_key]
                if EmbedGenerator._is_cache_valid(cached_data['timestamp']):
                    return cached_data['embed']
        
        embed = discord.Embed(
            title=f"{character_name} - Talent Tree",
            description=talent_data.get('description', ''),
            color=EMBED_COLORS["primary"]
        )
        
        # Add talent type information if available
        if talent_type_info and talent_type_info.get('talent_type'):
            embed.add_field(
                name="Talent Type",
                value=talent_type_info['talent_type'],
                inline=True
            )
        
        # Add general talent tree information
        embed.add_field(
            name="Talent Tree Info",
            value="• **Total Points**: 89 points for maxed hero\n"
                  "• **Dual Purpose**: Trees may have multiple focuses\n"
                  "• **Gold/Blue**: Activated talents\n"
                  "• **Red X**: Ignore crossed-out talents",
            inline=False
        )
        
        # Add talent tree structure efficiently
        if 'talents' in talent_data:
            for tier, talents in talent_data['talents'].items():
                tier_text = "\n".join([f"• **{talent['name']}**: {talent.get('description', '')}" for talent in talents])
                embed.add_field(
                    name=f"Tier {tier}",
                    value=tier_text,
                    inline=False
                )
        
        # Add talent tree images if available
        if talent_images:
            if talent_images.get('talent_tree_1'):
                embed.set_image(url=f"attachment://{Path(talent_images['talent_tree_1']).name}")
            elif talent_images.get('talent_tree_2'):
                embed.set_image(url=f"attachment://{Path(talent_images['talent_tree_2']).name}")
        
        embed.set_footer(text="Use !talent <character> <talent_name> for detailed talent information")
        
        # Cache the embed
        if use_cache:
            EmbedGenerator._embed_cache[cache_key] = {
                'embed': embed,
                'timestamp': time.time()
            }
        
        return embed
    
    @staticmethod
    def create_event_embed(event_data: Dict[str, Any], use_cache: bool = True) -> discord.Embed:
        """
        Create an optimized embed for event information.
        
        Args:
            event_data: Dictionary containing event information
            use_cache: Whether to use caching for this embed
            
        Returns:
            discord.Embed: Event information embed
        """
        event_name = event_data.get('name', 'Unknown')
        
        # Check cache first
        if use_cache:
            cache_key = f"event_{event_name}"
            if cache_key in EmbedGenerator._embed_cache:
                cached_data = EmbedGenerator._embed_cache[cache_key]
                if EmbedGenerator._is_cache_valid(cached_data['timestamp']):
                    return cached_data['embed']
        
        embed = discord.Embed(
            title=f"Event: {event_name}",
            description=event_data.get('description', ''),
            color=EMBED_COLORS["warning"]
        )
        
        # Add event details efficiently
        event_fields = [
            ('start_date', 'Start Date'),
            ('end_date', 'End Date'),
            ('type', 'Event Type'),
            ('difficulty', 'Difficulty'),
            ('duration', 'Duration')
        ]
        
        for field_key, field_name in event_fields:
            if field_key in event_data:
                embed.add_field(name=field_name, value=event_data[field_key], inline=True)
        
        # Add requirements if available
        if 'requirements' in event_data and event_data['requirements']:
            req_text = "\n".join([f"• {req}" for req in event_data['requirements']])
            embed.add_field(name="Requirements", value=req_text, inline=False)
        
        # Handle rewards with new point-based structure efficiently
        if 'rewards' in event_data and event_data['rewards']:
            if isinstance(event_data['rewards'], list) and len(event_data['rewards']) > 0 and isinstance(event_data['rewards'][0], dict):
                # New format with point tiers
                for reward_tier in event_data['rewards']:
                    points = reward_tier.get('points', 0)
                    rewards = reward_tier.get('rewards', [])
                    
                    tier_text = "\n".join([f"• {reward}" for reward in rewards])
                    
                    embed.add_field(
                        name=f"{points} Points",
                        value=tier_text,
                        inline=False
                    )
            else:
                # Old format (simple list)
                reward_text = "\n".join([f"• {reward}" for reward in event_data['rewards']])
                embed.add_field(name="Rewards", value=reward_text, inline=False)
        
        # Add mechanics if available
        if 'mechanics' in event_data and event_data['mechanics']:
            mechanics_text = "\n".join([f"• {mechanic}" for mechanic in event_data['mechanics']])
            embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        # Add tips if available
        if 'tips' in event_data and event_data['tips']:
            tips_text = "\n".join([f"• {tip}" for tip in event_data['tips']])
            embed.add_field(name="Tips", value=tips_text, inline=False)
        
        # Cache the embed
        if use_cache:
            EmbedGenerator._embed_cache[cache_key] = {
                'embed': embed,
                'timestamp': time.time()
            }
        
        return embed
    
    @staticmethod
    def create_error_embed(message: str) -> discord.Embed:
        """
        Create an error embed.
        
        Args:
            message: Error message
            
        Returns:
            discord.Embed: Error embed
        """
        return discord.Embed(
            title="Error",
            description=message,
            color=EMBED_COLORS["error"]
        )
    
    @staticmethod
    def create_success_embed(message: str) -> discord.Embed:
        """
        Create a success embed.
        
        Args:
            message: Success message
            
        Returns:
            discord.Embed: Success embed
        """
        return discord.Embed(
            title="Success",
            description=message,
            color=EMBED_COLORS["success"]
        )
    
    @staticmethod
    def create_help_embed(commands_data: List[Dict[str, Any]]) -> discord.Embed:
        """
        Create a help embed with command information.
        
        Args:
            commands_data: List of command dictionaries
            
        Returns:
            discord.Embed: Help embed
        """
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are all available commands:",
            color=EMBED_COLORS["info"]
        )
        
        for cmd in commands_data:
            embed.add_field(
                name=f"!{cmd['name']}",
                value=f"{cmd['description']}\nUsage: `{cmd['usage']}`",
                inline=False
            )
        
        embed.set_footer(text="Use !help <command> for detailed information about a specific command.")
        
        return embed
    
    @staticmethod
    def clear_cache():
        """Clear the embed cache."""
        EmbedGenerator._embed_cache.clear()
    
    @staticmethod
    def get_cache_stats() -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'cache_size': len(EmbedGenerator._embed_cache),
            'cache_timeout': EmbedGenerator._cache_timeout,
            'cached_embeds': list(EmbedGenerator._embed_cache.keys())
        } 