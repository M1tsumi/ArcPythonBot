"""
Game information commands cog for the Avatar Realms Collide Discord Bot.
"""

import discord
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES
from pathlib import Path

class GameInfo(commands.Cog):
    """Game information commands for characters, skills, and talents."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @commands.command(name="characters")
    async def list_characters(self, ctx):
        """List all available characters."""
        characters = self.data_parser.get_character_list()
        
        if not characters:
            embed = EmbedGenerator.create_error_embed("No characters found in the database.")
            await ctx.send(embed=embed)
            return
        
        # Create embed with character list
        embed = EmbedGenerator.create_embed(
            title="Available Characters",
            description=f"Found {len(characters)} characters in the database.",
            color=discord.Color.blue()
        )
        
        # Group characters by category if available
        character_text = ""
        for i, char in enumerate(characters, 1):
            name = char.get('name', 'Unknown')
            category = char.get('category', 'General')
            character_text += f"**{i}.** {name} ({category})\n"
        
        # Split into multiple embeds if too long
        if len(character_text) > 1024:
            # Split into chunks
            chunks = [character_text[i:i+1024] for i in range(0, len(character_text), 1024)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    embed.description = f"Found {len(characters)} characters in the database."
                    embed.add_field(name="Characters", value=chunk, inline=False)
                else:
                    embed.add_field(name=f"Characters (continued)", value=chunk, inline=False)
        else:
            embed.add_field(name="Characters", value=character_text, inline=False)
        
        embed.add_field(
            name="Usage",
            value="Use `!character <name>` to get detailed information about a specific character.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="character")
    async def character_info(self, ctx, *, character_name: str):
        """Get detailed information about a specific character."""
        character = self.data_parser.get_character(character_name)
        
        if not character:
            embed = EmbedGenerator.create_error_embed(
                f"Character '{character_name}' not found. Use `!characters` to see available characters."
            )
            await ctx.send(embed=embed)
            return
        
        # Create character embed
        embed = EmbedGenerator.create_character_embed(character)
        
        # Add additional information
        if 'rarity' in character:
            embed.add_field(name="Rarity", value=character['rarity'], inline=True)
        
        if 'element' in character:
            embed.add_field(name="Element", value=character['element'], inline=True)
        
        if 'weapon_type' in character:
            embed.add_field(name="Weapon Type", value=character['weapon_type'], inline=True)
        
        # Add usage information
        embed.add_field(
            name="More Information",
            value=f"Use `!character_skills {character['name']}` to see skills\n"
                  f"Use `!character_talent {character['name']}` to see talent tree",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="character_skills")
    async def character_skills(self, ctx, *, character_name: str):
        """Show skills for a specific character."""
        skills = self.data_parser.get_character_skills(character_name)
        
        if not skills:
            embed = EmbedGenerator.create_error_embed(
                f"No skills found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Create skills embed
        embed = EmbedGenerator.create_skills_embed(character_name, skills)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="character_talent")
    async def character_talent(self, ctx, *, character_name: str):
        """Show talent tree for a specific character."""
        # Get character information
        character = self.data_parser.get_character(character_name)
        
        # Get talent type information
        talent_type_info = self.data_parser.get_talent_type_info(character_name)
        
        # Get talent tree images
        talent_images = self.data_parser.get_talent_tree_images(character_name)
        
        if not talent_images:
            embed = EmbedGenerator.create_error_embed(
                f"No talent tree images found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Create comprehensive embed with character information
        embed = discord.Embed(
            title=f"{character_name} - Talent Trees",
            description=f"Complete talent tree information for {character_name}",
            color=discord.Color.purple()
        )
        
        # Add character information if available
        if character:
            if 'description' in character:
                embed.add_field(name="Character Description", value=character['description'], inline=False)
            
            if 'rarity' in character:
                embed.add_field(name="Rarity", value=character['rarity'], inline=True)
            
            if 'element' in character:
                embed.add_field(name="Element", value=character['element'], inline=True)
            
            if 'weapon_type' in character:
                embed.add_field(name="Weapon Type", value=character['weapon_type'], inline=True)
        
        # Add talent type information
        if talent_type_info and talent_type_info.get('talent_type'):
            embed.add_field(
                name="Talent Tree Type",
                value=talent_type_info['talent_type'],
                inline=True
            )
        
        # Add talent tree information
        embed.add_field(
            name="Talent Tree Info",
            value="• **Total Points**: 89 points for maxed hero\n"
                  "• **Dual Purpose**: Trees may have multiple focuses\n"
                  "• **Gold/Blue**: Activated talents\n"
                  "• **Red X**: Ignore crossed-out talents",
            inline=False
        )
        
        # Add image information
        image_info = ""
        if talent_images.get('talent_tree_1'):
            image_info += f"• **Talent Tree 1**: {Path(talent_images['talent_tree_1']).name}\n"
        if talent_images.get('talent_tree_2'):
            image_info += f"• **Talent Tree 2**: {Path(talent_images['talent_tree_2']).name}\n"
        
        if image_info:
            embed.add_field(name="Available Talent Trees", value=image_info, inline=False)
        
        embed.set_footer(text="Use !character <name> for more character information")
        
        # Send embed with both images if available
        files = []
        if talent_images.get('talent_tree_1'):
            files.append(discord.File(talent_images['talent_tree_1'], filename=Path(talent_images['talent_tree_1']).name))
        if talent_images.get('talent_tree_2'):
            files.append(discord.File(talent_images['talent_tree_2'], filename=Path(talent_images['talent_tree_2']).name))
        
        if files:
            await ctx.send(embed=embed, files=files)
        else:
            await ctx.send(embed=embed)
    
    @commands.command(name="search")
    async def search_characters(self, ctx, *, search_term: str):
        """Search for characters by name or description."""
        if len(search_term) < 2:
            embed = EmbedGenerator.create_error_embed("Search term must be at least 2 characters long.")
            await ctx.send(embed=embed)
            return
        
        matches = self.data_parser.search_characters(search_term)
        
        if not matches:
            embed = EmbedGenerator.create_error_embed(
                f"No characters found matching '{search_term}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Create search results embed
        embed = EmbedGenerator.create_embed(
            title=f"Search Results for '{search_term}'",
            description=f"Found {len(matches)} matching characters:",
            color=discord.Color.green()
        )
        
        for char in matches:
            name = char.get('name', 'Unknown')
            description = char.get('description', 'No description')
            # Truncate description if too long
            if len(description) > 100:
                description = description[:97] + "..."
            
            embed.add_field(
                name=name,
                value=description,
                inline=False
            )
        
        embed.add_field(
            name="Usage",
            value="Use `!character <name>` to get detailed information about a character.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="skill")
    async def skill_info(self, ctx, character_name: str, *, skill_name: str):
        """Get detailed information about a specific skill."""
        skills = self.data_parser.get_character_skills(character_name)
        
        if not skills:
            embed = EmbedGenerator.create_error_embed(
                f"No skills found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Find the specific skill
        target_skill = None
        for skill in skills:
            if skill.get('name', '').lower() == skill_name.lower():
                target_skill = skill
                break
        
        if not target_skill:
            embed = EmbedGenerator.create_error_embed(
                f"Skill '{skill_name}' not found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Create detailed skill embed
        embed = EmbedGenerator.create_embed(
            title=f"{character_name} - {target_skill['name']}",
            description=target_skill.get('description', 'No description available'),
            color=discord.Color.blue()
        )
        
        # Add skill details
        if 'cooldown' in target_skill:
            embed.add_field(name="Cooldown", value=target_skill['cooldown'], inline=True)
        
        if 'cost' in target_skill:
            embed.add_field(name="Cost", value=target_skill['cost'], inline=True)
        
        if 'range' in target_skill:
            embed.add_field(name="Range", value=target_skill['range'], inline=True)
        
        # Add skill levels
        if 'levels' in target_skill:
            levels_text = ""
            for level, details in target_skill['levels'].items():
                levels_text += f"**Level {level}**: {details}\n"
            embed.add_field(name="Skill Levels", value=levels_text, inline=False)
        
        # Add skill effects
        if 'effects' in target_skill:
            effects_text = ""
            for effect in target_skill['effects']:
                effects_text += f"• {effect}\n"
            embed.add_field(name="Effects", value=effects_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="talent")
    async def talent_info(self, ctx, character_name: str, *, talent_name: str):
        """Get detailed information about a specific talent."""
        talents = self.data_parser.get_character_talents(character_name)
        
        if not talents:
            embed = EmbedGenerator.create_error_embed(
                f"No talent tree found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Find the specific talent
        target_talent = None
        talent_tier = None
        
        for tier, tier_talents in talents.get('talents', {}).items():
            for talent in tier_talents:
                if talent.get('name', '').lower() == talent_name.lower():
                    target_talent = talent
                    talent_tier = tier
                    break
            if target_talent:
                break
        
        if not target_talent:
            embed = EmbedGenerator.create_error_embed(
                f"Talent '{talent_name}' not found for character '{character_name}'."
            )
            await ctx.send(embed=embed)
            return
        
        # Create detailed talent embed
        embed = EmbedGenerator.create_embed(
            title=f"{character_name} - {target_talent['name']}",
            description=target_talent.get('description', 'No description available'),
            color=discord.Color.purple()
        )
        
        # Add talent details
        if talent_tier:
            embed.add_field(name="Tier", value=talent_tier, inline=True)
        
        if 'cost' in target_talent:
            embed.add_field(name="Cost", value=target_talent['cost'], inline=True)
        
        if 'prerequisites' in target_talent:
            prereq_text = ""
            for prereq in target_talent['prerequisites']:
                prereq_text += f"• {prereq}\n"
            embed.add_field(name="Prerequisites", value=prereq_text, inline=False)
        
        if 'effects' in target_talent:
            effects_text = ""
            for effect in target_talent['effects']:
                effects_text += f"• {effect}\n"
            embed.add_field(name="Effects", value=effects_text, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="talent_trees")
    async def list_talent_trees(self, ctx):
        """List all available talent trees with their types."""
        try:
            talent_types_file = Path("HeroTalentImages/TalentType.txt")
            if not talent_types_file.exists():
                embed = EmbedGenerator.create_error_embed("Talent type information not found.")
                await ctx.send(embed=embed)
                return
            
            with open(talent_types_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the talent type information
            lines = content.split('\n')
            talent_types = {}
            
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith('Avatar Realms Collide') and not line.startswith('This document') and not line.startswith('General Talent') and not line.startswith('Dual Purpose') and not line.startswith('Total Points') and not line.startswith('"Drawn-on"') and not line.startswith('"Crossed-out"') and not line.startswith('Future Changes') and not line.startswith('Hero Talent') and not line.startswith('Below is a list'):
                    if line.endswith(':'):
                        continue
                    parts = line.split(':')
                    if len(parts) == 2:
                        char_name = parts[0].strip()
                        talent_type = parts[1].strip()
                        talent_types[char_name] = talent_type
            
            if not talent_types:
                embed = EmbedGenerator.create_error_embed("No talent type information found.")
                await ctx.send(embed=embed)
                return
            
            # Group by talent type
            type_groups = {}
            for char_name, talent_type in talent_types.items():
                if talent_type not in type_groups:
                    type_groups[talent_type] = []
                type_groups[talent_type].append(char_name)
            
            # Create embed
            embed = EmbedGenerator.create_embed(
                title="Available Talent Trees",
                description=f"Found {len(talent_types)} characters with talent trees",
                color=discord.Color.purple()
            )
            
            for talent_type, characters in type_groups.items():
                char_list = ", ".join(sorted(characters))
                embed.add_field(
                    name=f"{talent_type} ({len(characters)} characters)",
                    value=char_list,
                    inline=False
                )
            
            embed.add_field(
                name="Usage",
                value="Use `!character_talent <character_name>` to view a specific talent tree",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"Error loading talent tree information: {e}")
            await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(GameInfo(bot)) 