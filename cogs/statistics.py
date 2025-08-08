import asyncio
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import discord
from discord import app_commands
from discord.ext import commands


class Statistics(commands.Cog):
    """Tracks bot command usage and exposes an owner-only /statistics command."""

    # Keep in sync with the owner check used in Utility (/servers)
    AUTHORIZED_USER_ID: int = 1051142172130422884

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = getattr(bot, "logger", None) or discord.utils.setup_logging()

        # Storage
        self.data_file_path: Path = Path("data/usage_stats.json")
        self.data_file_path.parent.mkdir(parents=True, exist_ok=True)
        self._io_lock: asyncio.Lock = asyncio.Lock()

        # In-memory stats cache
        self.stats: Dict[str, Any] = {
            "total": 0,
            "type_counts": {"slash": 0, "prefix": 0},
            "per_user": {},          # user_id -> count
            "per_command": {},       # command_name -> count
            "per_guild": {},         # guild_id -> count
            "per_channel": {},       # channel_id -> count
            "daily": {},             # YYYY-MM-DD -> count
            "recent": deque(maxlen=25),  # list of recent events
            "last_updated": None,
        }

        # Load persisted stats if present
        self._load_stats_from_disk()

    # ------------------------
    # Event Listeners
    # ------------------------
    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        """Record successful prefix command usage."""
        try:
            command_name = ctx.command.qualified_name if ctx.command else "unknown"
            user_id = ctx.author.id if ctx and ctx.author else None
            guild_id = ctx.guild.id if ctx and ctx.guild else None
            channel_id = ctx.channel.id if ctx and ctx.channel else None
            await self._record_event(
                command_name=command_name,
                user_id=user_id,
                guild_id=guild_id,
                channel_id=channel_id,
                command_type="prefix",
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to record prefix command usage: {e}")

    @commands.Cog.listener()
    async def on_app_command_completion(
        self, interaction: discord.Interaction, command: app_commands.Command
    ) -> None:
        """Record successful slash command usage."""
        try:
            command_name = (
                getattr(command, "qualified_name", None)
                or (interaction.command.qualified_name if interaction and interaction.command else "unknown")
                or "unknown"
            )
            user_id = interaction.user.id if interaction and interaction.user else None
            guild_id = interaction.guild.id if interaction and interaction.guild else None
            channel_id = interaction.channel.id if interaction and interaction.channel else None
            await self._record_event(
                command_name=command_name,
                user_id=user_id,
                guild_id=guild_id,
                channel_id=channel_id,
                command_type="slash",
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to record slash command usage: {e}")

    # ------------------------
    # Owner-only Command
    # ------------------------
    @app_commands.command(name="statistics", description="View bot usage analytics (Owner only)")
    async def statistics(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.AUTHORIZED_USER_ID:
            embed = discord.Embed(
                title="Access Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)
            # Use a snapshot to avoid race conditions while rendering
            async with self._io_lock:
                stats_snapshot = json.loads(json.dumps(self._normalize_for_json(self.stats)))

            embed = self._build_statistics_embed(stats_snapshot)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"An error occurred while generating statistics: {e}",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

    # ------------------------
    # Internal Helpers
    # ------------------------
    async def _record_event(
        self,
        *,
        command_name: str,
        user_id: Optional[int],
        guild_id: Optional[int],
        channel_id: Optional[int],
        command_type: str,
    ) -> None:
        """Update counters in memory and persist to disk."""
        now = datetime.now(timezone.utc)
        day_key = now.strftime("%Y-%m-%d")

        async with self._io_lock:
            # Totals
            self.stats["total"] = int(self.stats.get("total", 0)) + 1
            type_counts = self.stats.setdefault("type_counts", {"slash": 0, "prefix": 0})
            type_counts[command_type] = int(type_counts.get(command_type, 0)) + 1

            # Per-command
            per_cmd = self.stats.setdefault("per_command", {})
            per_cmd[command_name] = int(per_cmd.get(command_name, 0)) + 1

            # Per-user
            if user_id is not None:
                per_user = self.stats.setdefault("per_user", {})
                per_user[str(user_id)] = int(per_user.get(str(user_id), 0)) + 1

            # Per-guild
            if guild_id is not None:
                per_guild = self.stats.setdefault("per_guild", {})
                per_guild[str(guild_id)] = int(per_guild.get(str(guild_id), 0)) + 1

            # Per-channel
            if channel_id is not None:
                per_channel = self.stats.setdefault("per_channel", {})
                per_channel[str(channel_id)] = int(per_channel.get(str(channel_id), 0)) + 1

            # Daily
            daily = self.stats.setdefault("daily", {})
            daily[day_key] = int(daily.get(day_key, 0)) + 1

            # Recent
            recent = self.stats.setdefault("recent", deque(maxlen=25))
            # deque is not JSON-serializable, but we normalize when persisting
            recent.appendleft(
                {
                    "t": now.isoformat(),
                    "u": user_id,
                    "g": guild_id,
                    "ch": channel_id,
                    "cmd": command_name,
                    "type": command_type,
                }
            )

            self.stats["last_updated"] = now.isoformat()

            # Persist
            self._save_stats_to_disk_unlocked()

    def _normalize_for_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert non-JSON types (e.g., deque) to JSON-friendly structures."""
        normalized = dict(data)
        if isinstance(normalized.get("recent"), deque):
            normalized["recent"] = list(normalized["recent"])  # newest first
        return normalized

    def _load_stats_from_disk(self) -> None:
        try:
            if self.data_file_path.exists():
                with open(self.data_file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Restore into our structure
                self.stats.update(loaded)
                # Re-wrap recent as deque for efficient updates
                if isinstance(self.stats.get("recent"), list):
                    self.stats["recent"] = deque(self.stats["recent"], maxlen=25)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to load usage stats: {e}")

    def _save_stats_to_disk_unlocked(self) -> None:
        try:
            serializable = self._normalize_for_json(self.stats)
            with open(self.data_file_path, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, ensure_ascii=False)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to save usage stats: {e}")

    def _build_statistics_embed(self, stats: Dict[str, Any]) -> discord.Embed:
        """Builds a rich embed with key analytics for the owner."""
        embed = discord.Embed(
            title="📈 Bot Usage Statistics",
            description="Analytics overview of how the bot is being used",
            color=discord.Color.blurple(),
            timestamp=discord.utils.utcnow(),
        )

        total = int(stats.get("total", 0))
        type_counts = stats.get("type_counts", {})
        per_user = stats.get("per_user", {})
        per_cmd = stats.get("per_command", {})
        per_guild = stats.get("per_guild", {})
        daily = stats.get("daily", {})

        unique_users = len(per_user)
        unique_guilds = len(per_guild)
        today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        today_count = int(daily.get(today_key, 0))

        # Decorate with bot identity if available
        try:
            if self.bot.user:
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        except Exception:
            pass

        embed.add_field(
            name="Overview",
            value=(
                f"Total Commands: **{total:,}**\n"
                f"Slash: **{int(type_counts.get('slash', 0)):,}** | Prefix: **{int(type_counts.get('prefix', 0)):,}**\n"
                f"Unique Users: **{unique_users:,}**\n"
                f"Unique Servers: **{unique_guilds:,}**\n"
                f"Today: **{today_count:,}**"
            ),
            inline=False,
        )

        # Top Users
        if per_user:
            top_users = sorted(per_user.items(), key=lambda kv: kv[1], reverse=True)[:10]
            user_lines = []
            for rank, (uid_str, count) in enumerate(top_users, start=1):
                try:
                    uid_int = int(uid_str)
                    user_lines.append(f"{rank}. <@{uid_int}> — {int(count):,}")
                except Exception:
                    user_lines.append(f"{rank}. {uid_str} — {int(count):,}")
            embed.add_field(name="Top Users", value="\n".join(user_lines), inline=True)

        # Top Commands
        if per_cmd:
            top_cmds = sorted(per_cmd.items(), key=lambda kv: kv[1], reverse=True)[:10]
            cmd_lines = [f"{i}. /{name} — {int(cnt):,}" for i, (name, cnt) in enumerate(top_cmds, start=1)]
            embed.add_field(name="Top Commands", value="\n".join(cmd_lines), inline=True)

        # Top Servers
        if per_guild:
            top_guilds = sorted(per_guild.items(), key=lambda kv: kv[1], reverse=True)[:10]
            guild_lines = []
            for rank, (gid_str, count) in enumerate(top_guilds, start=1):
                try:
                    gid_int = int(gid_str)
                    guild_obj = self.bot.get_guild(gid_int)
                    guild_name = guild_obj.name if guild_obj else gid_str
                    guild_lines.append(f"{rank}. {guild_name} — {int(count):,}")
                except Exception:
                    guild_lines.append(f"{rank}. {gid_str} — {int(count):,}")
            embed.add_field(name="Top Servers", value="\n".join(guild_lines), inline=False)

        # Last 7 days
        if daily:
            last_7 = self._last_n_days_series(daily, days=7)
            series_lines = [f"{d}: {c:,}" for d, c in last_7]
            embed.add_field(name="Last 7 Days", value="\n".join(series_lines), inline=False)

        # Recent activity
        recent = stats.get("recent", [])
        if recent:
            preview = recent[:10]
            lines = []
            for item in preview:
                user_mention = f"<@{item.get('u')}>" if item.get('u') else "Unknown"
                cmd_name = item.get('cmd') or 'unknown'
                when = self._short_ts(item.get('t'))
                lines.append(f"{when} — /{cmd_name} by {user_mention}")
            embed.add_field(name="Recent", value="\n".join(lines), inline=False)

        embed.set_footer(text="Owner-only statistics • Updated live")
        return embed

    def _last_n_days_series(self, daily_map: Dict[str, Any], *, days: int) -> Tuple[Tuple[str, int], ...]:
        """Return a tuple of (date_str, count) for the last N days inclusive of today."""
        out = []
        today = datetime.now(timezone.utc).date()
        for i in range(days - 1, -1, -1):
            d = today.fromordinal(today.toordinal() - i)
            key = d.strftime("%Y-%m-%d")
            out.append((key, int(daily_map.get(key, 0))))
        return tuple(out)

    def _short_ts(self, iso: Optional[str]) -> str:
        if not iso:
            return "unknown"
        try:
            dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            return dt.strftime("%m-%d %H:%M")
        except Exception:
            return iso


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Statistics(bot))


