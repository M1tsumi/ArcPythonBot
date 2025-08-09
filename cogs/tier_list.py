"""
Tier List commands cog for the Avatar Realms Collide Discord Bot.
Shows the current community tier list image.
"""

import os
from pathlib import Path
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from utils.embed_generator import EmbedGenerator


TIERLIST_DEFAULT_PATHS = [
    Path("assets/images/leaderboards/hero-tierlist.webp"),
    Path("assets/images/leaderboards/hero-tierlist.png"),
    Path("assets/images/leaderboards/hero-tierlist.jpg"),
    Path("assets/images/characters/hero-tierlist.webp"),
]


class TierList(commands.Cog):
    """Tier list command cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = bot.logger

    def _find_tierlist_file(self) -> Optional[Path]:
        for p in TIERLIST_DEFAULT_PATHS:
            if p.exists() and p.is_file():
                return p
        return None

    @app_commands.command(name="tierlist", description="Show the community hero tier list")
    @app_commands.checks.cooldown(1, 10.0)
    async def tierlist(self, interaction: discord.Interaction):
        """Send the current community tier list image in an embed."""
        try:
            file_path = self._find_tierlist_file()

            embed = EmbedGenerator.create_embed(
                title="Community Hero Tier List",
                description=(
                    "Curated by the community. Criteria consider overall PvE/PvP performance, versatility, and availability.\n"
                    "Note: Tier lists are subjective and may evolve with updates."
                ),
                color=discord.Color.gold(),
            )

            if file_path:
                file = discord.File(file_path, filename=file_path.name)
                embed.set_image(url=f"attachment://{file_path.name}")
                embed = EmbedGenerator.finalize_embed(embed)
                await interaction.response.send_message(embed=embed, file=file)
                return

            # Graceful fallback if the image file isn't present
            embed.add_field(
                name="Image Not Found",
                value=(
                    "Tier list image was not found on disk. Place the image at one of the following paths and rerun:\n"
                    "• assets/images/leaderboards/hero-tierlist.webp\n"
                    "• assets/images/leaderboards/hero-tierlist.png\n"
                    "• assets/images/leaderboards/hero-tierlist.jpg"
                ),
                inline=False,
            )
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            error_embed = EmbedGenerator.create_error_embed(f"Failed to send tier list: {e}")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(TierList(bot))


