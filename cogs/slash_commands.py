"""
Slash commands cog for the Avatar Realms Collide Discord Bot.
Provides modern slash command interface for better user experience.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES
from pathlib import Path

class SlashCommands(commands.Cog):
    """Slash commands for modern Discord interface."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @app_commands.command(name="character", description="Get information about a specific character")
    @app_commands.describe(character_name="The name of the character")
    @app_commands.choices(character_name=[
        app_commands.Choice(name="Kyoshi", value="Kyoshi"),
        app_commands.Choice(name="Bumi", value="Bumi"),
        app_commands.Choice(name="Korra", value="Korra"),
        app_commands.Choice(name="Toph", value="Toph"),
        app_commands.Choice(name="Azula", value="Azula"),
        app_commands.Choice(name="Iroh", value="Iroh"),
        app_commands.Choice(name="Asami", value="Asami"),
        app_commands.Choice(name="Sokka", value="Sokka"),
        app_commands.Choice(name="Suki", value="Suki"),
        app_commands.Choice(name="Zuko", value="Zuko"),
        app_commands.Choice(name="Katara", value="Katara"),
        app_commands.Choice(name="Tenzin", value="Tenzin"),
        app_commands.Choice(name="Teo", value="Teo"),
        app_commands.Choice(name="Borte", value="Borte"),
        app_commands.Choice(name="Aang", value="Aang"),
        app_commands.Choice(name="Kuei", value="Kuei"),
        app_commands.Choice(name="Meelo", value="Meelo"),
        app_commands.Choice(name="Piandao", value="Piandao"),
        app_commands.Choice(name="Yue", value="Yue"),
        app_commands.Choice(name="Amon", value="Amon"),
        app_commands.Choice(name="King Bumi", value="King Bumi"),
        app_commands.Choice(name="Yangchen", value="Yangchen"),
        app_commands.Choice(name="Katara (Painted Lady)", value="Katara (Painted Lady)"),
        app_commands.Choice(name="Unalaq", value="Unalaq"),
        app_commands.Choice(name="Roku", value="Roku"),
        app_commands.Choice(name="Lin Beifong", value="Lin Beifong")
    ])
    async def character_info(self, interaction: discord.Interaction, character_name: str):
        """Get detailed information about a specific character."""
        await interaction.response.defer()
        
        character = self.data_parser.get_character(character_name)
        
        if not character:
            embed = EmbedGenerator.create_error_embed(
                f"Character '{character_name}' not found. Use `/characters` to see available characters."
            )
            await interaction.followup.send(embed=embed)
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
            value=f"Use `/character_skills {character['name']}` to see skills\n"
                  f"Use `/character_talent {character['name']}` to see talent tree",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="characters", description="List all available characters")
    async def list_characters(self, interaction: discord.Interaction):
        """List all available characters."""
        await interaction.response.defer()
        
        characters = self.data_parser.get_character_list()
        
        if not characters:
            embed = EmbedGenerator.create_error_embed("No characters found in the database.")
            await interaction.followup.send(embed=embed)
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
            value="Use `/character <name>` to get detailed information about a specific character.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="character_talent", description="Show talent tree for a specific character")
    @app_commands.describe(character_name="The name of the character")
    @app_commands.choices(character_name=[
        app_commands.Choice(name="Kyoshi", value="Kyoshi"),
        app_commands.Choice(name="Bumi", value="Bumi"),
        app_commands.Choice(name="Korra", value="Korra"),
        app_commands.Choice(name="Toph", value="Toph"),
        app_commands.Choice(name="Azula", value="Azula"),
        app_commands.Choice(name="Iroh", value="Iroh"),
        app_commands.Choice(name="Asami", value="Asami"),
        app_commands.Choice(name="Sokka", value="Sokka"),
        app_commands.Choice(name="Suki", value="Suki"),
        app_commands.Choice(name="Zuko", value="Zuko"),
        app_commands.Choice(name="Katara", value="Katara"),
        app_commands.Choice(name="Tenzin", value="Tenzin"),
        app_commands.Choice(name="Teo", value="Teo"),
        app_commands.Choice(name="Borte", value="Borte"),
        app_commands.Choice(name="Aang", value="Aang"),
        app_commands.Choice(name="Kuei", value="Kuei"),
        app_commands.Choice(name="Meelo", value="Meelo"),
        app_commands.Choice(name="Piandao", value="Piandao"),
        app_commands.Choice(name="Yue", value="Yue"),
        app_commands.Choice(name="Amon", value="Amon"),
        app_commands.Choice(name="King Bumi", value="King Bumi"),
        app_commands.Choice(name="Yangchen", value="Yangchen"),
        app_commands.Choice(name="Katara (Painted Lady)", value="Katara (Painted Lady)"),
        app_commands.Choice(name="Unalaq", value="Unalaq"),
        app_commands.Choice(name="Roku", value="Roku"),
        app_commands.Choice(name="Lin Beifong", value="Lin Beifong")
    ])
    async def character_talent(self, interaction: discord.Interaction, character_name: str):
        """Show talent tree for a specific character."""
        await interaction.response.defer()
        
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
            await interaction.followup.send(embed=embed)
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
        
        embed.set_footer(text="Use /character <name> for more character information")
        
        # Send embed with both images if available
        files = []
        if talent_images.get('talent_tree_1'):
            files.append(discord.File(talent_images['talent_tree_1'], filename=Path(talent_images['talent_tree_1']).name))
        if talent_images.get('talent_tree_2'):
            files.append(discord.File(talent_images['talent_tree_2'], filename=Path(talent_images['talent_tree_2']).name))
        
        if files:
            await interaction.followup.send(embed=embed, files=files)
        else:
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="talent_trees", description="List all available talent trees by type")
    async def list_talent_trees(self, interaction: discord.Interaction):
        """List all available talent trees with their types."""
        await interaction.response.defer()
        
        try:
            talent_types_file = Path("HeroTalentImages/TalentType.txt")
            if not talent_types_file.exists():
                embed = EmbedGenerator.create_error_embed("Talent type information not found.")
                await interaction.followup.send(embed=embed)
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
                await interaction.followup.send(embed=embed)
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
                value="Use `/character_talent <character_name>` to view a specific talent tree",
                inline=False
            )
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            embed = EmbedGenerator.create_error_embed(f"Error loading talent tree information: {e}")
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="search", description="Search for characters by name or description")
    @app_commands.describe(search_term="The search term to look for")
    async def search_characters(self, interaction: discord.Interaction, search_term: str):
        """Search for characters by name or description."""
        await interaction.response.defer()
        
        if len(search_term) < 2:
            embed = EmbedGenerator.create_error_embed("Search term must be at least 2 characters long.")
            await interaction.followup.send(embed=embed)
            return
        
        matches = self.data_parser.search_characters(search_term)
        
        if not matches:
            embed = EmbedGenerator.create_error_embed(
                f"No characters found matching '{search_term}'."
            )
            await interaction.followup.send(embed=embed)
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
            value="Use `/character <name>` to get detailed information about a character.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="server", description="Get the Discord server invite link")
    async def server(self, interaction: discord.Interaction):
        """Get the Discord server invite link."""
        embed = EmbedGenerator.create_embed(
            title="🎮 Join Our Community!",
            description="Connect with other Avatar Realms Collide players and get bot support.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Discord Server",
            value="[Click here to join!](https://discord.gg/a3tGyAwVRc)",
            inline=False
        )
        
        embed.add_field(
            name="What you'll find:",
            value="• Bot support and help\n• Game discussions\n• Character builds and strategies\n• Event coordination\n• Community features",
            inline=False
        )
        
        embed.add_field(
            name="Bot Features",
            value="• Character information and talent trees\n• Event tracking and notifications\n• User profiles and preferences\n• Search and comparison tools",
            inline=False
        )
        
        await interaction.response.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(SlashCommands(bot)) 