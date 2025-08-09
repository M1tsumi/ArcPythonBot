"""
Vote System: Encourage server growth through voting rewards.

This system provides voting links and rewards users with XP bonuses for supporting the server.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.embed_generator import EmbedGenerator


class VoteSystem(commands.Cog):
    """Vote system with XP bonuses for supporting the server."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vote_data_file = Path("data/system/vote_bonuses.json")
        self.vote_data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Voting sites configuration
        self.voting_sites = {
            "top.gg": {
                "name": "Top.gg",
                "url": "https://top.gg/discord/servers/741744324790493184",
                "emoji": "🏆",
                "description": "Vote for our server on Top.gg"
            },
            "discadia": {
                "name": "Discadia",
                "url": "https://discadia.com/server/arcbot/",
                "emoji": "⭐",
                "description": "Bump our server on Discadia"
            },
            "reddit": {
                "name": "Reddit Community",
                "url": "https://www.reddit.com/r/ArcUnofficialBot/",
                "emoji": "📱",
                "description": "Join our unofficial subreddit (Optional)"
            }
        }

    def _load_vote_data(self) -> Dict[str, Any]:
        """Load vote bonus data from file."""
        if not self.vote_data_file.exists():
            return {}
        
        try:
            with open(self.vote_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_vote_data(self, data: Dict[str, Any]) -> None:
        """Save vote bonus data to file."""
        try:
            with open(self.vote_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get_user_vote_bonus(self, user_id: int) -> float:
        """Get the current XP bonus multiplier for a user."""
        data = self._load_vote_data()
        user_str = str(user_id)
        
        if user_str not in data:
            return 1.0  # No bonus
        
        user_data = data[user_str]
        now = datetime.now(timezone.utc)
        
        # Check each voting site bonus
        total_multiplier = 1.0
        active_bonuses = []
        
        for site, bonus_data in user_data.items():
            if site in self.voting_sites:
                expires_at = datetime.fromisoformat(bonus_data["expires_at"])
                if now < expires_at:
                    total_multiplier += 4.0  # +400% (5x total when stacked)
                    active_bonuses.append(site)
        
        # Clean up expired bonuses
        if active_bonuses != list(user_data.keys()):
            for site in list(user_data.keys()):
                if site not in active_bonuses:
                    del user_data[site]
            
            if user_data:
                data[user_str] = user_data
            else:
                data.pop(user_str, None)
            
            self._save_vote_data(data)
        
        return min(total_multiplier, 16.0)  # Cap at 16x (3 sites + base = 1 + 4 + 4 + 4 + 3 buffer)

    def add_vote_bonus(self, user_id: int, site: str) -> bool:
        """Add a 24-hour 5x XP bonus for voting on a site."""
        if site not in self.voting_sites:
            return False
        
        data = self._load_vote_data()
        user_str = str(user_id)
        
        if user_str not in data:
            data[user_str] = {}
        
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        data[user_str][site] = {
            "voted_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at.isoformat()
        }
        
        self._save_vote_data(data)
        return True

    def get_user_vote_status(self, user_id: int) -> Dict[str, Any]:
        """Get detailed voting status for a user."""
        data = self._load_vote_data()
        user_str = str(user_id)
        now = datetime.now(timezone.utc)
        
        status = {
            "active_bonuses": [],
            "expired_sites": [],
            "never_voted": [],
            "total_multiplier": 1.0
        }
        
        user_data = data.get(user_str, {})
        
        for site_key, site_info in self.voting_sites.items():
            if site_key in user_data:
                expires_at = datetime.fromisoformat(user_data[site_key]["expires_at"])
                if now < expires_at:
                    hours_left = (expires_at - now).total_seconds() / 3600
                    status["active_bonuses"].append({
                        "site": site_key,
                        "name": site_info["name"],
                        "hours_left": hours_left
                    })
                    status["total_multiplier"] += 4.0
                else:
                    status["expired_sites"].append(site_key)
            else:
                status["never_voted"].append(site_key)
        
        status["total_multiplier"] = min(status["total_multiplier"], 16.0)
        return status

    @app_commands.command(name="vote", description="🗳️ Vote for the server and get amazing XP bonuses!")
    async def vote(self, interaction: discord.Interaction):
        """Display voting links and current bonus status."""
        user_id = interaction.user.id
        status = self.get_user_vote_status(user_id)
        
        # Create main embed (without caching to prevent duplication)
        embed = discord.Embed(
            title="🗳️ Vote for Avatar Realms Collide!",
            description="Support our community and earn **massive XP bonuses**!\n\n**Each vote gives you 5x XP for 24 hours and they STACK!**",
            color=discord.Color.gold()
        )
        
        # Add voting sites
        voting_links = []
        for site_key, site_info in self.voting_sites.items():
            if site_key == "reddit":
                voting_links.append(f"{site_info['emoji']} **[{site_info['name']}]({site_info['url']})**\n{site_info['description']}")
            else:
                voting_links.append(f"{site_info['emoji']} **[{site_info['name']}]({site_info['url']})**\n{site_info['description']}")
        
        embed.add_field(
            name="📊 Voting Sites",
            value="\n\n".join(voting_links),
            inline=False
        )
        
        # Current bonus status
        if status["active_bonuses"]:
            bonus_text = []
            for bonus in status["active_bonuses"]:
                hours = int(bonus["hours_left"])
                minutes = int((bonus["hours_left"] - hours) * 60)
                bonus_text.append(f"🔥 **{bonus['name']}**: {hours}h {minutes}m remaining")
            
            embed.add_field(
                name="🎁 Active Bonuses",
                value="\n".join(bonus_text),
                inline=True
            )
        
        # Show total multiplier
        multiplier = status["total_multiplier"]
        if multiplier > 1.0:
            embed.add_field(
                name="⚡ Current XP Multiplier",
                value=f"**{multiplier:.1f}x** XP Bonus!",
                inline=True
            )
        else:
            embed.add_field(
                name="💡 Potential Bonus",
                value="Vote to get **5x XP** per site!\n*Up to 13x XP total!*",
                inline=True
            )
        
        # Instructions
        embed.add_field(
            name="📋 How to Claim Bonuses",
            value="1️⃣ Click the voting links above\n2️⃣ Vote/bump our server\n3️⃣ Use `/vote claim <site>` to activate bonus\n\n*Example: `/vote claim top.gg`*",
            inline=False
        )
        
        embed.set_footer(text="💖 Thank you for supporting Avatar Realms Collide!")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="vote_claim", description="🎁 Claim your XP bonus after voting!")
    @app_commands.describe(site="Which site did you vote on?")
    @app_commands.choices(site=[
        app_commands.Choice(name="Top.gg", value="top.gg"),
        app_commands.Choice(name="Discadia", value="discadia"),
        app_commands.Choice(name="Reddit (Joined)", value="reddit"),
    ])
    async def vote_claim(self, interaction: discord.Interaction, site: app_commands.Choice[str]):
        """Claim XP bonus after voting."""
        user_id = interaction.user.id
        site_key = site.value
        
        if site_key not in self.voting_sites:
            await interaction.response.send_message("❌ Invalid voting site!", ephemeral=True)
            return
        
        # Check if user already has active bonus for this site
        status = self.get_user_vote_status(user_id)
        for bonus in status["active_bonuses"]:
            if bonus["site"] == site_key:
                hours = int(bonus["hours_left"])
                minutes = int((bonus["hours_left"] - hours) * 60)
                await interaction.response.send_message(
                    f"⏰ You already have an active bonus for **{self.voting_sites[site_key]['name']}**!\n"
                    f"Time remaining: **{hours}h {minutes}m**",
                    ephemeral=True
                )
                return
        
        # Add the bonus
        success = self.add_vote_bonus(user_id, site_key)
        if success:
            # Get updated status
            new_status = self.get_user_vote_status(user_id)
            multiplier = new_status["total_multiplier"]
            
            embed = discord.Embed(
                title="🎉 Vote Bonus Activated!",
                description=f"Thank you for voting on **{self.voting_sites[site_key]['name']}**!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="🔥 Bonus Activated",
                value=f"**5x XP** for the next **24 hours**!",
                inline=True
            )
            
            embed.add_field(
                name="⚡ Total Multiplier",
                value=f"**{multiplier:.1f}x** XP Bonus",
                inline=True
            )
            
            if len(new_status["active_bonuses"]) < 3:
                remaining_sites = [self.voting_sites[s]["name"] for s in new_status["never_voted"] + new_status["expired_sites"]]
                if remaining_sites:
                    embed.add_field(
                        name="💡 Stack More Bonuses",
                        value=f"Vote on: {', '.join(remaining_sites[:2])}{'...' if len(remaining_sites) > 2 else ''}",
                        inline=False
                    )
            
            embed.set_footer(text="🚀 Go earn some XP with your new bonus!")
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Failed to activate bonus. Please try again!", ephemeral=True)

    @app_commands.command(name="vote_status", description="📊 Check your current voting bonuses")
    async def vote_status(self, interaction: discord.Interaction):
        """Check current voting bonus status."""
        user_id = interaction.user.id
        status = self.get_user_vote_status(user_id)
        
        embed = discord.Embed(
            title="📊 Your Voting Status",
            color=discord.Color.blue()
        )
        
        # Current multiplier
        multiplier = status["total_multiplier"]
        if multiplier > 1.0:
            embed.add_field(
                name="⚡ Current XP Multiplier",
                value=f"**{multiplier:.1f}x** XP Bonus!",
                inline=True
            )
        else:
            embed.add_field(
                name="💡 No Active Bonuses",
                value="Use `/vote` to get started!",
                inline=True
            )
        
        # Active bonuses
        if status["active_bonuses"]:
            bonus_text = []
            for bonus in status["active_bonuses"]:
                hours = int(bonus["hours_left"])
                minutes = int((bonus["hours_left"] - hours) * 60)
                bonus_text.append(f"🔥 **{bonus['name']}**: {hours}h {minutes}m")
            
            embed.add_field(
                name="🎁 Active Bonuses",
                value="\n".join(bonus_text),
                inline=True
            )
        
        # Available votes
        available_sites = status["never_voted"] + status["expired_sites"]
        if available_sites:
            site_names = [self.voting_sites[site]["name"] for site in available_sites]
            embed.add_field(
                name="🗳️ Available Votes",
                value="\n".join([f"• {name}" for name in site_names]),
                inline=False
            )
        
        if not status["active_bonuses"] and not available_sites:
            embed.add_field(
                name="🏆 All Bonuses Active!",
                value="You're getting maximum XP rewards!",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(VoteSystem(bot))
