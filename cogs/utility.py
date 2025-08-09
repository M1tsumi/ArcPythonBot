"""
Utility command module for Avatar Realms Collide Discord Bot.
Provides utility commands like links, help, ping, info, and bot management.
"""

import time
import discord
from discord import app_commands
from discord.ext import commands
from config.settings import DISCORD_SERVER_LINK, BOT_INVITE_LINK, DEVELOPMENT_SERVER_LINK
from utils.embed_generator import EmbedGenerator

class Utility(commands.Cog):
    """Utility command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    # ===== Prefix commands =====

    @commands.command(name="ping", description="Check bot latency and status")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping_prefix(self, ctx):
        """Traditional prefix command to check bot latency and status."""
        start_time = time.time()

        embed = EmbedGenerator.create_embed(
            title="Pong!",
            description="Checking bot status and latency...",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        api_latency = round(self.bot.latency * 1000, 2)

        embed = EmbedGenerator.create_embed(
            title="Pong!",
            description="Bot is online and responding.",
            color=discord.Color.green()
        )
        embed.add_field(name="📊 Response Time", value=f"**{latency:.1f}ms**", inline=True)
        embed.add_field(name="🌐 API Latency", value=f"**{api_latency}ms**", inline=True)
        embed.add_field(name="🆔 Bot Status", value="✅ Online and Ready", inline=True)
        embed.add_field(name="🏠 Servers", value=f"**{len(self.bot.guilds)}** servers", inline=True)
        embed.add_field(name="👥 Users", value=f"**{len(self.bot.users)}** users", inline=True)
        embed.add_field(name="⚡ Commands", value=f"**{len(self.bot.tree.get_commands())}** slash commands", inline=True)

        embed = EmbedGenerator.finalize_embed(embed)
        await message.edit(embed=embed)

    # RENAMED from "help" -> "uhelp" to avoid conflict with built-in HelpCommand
    @commands.command(name="uhelp", description="Get help and command information")
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def help_prefix(self, ctx):
        """Traditional prefix command to provide help and command information."""
        embed = EmbedGenerator.create_embed(
            title="Help",
            description="Available commands organized by category.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🎮 Game Information Commands",
            value="• `!talent_trees` - Browse character talent trees\n• `!skill_priorities` - View hero skill priorities\n• `!hero_info` - Get detailed hero information\n• `!hero_rankup` - View hero rankup guide and costs\n• `!townhall` - View town hall requirements\n• `!leaderboard` - Check top players and alliances",
            inline=False
        )
        embed.add_field(
            name="🎭 Event Commands",
            value="• `!events` - View current and upcoming events\n• `!avatar_day_festival` - Avatar Day Festival information\n• `!festival_tasks` - View all festival tasks by day\n• `!festival_shop` - View festival exchange shop\n• `!festival_guide` - Get festival tips and strategy\n• `!festival_rewards` - View all festival rewards\n• `!balance_and_order` - Balance and Order event information\n• `!balance_tasks` - View Balance and Order tasks\n• `!balance_guide` - Get Balance and Order tips\n• `!borte_scheme` - Borte's Scheme event information\n• `!borte_mechanics` - View Borte's Scheme mechanics\n• `!borte_rewards` - View Borte's Scheme rewards\n• `!borte_guide` - Get Borte's Scheme tips",
            inline=False
        )
        embed.add_field(
            name="⚔️ Rally System Commands",
            value="• `!setup` - Setup rally system (Admin)\n• `!rally` - Create a new rally (level + time limit)\n• `!rally_stats` - View your rally statistics\n• `!rally_leaderboard` - View rally leaderboard\n• `!leader` - Admin leaderboard management (pause/resume/clear)",
            inline=False
        )
        embed.add_field(
            name="🏆 TGL Commands",
            value="• `!tgl` - The Greatest Leader event information\n• `!tgl_calc` - Calculate TGL points for activities",
            inline=False
        )
        embed.add_field(
            name="🔧 Utility Commands",
            value="• `!ping` - Check bot status and latency\n• `!info` - Comprehensive bot information\n• `!links` - Get bot links and information\n• `!addtoserver` - Add bot to your server",
            inline=False
        )
        embed.add_field(
            name="📱 Join Our Discord Server",
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\nGet help, ask questions, and connect with other players!",
            inline=False
        )

        embed = EmbedGenerator.finalize_embed(embed)
        await ctx.send(embed=embed)

    @commands.command(name="info", description="Get comprehensive bot information and contribution details")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def info_prefix(self, ctx):
        """Traditional prefix command to provide comprehensive bot information and contribution details."""
        embed = EmbedGenerator.create_embed(
            title="Bot Information",
            description="Unofficial community bot providing game tools and information.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🎮 Key Features",
            value="• Talent Trees & Hero Info\n• Leaderboards & Rally System\n• Event Tools & Timers\n• Town Hall & Skill Guides",
            inline=False
        )
        embed.add_field(
            name="👨‍💻 Developer & Contributors",
            value="**Developed by Quefep**\n**Contributors**: Lycaris (comprehensive event overview), PrincessBell & Samkee (event details), Deng (@2rk) (leaderboards), Kuvira (talent trees, skill priorities, town hall stats)",
            inline=False
        )
        embed.add_field(
            name="📊 Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}",
            inline=False
        )
        embed.add_field(
            name="🤝 Contribute",
            value="Share game data, images, or resources! Contact **quefep** on Discord.",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)

        view = discord.ui.View(timeout=None)
        dev_server_button = discord.ui.Button(
            label="Join Development Server",
            url=DEVELOPMENT_SERVER_LINK,
            style=discord.ButtonStyle.link,
            emoji="🔗"
        )
        view.add_item(dev_server_button)

        await ctx.send(embed=embed, view=view)

    # ===== Slash commands =====

    @app_commands.command(name="ping", description="Check bot latency and status")
    @app_commands.checks.cooldown(1, 5.0)
    async def ping(self, interaction: discord.Interaction):
        """Slash command to check bot latency and status."""
        start_time = time.time()
        await interaction.response.send_message("Checking bot status...")

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        api_latency = round(self.bot.latency * 1000, 2)

        embed = EmbedGenerator.create_ping_embed(
            latency=latency,
            api_latency=api_latency,
            guild_count=len(self.bot.guilds),
            user_count=len(self.bot.users),
            command_count=len(self.bot.tree.get_commands())
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.edit_original_response(content=None, embed=embed)

    @app_commands.command(name="info", description="Get comprehensive bot information and contribution details")
    @app_commands.checks.cooldown(1, 10.0)
    async def info(self, interaction: discord.Interaction):
        """Slash command to provide comprehensive bot information and contribution details."""
        embed = EmbedGenerator.create_embed(
            title="Bot Information",
            description="Unofficial community bot providing game tools and information.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Key Features",
            value="• Talent Trees & Hero Info\n• Leaderboards & Rally System\n• Event Tools & Timers\n• Town Hall & Skill Guides",
            inline=False
        )
        embed.add_field(
            name="Developer & Contributors",
            value="**Developed by Quefep**\n**Contributors**: Lycaris (comprehensive event overview), PrincessBell & Samkee (event details), Deng (@2rk) (leaderboards), Kuvira (talent trees, skill priorities, town hall stats), Drummer (@priskent) & Marshmellow (@sophremacy) (troop information and costs)",
            inline=False
        )
        embed.add_field(
            name="Statistics",
            value=f"• **Servers**: {len(self.bot.guilds)}\n• **Users**: {len(self.bot.users)}\n• **Commands**: {len(self.bot.tree.get_commands())}",
            inline=False
        )
        embed.add_field(
            name="Contribute",
            value="Share game data, images, or resources! Contact **quefep** on Discord.",
            inline=False
        )

        embed = EmbedGenerator.finalize_embed(embed)

        view = discord.ui.View(timeout=None)
        dev_server_button = discord.ui.Button(
            label="Join Development Server",
            url=DEVELOPMENT_SERVER_LINK,
            style=discord.ButtonStyle.link
        )
        view.add_item(dev_server_button)

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="links", description="Get bot links and information")
    @app_commands.checks.cooldown(1, 10.0)
    async def links(self, interaction: discord.Interaction):
        """Slash command to provide bot links and information."""
        embed = EmbedGenerator.create_embed(
            title="Links & Information",
            description="Connect with the Avatar Realms Collide community.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Join Our Discord Server", value=f"[Join Server]({DISCORD_SERVER_LINK})", inline=True)
        embed.add_field(name="Add Bot to Your Server", value=f"[Add to Server]({BOT_INVITE_LINK})", inline=True)
        embed.add_field(name="Developer", value="**Developed by Quefep**", inline=False)
        embed.add_field(
            name="Bot Features",
            value="• Talent Tree Browser\n• Skill Priorities\n• Leaderboards\n• Town Hall Info\n• Hero Rankup Guide\n• Interactive Commands",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Get help and join our Discord server")
    @app_commands.checks.cooldown(1, 10.0)
    async def help(self, interaction: discord.Interaction):
        """Slash command to provide help and Discord server link."""
        embed = EmbedGenerator.create_embed(
            title="Help",
            description="How to get help and stay connected.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Join Our Discord Server",
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\nGet help, ask questions, and connect with other players!",
            inline=False
        )
        embed.add_field(
            name="Game Information Commands",
            value="• `/talent_trees` - Browse character talent trees\n• `/skill_priorities` - View hero skill priorities\n• `/hero_info` - Get detailed hero information\n• `/hero_rankup` - View hero rankup guide and costs\n• `/townhall` - View town hall requirements\n• `/leaderboard` - Check top players and alliances",
            inline=False
        )
        embed.add_field(
            name="Event Commands",
            value="• `/events` - View current and upcoming events\n• `/avatar_day_festival` - Avatar Day Festival information\n• `/festival_tasks` - View all festival tasks by day\n• `/festival_shop` - View festival exchange shop\n• `/festival_guide` - Get festival tips and strategy\n• `/festival_rewards` - View all festival rewards\n• `/balance_and_order` - Balance and Order event information\n• `/balance_tasks` - View Balance and Order tasks\n• `/balance_guide` - Get Balance and Order tips\n• `/borte_scheme` - Borte's Scheme event information\n• `/borte_mechanics` - View Borte's Scheme mechanics\n• `/borte_rewards` - View Borte's Scheme rewards\n• `/borte_guide` - Get Borte's Scheme tips",
            inline=False
        )
        embed.add_field(
            name="Rally System Commands",
            value="• `/setup` - Setup rally system (Admin)\n• `/rally` - Create a new rally (level + time limit)\n• `/rally_stats` - View your rally statistics\n• `/rally_leaderboard` - View rally leaderboard\n• `/leader` - Admin leaderboard management (pause/resume/clear)",
            inline=False
        )
        embed.add_field(
            name="TGL Commands",
            value="• `/tgl` - The Greatest Leader event information\n• `/tgl_calc` - Calculate TGL points for activities",
            inline=False
        )
        embed.add_field(
            name="🔧 Utility Commands",
            value="• `/ping` - Check bot status and latency\n• `/info` - Comprehensive bot information\n• `/links` - Get bot links and information\n• `/addtoserver` - Add bot to your server",
            inline=False
        )
        embed.add_field(
            name="💡 Need More Help?",
            value="Join our Discord server for:\n• Real-time help and support\n• Game updates and announcements\n• Community discussions\n• Bug reports and suggestions\n• Contribution opportunities",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addtoserver", description="Add the bot to your server")
    @app_commands.checks.cooldown(1, 30.0)
    async def addtoserver(self, interaction: discord.Interaction):
        """Slash command to add the bot to a server with an embed and button."""
        embed = EmbedGenerator.create_embed(
            title="Add Bot to Your Server",
            description="Enhance your server with powerful game tools and community features.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="🎮 Bot Features",
            value="• **Talent Tree Browser** - View all character talent trees\n• **Skill Priorities** - Get optimal skill upgrade orders\n• **Leaderboards** - Track top players and alliances\n• **Town Hall Info** - View upgrade requirements\n• **Hero Rankup Guide** - Complete rankup costs and guide\n• **Event System** - Current and upcoming events\n• **Rally System** - Create and join Shattered Skulls Fortress rallies\n• **Interactive Commands** - Modern slash command interface",
            inline=False
        )
        embed.add_field(
            name="🔧 Permissions Required",
            value="• Send Messages\n• Embed Links\n• Attach Files\n• Use Slash Commands\n• Read Message History",
            inline=False
        )
        embed.add_field(
            name="📱 Community",
            value=f"[Join our Discord server]({DISCORD_SERVER_LINK}) for support and updates!",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)

        view = discord.ui.View(timeout=None)
        invite_button = discord.ui.Button(
            label="Add to Server",
            url=BOT_INVITE_LINK,
            style=discord.ButtonStyle.link,
            emoji="🤖"
        )
        view.add_item(invite_button)

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="servers", description="View bot server statistics and information (Owner only)")
    async def server_stats(self, interaction: discord.Interaction):
        """Command to show professional server statistics and information."""
        AUTHORIZED_USER_ID = 1051142172130422884

        if interaction.user.id != AUTHORIZED_USER_ID:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don't have permission to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)

            total_servers = len(self.bot.guilds)
            total_members = sum(g.member_count for g in self.bot.guilds)
            avg_members = total_members / total_servers if total_servers > 0 else 0

            top_servers = sorted(self.bot.guilds, key=lambda g: g.member_count, reverse=True)[:10]

            embed = discord.Embed(
                title="🏠 Bot Server Statistics",
                description="Comprehensive overview of bot server distribution and performance",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="📊 Overview",
                value=f"**Total Servers**: {total_servers:,}\n"
                      f"**Total Members**: {total_members:,}\n"
                      f"**Average Members/Server**: {avg_members:.0f}",
                inline=True
            )

            large_servers = len([g for g in self.bot.guilds if g.member_count >= 1000])
            medium_servers = len([g for g in self.bot.guilds if 100 <= g.member_count < 1000])
            small_servers = len([g for g in self.bot.guilds if g.member_count < 100])

            embed.add_field(
                name="📈 Distribution",
                value=f"**Large Servers** (1k+): {large_servers}\n"
                      f"**Medium Servers** (100-999): {medium_servers}\n"
                      f"**Small Servers** (<100): {small_servers}",
                inline=True
            )

            recent_servers = [
                g for g in self.bot.guilds
                if g.me.joined_at and (discord.utils.utcnow() - g.me.joined_at).days <= 30
            ]
            embed.add_field(
                name="🆕 Recent Activity",
                value=f"**Joined Last 30 Days**: {len(recent_servers)}\n"
                      f"**Active Servers**: {len([g for g in self.bot.guilds if g.member_count > 0])}\n"
                      f"**Bot Commands**: {len(self.bot.tree.get_commands())}",
                inline=True
            )

            top_servers_text = ""
            for i, guild in enumerate(top_servers, 1):
                owner_name = guild.owner.display_name if guild.owner else "Unknown"
                joined_date = guild.me.joined_at.strftime('%m/%d') if guild.me.joined_at else "Unknown"

                invite_link = "No permission"
                try:
                    invite_channel = None
                    for channel in guild.channels:
                        if (isinstance(channel, discord.TextChannel) and
                            channel.permissions_for(guild.me).create_instant_invite):
                            invite_channel = channel
                            break
                    if invite_channel:
                        invite = await invite_channel.create_invite(max_age=0, max_uses=0)
                        invite_link = invite.url
                except Exception:
                    invite_link = "Error creating invite"

                top_servers_text += f"**{i}.** {guild.name}\n"
                top_servers_text += f"👥 {guild.member_count:,} members | 👑 {owner_name} | 📅 {joined_date}\n"
                top_servers_text += f"🔗 {invite_link}\n\n"

            embed.add_field(
                name="🏆 Top 10 Servers",
                value=top_servers_text if top_servers_text else "No servers found",
                inline=False
            )
            embed.add_field(
                name="⚡ Performance",
                value=f"**Bot Latency**: {round(self.bot.latency * 1000, 1)}ms\n"
                      f"**Uptime**: {self._format_uptime()}\n"
                      f"**Memory Usage**: {self._get_memory_usage()}",
                inline=True
            )
            embed.set_footer(text="Server statistics generated by bot owner • Updated in real-time")
            embed.timestamp = discord.utils.utcnow()

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"An error occurred while generating server statistics: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

    def _format_uptime(self):
        """Format bot uptime in a readable format."""
        current_time = time.time()
        uptime_seconds = current_time - self.bot.start_time

        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"

    def _get_memory_usage(self):
        """Get current memory usage of the bot process."""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            return f"{memory_mb:.1f} MB"
        except ImportError:
            return "N/A"

    @app_commands.command(name="refresh", description="Refresh slash commands (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def refresh(self, interaction: discord.Interaction):
        """Command to manually refresh slash commands."""
        try:
            await interaction.response.defer(ephemeral=True)
            synced = await self.bot.tree.sync()
            if interaction.guild is not None:
                try:
                    await self.bot.tree.sync(guild=interaction.guild)
                except Exception:
                    pass

            embed = discord.Embed(
                title="✅ Commands Refreshed",
                description=f"Successfully synced {len(synced)} slash command(s)",
                color=discord.Color.green()
            )
            all_commands = [f"`/{cmd.name}`" for cmd in self.bot.tree.get_commands()]
            embed.add_field(name="📋 Available Commands", value=", ".join(all_commands), inline=False)
            embed.set_footer(text="Commands are now available in Discord!")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            try:
                embed = discord.Embed(
                    title="❌ Refresh Failed",
                    description=f"Error refreshing commands: {str(e)}",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                try:
                    await interaction.followup.send("❌ Failed to refresh commands. Please try again later.", ephemeral=True)
                except:
                    pass

    # ===== Slash command GROUPS =====
    # RENAMED group from "help" -> "guide" to avoid clashing with /help above
    guide_group = app_commands.Group(name="guide", description="Get guides for various bot features")

    @guide_group.command(name="minigame", description="📚 Complete guide to all minigames and systems")
    async def help_minigame(self, interaction: discord.Interaction):
        """Comprehensive guide to all minigame systems."""
        embed = discord.Embed(
            title="🎮 Minigame Systems Guide",
            description="**Avatar Realms Collide** features multiple engaging minigame systems! Here's everything you need to know:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🎯 Avatar Play System (`/play`)",
            value=(
                "**Avatar trivia with multiple game modes:**\n"
                "• **⚡ Quick** - 3 questions, 8s each (1.0x XP)\n"
                "• **🎯 Standard** - 5 questions, 10s each (1.2x XP)\n"
                "• **🔥 Challenge** - 8 questions, 12s each (1.5x XP)\n"
                "• **💨 Blitz** - 10 questions, 5s each (2.0x XP)\n"
                "• **👑 Master** - 15 questions, 15s each (3.0x XP)\n\n"
                "**Difficulty Options:**\n"
                "🟢 Easy (0.8x XP) | 🟡 Normal (1.0x XP) | 🟠 Hard (1.5x XP) | 🔴 Expert (2.0x XP)"
            ),
            inline=False
        )
        embed.add_field(
            name="📅 Daily Minigame System (`/daily` & `/minigame`)",
            value=(
                "**Daily verification and rewards:**\n"
                "• Use `/daily` for daily verification and XP\n"
                "• Use `/minigame` to open game panel and roll scrolls\n"
                "• Features trivia questions with XP rewards\n"
                "• **50 XP** per correct answer\n"
                "• Chance to earn **Basic Scrolls** 📜 and **Epic Scrolls** 🟣📜\n"
                "• Must verify once before accessing features"
            ),
            inline=False
        )
        embed.add_field(
            name="🏰 Rally System (`/rally`)",
            value=(
                "**Organize Shattered Skulls Fortress raids:**\n"
                "• Create rallies: `/rally level:1-6 time_limit:5m/15m/30m/1hr`\n"
                "• **Level 1**: 1 player, 10 points\n"
                "• **Level 2**: 1 player, 20 points\n"
                "• **Level 3**: 2 players, 30 points\n"
                "• **Level 4**: 3 players, 45 points\n"
                "• **Level 5**: 4 players, 50 points\n"
                "• **Level 6**: 5 players, 60 points\n"
                "• Use `/setup #channel` (Admin only) to configure"
            ),
            inline=False
        )
        embed.add_field(
            name="⚡ XP & Progression System",
            value=(
                "**Avatar Play XP Calculation:**\n"
                "• **Base**: 75 XP per correct answer\n"
                "• **Multipliers**: Mode × Difficulty × Streak × Daily × Vote\n"
                "• **Streak Bonus**: +10% per consecutive correct answer\n"
                "• **Daily Bonus**: 2x XP for first game each day\n"
                "• **Perfect Game**: +200 bonus XP\n"
                "• **Vote Bonus**: Up to 13x XP (use `/vote`!)\n\n"
                "**Level Up Rewards:**\n"
                "• **Avatar Tokens**: 10 per level gained\n"
                "• Exponential XP requirements (15% increase per level)"
            ),
            inline=False
        )
        embed.add_field(
            name="🦸 Hero & Skill Systems",
            value=(
                "**Hero Management (`/hero`):**\n"
                "• Upgrade heroes: Rare → Epic → Legendary\n"
                "• Choose elements: Fire 🔥, Water 💧, Earth 🌱, Air 💨\n"
                "• Requires **Hero Shards** from minigames\n\n"
                "**Skill Trees (`/skills`):**\n"
                "• 44 skills across 4 elemental trees\n"
                "• Upgrade with **Skill Points** earned from playing\n"
                "• Prerequisites and tier progression system\n"
                "• Boost stats for duels and achievements"
            ),
            inline=False
        )
        embed.add_field(
            name="⚔️ PvP Duel System (`/duel`)",
            value=(
                "**Player vs Player Combat:**\n"
                "• Challenge other players: `/duel challenge @user`\n"
                "• Turn-based combat with element advantages\n"
                "• ELO rating system with tier progression\n"
                "• Track wins, losses, streaks, and statistics\n"
                "• Uses your hero upgrades and elemental skills\n"
                "• View leaderboards: `/duel leaderboard`"
            ),
            inline=False
        )
        embed.add_field(
            name="💎 Resources & Rewards",
            value=(
                "**Earned from playing minigames:**\n"
                "• **XP** - Levels up your profile and unlocks features\n"
                "• **Avatar Tokens** - Premium currency for upgrades\n"
                "• **Hero Shards** - Upgrade your hero's rarity\n"
                "• **Skill Points** - Unlock and upgrade elemental skills\n"
                "• **Scrolls** - Basic 📜 and Epic 🟣📜 rewards\n"
                "• **Achievements** - Unlock titles and bonuses\n"
                "• **Spirit Energy** - Visual status representation"
            ),
            inline=False
        )
        embed.add_field(
            name="💡 Pro Tips",
            value=(
                "🗳️ **Vote daily** with `/vote` for massive XP bonuses!\n"
                "🔥 **Maintain streaks** for +10% XP per correct answer\n"
                "👑 **Try Master mode** for 3x XP multiplier\n"
                "🎯 **Play daily** for 2x XP bonus on first game\n"
                "📊 **Check leaderboards** to see your ranking\n"
                "⚔️ **Upgrade your hero** before dueling for better stats\n"
                "🌟 **Complete achievements** for permanent rewards"
            ),
            inline=False
        )
        embed.set_footer(text="💖 Have fun playing! Use individual commands to get started with any system.")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Utility(bot))
