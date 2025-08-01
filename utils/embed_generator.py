"""
Embed generator utility for creating consistent Discord embeds.
"""

import discord
from typing import Optional, List, Dict, Any
from config.settings import EMBED_COLORS
from pathlib import Path

class EmbedGenerator:
    """Utility class for generating consistent Discord embeds."""
    
    @staticmethod
    def create_embed(
        title: str,
        description: str = "",
        color: Optional[discord.Color] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer: Optional[str] = None,
        timestamp: Optional[bool] = True
    ) -> discord.Embed:
        """
        Create a standardized embed with consistent styling.
        
        Args:
            title: The embed title
            description: The embed description
            color: The embed color (defaults to primary color)
            fields: List of field dictionaries with 'name', 'value', 'inline' keys
            thumbnail: URL for thumbnail image
            image: URL for main image
            footer: Footer text
            timestamp: Whether to add current timestamp
            
        Returns:
            discord.Embed: The created embed
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color or EMBED_COLORS["primary"]
        )
        
        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get("name", ""),
                    value=field.get("value", ""),
                    inline=field.get("inline", True)
                )
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
            
        if image:
            embed.set_image(url=image)
            
        if footer:
            embed.set_footer(text=footer)
            
        if timestamp:
            embed.timestamp = discord.utils.utcnow()
            
        return embed
    
    @staticmethod
    def create_character_embed(character_data: Dict[str, Any]) -> discord.Embed:
        """
        Create an embed for character information.
        
        Args:
            character_data: Dictionary containing character information
            
        Returns:
            discord.Embed: Character information embed
        """
        embed = discord.Embed(
            title=f"Character: {character_data.get('name', 'Unknown')}",
            description=character_data.get('description', ''),
            color=EMBED_COLORS["info"]
        )
        
        # Add character stats
        if 'stats' in character_data:
            stats_text = ""
            for stat, value in character_data['stats'].items():
                stats_text += f"**{stat.title()}**: {value}\n"
            embed.add_field(name="Stats", value=stats_text, inline=False)
        
        # Add character abilities
        if 'abilities' in character_data:
            abilities_text = ""
            for ability in character_data['abilities']:
                abilities_text += f"• {ability}\n"
            embed.add_field(name="Abilities", value=abilities_text, inline=False)
        
        # Add character image if available
        if 'image_url' in character_data:
            embed.set_thumbnail(url=character_data['image_url'])
        
        return embed
    
    @staticmethod
    def create_skills_embed(character_name: str, skills_data: List[Dict[str, Any]]) -> discord.Embed:
        """
        Create an embed for character skills.
        
        Args:
            character_name: Name of the character
            skills_data: List of skill dictionaries
            
        Returns:
            discord.Embed: Skills information embed
        """
        embed = discord.Embed(
            title=f"{character_name} - Skills",
            description=f"All skills for {character_name}",
            color=EMBED_COLORS["secondary"]
        )
        
        for skill in skills_data:
            skill_text = f"**Description**: {skill.get('description', 'No description')}\n"
            skill_text += f"**Cooldown**: {skill.get('cooldown', 'N/A')}\n"
            
            # Add skill levels
            if 'levels' in skill:
                levels_text = ""
                for level, details in skill['levels'].items():
                    levels_text += f"**Level {level}**: {details}\n"
                skill_text += f"\n**Levels**:\n{levels_text}"
            
            embed.add_field(
                name=f"Skill: {skill.get('name', 'Unknown')}",
                value=skill_text,
                inline=False
            )
        
        return embed
    
    @staticmethod
    def create_talent_embed(character_name: str, talent_data: Dict[str, Any], talent_type_info: Optional[Dict[str, Any]] = None, talent_images: Optional[Dict[str, str]] = None) -> discord.Embed:
        """
        Create an embed for character talent tree.
        
        Args:
            character_name: Name of the character
            talent_data: Talent tree data
            talent_type_info: Talent type information
            talent_images: Dictionary with talent tree image paths
            
        Returns:
            discord.Embed: Talent tree embed
        """
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
        
        # Add talent tree structure if available
        if 'talents' in talent_data:
            for tier, talents in talent_data['talents'].items():
                tier_text = ""
                for talent in talents:
                    tier_text += f"• **{talent['name']}**: {talent.get('description', '')}\n"
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
        
        return embed
    
    @staticmethod
    def create_event_embed(event_data: Dict[str, Any]) -> discord.Embed:
        """
        Create an embed for event information.
        
        Args:
            event_data: Dictionary containing event information
            
        Returns:
            discord.Embed: Event information embed
        """
        embed = discord.Embed(
            title=f"Event: {event_data.get('name', 'Unknown')}",
            description=event_data.get('description', ''),
            color=EMBED_COLORS["warning"]
        )
        
        # Add event details
        if 'start_date' in event_data:
            embed.add_field(name="Start Date", value=event_data['start_date'], inline=True)
        
        if 'end_date' in event_data:
            embed.add_field(name="End Date", value=event_data['end_date'], inline=True)
        
        if 'type' in event_data:
            embed.add_field(name="Event Type", value=event_data['type'], inline=True)
        
        if 'difficulty' in event_data:
            embed.add_field(name="Difficulty", value=event_data['difficulty'], inline=True)
        
        if 'duration' in event_data:
            embed.add_field(name="Duration", value=event_data['duration'], inline=True)
        
        # Add requirements if available
        if 'requirements' in event_data and event_data['requirements']:
            req_text = ""
            for req in event_data['requirements']:
                req_text += f"📋 {req}\n"
            embed.add_field(name="Requirements", value=req_text, inline=False)
        
        # Handle rewards with new point-based structure
        if 'rewards' in event_data and event_data['rewards']:
            if isinstance(event_data['rewards'], list) and len(event_data['rewards']) > 0 and isinstance(event_data['rewards'][0], dict):
                # New format with point tiers
                for reward_tier in event_data['rewards']:
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
                reward_text = ""
                for reward in event_data['rewards']:
                    reward_text += f"🏆 {reward}\n"
                embed.add_field(name="Rewards", value=reward_text, inline=False)
        
        # Add mechanics if available
        if 'mechanics' in event_data and event_data['mechanics']:
            mechanics_text = ""
            for mechanic in event_data['mechanics']:
                mechanics_text += f"⚙️ {mechanic}\n"
            embed.add_field(name="Event Mechanics", value=mechanics_text, inline=False)
        
        # Add tips if available
        if 'tips' in event_data and event_data['tips']:
            tips_text = ""
            for tip in event_data['tips']:
                tips_text += f"💡 {tip}\n"
            embed.add_field(name="Tips", value=tips_text, inline=False)
        
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
            title="❌ Error",
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
            title="✅ Success",
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
            title="🤖 Bot Commands",
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