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
from utils.invite_manager import InviteManager

class Utility(commands.Cog):
    """Utility command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    def get_text(self, user_id: int, key: str, **kwargs) -> str:
        """Get translated text for a user using the language system."""
        try:
            # Get the language system cog
            language_cog = self.bot.get_cog('LanguageSystem')
            if language_cog:
                return language_cog.get_text(user_id, key, **kwargs)
            else:
                # Fallback to English if language system not available
                return f"[{key}]"
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
            return f"[Translation error: {key}]"

    # ===== Prefix commands =====

    @commands.command(name="ping", description="Check bot latency and status")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping_prefix(self, ctx):
        """Traditional prefix command to check bot latency and status."""
        start_time = time.time()

        embed = EmbedGenerator.create_embed(
            title=self.get_text(ctx.author.id, "pong_title"),
            description=self.get_text(ctx.author.id, "checking_bot_status"),
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        api_latency = round(self.bot.latency * 1000, 2)

        embed = EmbedGenerator.create_embed(
            title=self.get_text(ctx.author.id, "pong_title"),
            description=self.get_text(ctx.author.id, "bot_online_responding"),
            color=discord.Color.green()
        )
        embed.add_field(name=self.get_text(ctx.author.id, "response_time"), value=f"**{latency:.1f}ms**", inline=True)
        embed.add_field(name=self.get_text(ctx.author.id, "api_latency"), value=f"**{api_latency}ms**", inline=True)
        embed.add_field(name=self.get_text(ctx.author.id, "bot_status"), value=self.get_text(ctx.author.id, "online_ready"), inline=True)
        embed.add_field(name=self.get_text(ctx.author.id, "servers"), value=f"**{len(self.bot.guilds)}** {self.get_text(ctx.author.id, 'servers_plural')}", inline=True)
        embed.add_field(name=self.get_text(ctx.author.id, "users"), value=f"**{len(self.bot.users)}** {self.get_text(ctx.author.id, 'users_plural')}", inline=True)
        embed.add_field(name=self.get_text(ctx.author.id, "commands"), value=f"**{len(self.bot.tree.get_commands())}** {self.get_text(ctx.author.id, 'slash_commands')}", inline=True)

        embed = EmbedGenerator.finalize_embed(embed)
        await message.edit(embed=embed)

    # RENAMED from "help" -> "uhelp" to avoid conflict with built-in HelpCommand
    @commands.command(name="uhelp", description="Get help and command information")
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def help_prefix(self, ctx):
        """Traditional prefix command to provide help and command information."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(ctx.author.id, "help_title"),
            description=self.get_text(ctx.author.id, "help_description"),
            color=discord.Color.blue(),
            use_cache=False  # Disable caching to prevent field duplication
        )

        embed.add_field(
            name="🎮 " + self.get_text(ctx.author.id, "game_info_commands"),
            value=f"• `!talent_trees` - {self.get_text(ctx.author.id, 'talent_trees_desc')}\n• `!skill_priorities` - {self.get_text(ctx.author.id, 'skill_priorities_desc')}\n• `!hero_info` - {self.get_text(ctx.author.id, 'hero_info_desc')}\n• `!hero_rankup` - {self.get_text(ctx.author.id, 'hero_rankup_desc')}\n• `!townhall` - {self.get_text(ctx.author.id, 'townhall_desc')}\n• `!leaderboard` - {self.get_text(ctx.author.id, 'leaderboard_desc')}",
            inline=False
        )
        embed.add_field(
            name="🎭 " + self.get_text(ctx.author.id, "event_commands"),
            value=f"• `!events` - {self.get_text(ctx.author.id, 'events_desc')}\n• `!avatar_day_festival` - {self.get_text(ctx.author.id, 'avatar_day_festival_desc')}\n• `!festival_tasks` - {self.get_text(ctx.author.id, 'festival_tasks_desc')}\n• `!festival_shop` - {self.get_text(ctx.author.id, 'festival_shop_desc')}\n• `!festival_guide` - {self.get_text(ctx.author.id, 'festival_guide_desc')}\n• `!festival_rewards` - {self.get_text(ctx.author.id, 'festival_rewards_desc')}\n• `!balance_and_order` - {self.get_text(ctx.author.id, 'balance_and_order_desc')}\n• `!balance_tasks` - {self.get_text(ctx.author.id, 'balance_tasks_desc')}\n• `!balance_guide` - {self.get_text(ctx.author.id, 'balance_guide_desc')}\n• `!borte_scheme` - {self.get_text(ctx.author.id, 'borte_scheme_desc')}\n• `!borte_mechanics` - {self.get_text(ctx.author.id, 'borte_mechanics_desc')}\n• `!borte_rewards` - {self.get_text(ctx.author.id, 'borte_rewards_desc')}\n• `!borte_guide` - {self.get_text(ctx.author.id, 'borte_guide_desc')}",
            inline=False
        )
        embed.add_field(
            name="⚔️ " + self.get_text(ctx.author.id, "rally_commands"),
            value=f"• `!setup` - {self.get_text(ctx.author.id, 'setup_desc')}\n• `!rally` - {self.get_text(ctx.author.id, 'rally_desc')}\n• `!rally_stats` - {self.get_text(ctx.author.id, 'rally_stats_desc')}\n• `!rally_leaderboard` - {self.get_text(ctx.author.id, 'rally_leaderboard_desc')}\n• `!leader` - {self.get_text(ctx.author.id, 'leader_desc')}",
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
            name="📱 " + self.get_text(ctx.author.id, "join_discord_message"),
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\n{self.get_text(ctx.author.id, 'get_help_questions')}!",
            inline=False
        )

        embed = EmbedGenerator.finalize_embed(embed)
        await ctx.send(embed=embed)

    @commands.command(name="info", description="Get comprehensive bot information and contribution details")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def info_prefix(self, ctx):
        """Traditional prefix command to provide comprehensive bot information and contribution details."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "bot_information_title"),
            description=self.get_text(interaction.user.id, "bot_information_desc"),
            color=discord.Color.blue(),
            use_cache=False  # Disable caching to prevent field duplication
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
            title=self.get_text(interaction.user.id, "bot_information_title"),
            description=self.get_text(interaction.user.id, "bot_information_desc"),
            color=discord.Color.blue(),
            use_cache=False  # Disable caching to prevent field duplication
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
            title=self.get_text(interaction.user.id, "links_title"),
            description=self.get_text(interaction.user.id, "links_description"),
            color=discord.Color.blue()
        )
        embed.add_field(name=self.get_text(interaction.user.id, "join_discord_server"), value=f"[Join Server]({DISCORD_SERVER_LINK})", inline=True)
        embed.add_field(name=self.get_text(interaction.user.id, "add_bot_to_server"), value=f"[Add to Server]({BOT_INVITE_LINK})", inline=True)
        embed.add_field(name=self.get_text(interaction.user.id, "developer"), value="**Developed by Quefep**", inline=False)
        embed.add_field(
            name=self.get_text(interaction.user.id, "bot_features"),
            value=f"• {self.get_text(interaction.user.id, 'talent_tree_browser')}\n• {self.get_text(interaction.user.id, 'skill_priorities')}\n• {self.get_text(interaction.user.id, 'leaderboards')}\n• {self.get_text(interaction.user.id, 'town_hall_info')}\n• {self.get_text(interaction.user.id, 'hero_rankup_guide')}\n• {self.get_text(interaction.user.id, 'interactive_commands')}",
            inline=False
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Comprehensive help and command guide")
    @app_commands.checks.cooldown(1, 10.0)
    async def help(self, interaction: discord.Interaction):
        """Comprehensive help command with all bot features and commands."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "help_title"),
            description=self.get_text(interaction.user.id, "help_description"),
            color=discord.Color.blue(),
            use_cache=False  # Disable caching to prevent field duplication
        )
        
        embed.add_field(
            name="📱 " + self.get_text(interaction.user.id, "join_discord_message"),
            value=f"[Click here to join our Discord!]({DISCORD_SERVER_LINK})\n{self.get_text(interaction.user.id, 'get_help_questions')}!",
            inline=False
        )
        
        embed.add_field(
            name="🎮 " + self.get_text(interaction.user.id, "game_info_commands"),
            value=f"• `/talent_trees` - {self.get_text(interaction.user.id, 'talent_trees_desc')}\n• `/skill_priorities` - {self.get_text(interaction.user.id, 'skill_priorities_desc')}\n• `/hero_info` - {self.get_text(interaction.user.id, 'hero_info_desc')}\n• `/hero_rankup` - {self.get_text(interaction.user.id, 'hero_rankup_desc')}\n• `/townhall` - {self.get_text(interaction.user.id, 'townhall_desc')}\n• `/leaderboard` - {self.get_text(interaction.user.id, 'leaderboard_desc')}\n• `/map` - {self.get_text(interaction.user.id, 'map_desc')}\n• `/troops` - {self.get_text(interaction.user.id, 'troops_desc')}\n• `/troopcalc` - {self.get_text(interaction.user.id, 'troopcalc_desc')}\n• `/tierlist` - {self.get_text(interaction.user.id, 'tierlist_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="🎭 " + self.get_text(interaction.user.id, "event_commands"),
            value=f"• `/events` - {self.get_text(interaction.user.id, 'events_desc')}\n• `/avatar_day_festival` - {self.get_text(interaction.user.id, 'avatar_day_festival_desc')}\n• `/festival_tasks` - {self.get_text(interaction.user.id, 'festival_tasks_desc')}\n• `/festival_shop` - {self.get_text(interaction.user.id, 'festival_shop_desc')}\n• `/festival_guide` - {self.get_text(interaction.user.id, 'festival_guide_desc')}\n• `/festival_rewards` - {self.get_text(interaction.user.id, 'festival_rewards_desc')}\n• `/balance_and_order` - {self.get_text(interaction.user.id, 'balance_and_order_desc')}\n• `/balance_tasks` - {self.get_text(interaction.user.id, 'balance_tasks_desc')}\n• `/balance_guide` - {self.get_text(interaction.user.id, 'balance_guide_desc')}\n• `/borte_scheme` - {self.get_text(interaction.user.id, 'borte_scheme_desc')}\n• `/borte_mechanics` - {self.get_text(interaction.user.id, 'borte_mechanics_desc')}\n• `/borte_rewards` - {self.get_text(interaction.user.id, 'borte_rewards_desc')}\n• `/borte_guide` - {self.get_text(interaction.user.id, 'borte_guide_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="🎯 " + self.get_text(interaction.user.id, "minigame_systems"),
            value=f"• `/play` - {self.get_text(interaction.user.id, 'play_desc')}\n• `/daily` - {self.get_text(interaction.user.id, 'daily_desc')}\n• `/minigame` - {self.get_text(interaction.user.id, 'minigame_desc')}\n• `/trivia` - {self.get_text(interaction.user.id, 'trivia_desc')}\n• `/trivia_leaderboard` - {self.get_text(interaction.user.id, 'trivia_leaderboard_desc')}\n• `/inventory` - {self.get_text(interaction.user.id, 'inventory_desc')}\n• `/hero` - {self.get_text(interaction.user.id, 'hero_desc')}\n• `/skills` - {self.get_text(interaction.user.id, 'skills_desc')}\n• `/duel` - {self.get_text(interaction.user.id, 'duel_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="⚔️ " + self.get_text(interaction.user.id, "rally_commands"),
            value=f"• `/setup` - {self.get_text(interaction.user.id, 'setup_desc')}\n• `/rally` - {self.get_text(interaction.user.id, 'rally_desc')}\n• `/rally_stats` - {self.get_text(interaction.user.id, 'rally_stats_desc')}\n• `/rally_leaderboard` - {self.get_text(interaction.user.id, 'rally_leaderboard_desc')}\n• `/leader` - {self.get_text(interaction.user.id, 'leader_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="🏆 " + self.get_text(interaction.user.id, "tgl_glorious_victory"),
            value=f"• `/tgl` - {self.get_text(interaction.user.id, 'tgl_desc')}\n• `/tgl_calc` - {self.get_text(interaction.user.id, 'tgl_calc_desc')}\n• `/glorious_victory` - {self.get_text(interaction.user.id, 'glorious_victory_desc')}\n• `/gv_calc` - {self.get_text(interaction.user.id, 'gv_calc_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="⏰ " + self.get_text(interaction.user.id, "timer_voting"),
            value=f"• `/timer` - {self.get_text(interaction.user.id, 'timer_desc')}\n• `/timers` - {self.get_text(interaction.user.id, 'timers_desc')}\n• `/cancel_timer` - {self.get_text(interaction.user.id, 'cancel_timer_desc')}\n• `/cancel_all_timers` - {self.get_text(interaction.user.id, 'cancel_all_timers_desc')}\n• `/vote` - {self.get_text(interaction.user.id, 'vote_desc')}\n• `/vote_status` - {self.get_text(interaction.user.id, 'vote_status_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="🔧 " + self.get_text(interaction.user.id, "utility_commands"),
            value=f"• `/ping` - {self.get_text(interaction.user.id, 'ping_desc')}\n• `/info` - {self.get_text(interaction.user.id, 'info_desc')}\n• `/links` - {self.get_text(interaction.user.id, 'links_desc')}\n• `/addtoserver` - {self.get_text(interaction.user.id, 'addtoserver_desc')}\n• `/refresh` - {self.get_text(interaction.user.id, 'refresh_desc')}\n• `/statistics` - {self.get_text(interaction.user.id, 'statistics_desc')}",
            inline=False
        )
        
        embed.add_field(
            name="💡 " + self.get_text(interaction.user.id, "pro_tips"),
            value=f"🗳️ **{self.get_text(interaction.user.id, 'vote_daily')}**\n🔥 **{self.get_text(interaction.user.id, 'maintain_streaks')}**\n👑 **{self.get_text(interaction.user.id, 'try_master_mode')}**\n🎯 **{self.get_text(interaction.user.id, 'play_daily')}**\n📊 **{self.get_text(interaction.user.id, 'check_leaderboards')}**\n⚔️ **{self.get_text(interaction.user.id, 'upgrade_hero')}**\n🌟 **{self.get_text(interaction.user.id, 'complete_achievements')}**",
            inline=False
        )
        
        embed.add_field(
            name="💡 " + self.get_text(interaction.user.id, "need_more_help"),
            value=f"{self.get_text(interaction.user.id, 'join_discord_for')}\n• {self.get_text(interaction.user.id, 'real_time_help')}\n• {self.get_text(interaction.user.id, 'game_updates')}\n• {self.get_text(interaction.user.id, 'community_discussions')}\n• {self.get_text(interaction.user.id, 'bug_reports')}\n• {self.get_text(interaction.user.id, 'contribution_opportunities')}",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="addtoserver", description="Add the bot to your server")
    @app_commands.checks.cooldown(1, 30.0)
    async def addtoserver(self, interaction: discord.Interaction):
        """Slash command to add the bot to a server with an embed and button."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "add_bot_title"),
            description=self.get_text(interaction.user.id, "add_bot_description"),
            color=discord.Color.green()
        )
        embed.add_field(
            name="🎮 " + self.get_text(interaction.user.id, "bot_features_detailed"),
            value=f"• **{self.get_text(interaction.user.id, 'talent_tree_browser')}** - View all character talent trees\n• **{self.get_text(interaction.user.id, 'skill_priorities')}** - Get optimal skill upgrade orders\n• **{self.get_text(interaction.user.id, 'leaderboards')}** - Track top players and alliances\n• **{self.get_text(interaction.user.id, 'town_hall_info')}** - View upgrade requirements\n• **{self.get_text(interaction.user.id, 'hero_rankup_guide')}** - Complete rankup costs and guide\n• **Event System** - Current and upcoming events\n• **Rally System** - Create and join Shattered Skulls Fortress rallies\n• **{self.get_text(interaction.user.id, 'interactive_commands')}** - Modern slash command interface",
            inline=False
        )
        embed.add_field(
            name="🔧 " + self.get_text(interaction.user.id, "permissions_required"),
            value=f"• {self.get_text(interaction.user.id, 'send_messages')}\n• {self.get_text(interaction.user.id, 'embed_links')}\n• {self.get_text(interaction.user.id, 'attach_files')}\n• {self.get_text(interaction.user.id, 'use_slash_commands')}\n• {self.get_text(interaction.user.id, 'read_message_history')}",
            inline=False
        )
        embed.add_field(
            name="📱 " + self.get_text(interaction.user.id, "community"),
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
                title=self.get_text(interaction.user.id, "access_denied_title"),
                description=self.get_text(interaction.user.id, "access_denied_desc"),
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
                title="🏠 " + self.get_text(interaction.user.id, "server_statistics"),
                description=self.get_text(interaction.user.id, "comprehensive_overview"),
                color=discord.Color.blue()
            )
            embed.add_field(
                name="📊 " + self.get_text(interaction.user.id, "overview"),
                value=f"**{self.get_text(interaction.user.id, 'total_servers')}**: {total_servers:,}\n"
                      f"**{self.get_text(interaction.user.id, 'total_members')}**: {total_members:,}\n"
                      f"**{self.get_text(interaction.user.id, 'average_members')}**: {avg_members:.0f}",
                inline=True
            )

            large_servers = len([g for g in self.bot.guilds if g.member_count >= 1000])
            medium_servers = len([g for g in self.bot.guilds if 100 <= g.member_count < 1000])
            small_servers = len([g for g in self.bot.guilds if g.member_count < 100])

            embed.add_field(
                name="📈 " + self.get_text(interaction.user.id, "distribution"),
                value=f"**{self.get_text(interaction.user.id, 'large_servers')}** (1k+): {large_servers}\n"
                      f"**{self.get_text(interaction.user.id, 'medium_servers')}** (100-999): {medium_servers}\n"
                      f"**{self.get_text(interaction.user.id, 'small_servers')}** (<100): {small_servers}",
                inline=True
            )

            recent_servers = [
                g for g in self.bot.guilds
                if g.me.joined_at and (discord.utils.utcnow() - g.me.joined_at).days <= 30
            ]
            embed.add_field(
                name="🆕 " + self.get_text(interaction.user.id, "recent_activity"),
                value=f"**{self.get_text(interaction.user.id, 'joined_last_30_days')}**: {len(recent_servers)}\n"
                      f"**{self.get_text(interaction.user.id, 'active_servers')}**: {len([g for g in self.bot.guilds if g.member_count > 0])}\n"
                      f"**{self.get_text(interaction.user.id, 'bot_commands')}**: {len(self.bot.tree.get_commands())}",
                inline=True
            )

            top_servers_text = ""
            for i, guild in enumerate(top_servers, 1):
                owner_name = guild.owner.display_name if guild.owner else "Unknown"
                joined_date = guild.me.joined_at.strftime('%m/%d') if guild.me.joined_at else "Unknown"

                invite_link = await self.bot.invite_manager.get_or_create_permanent_invite(guild)

                top_servers_text += f"**{i}.** {guild.name}\n"
                top_servers_text += f"👥 {guild.member_count:,} members | 👑 {owner_name} | 📅 {joined_date}\n"
                top_servers_text += f"🔗 {invite_link}\n\n"

            embed.add_field(
                name="🏆 " + self.get_text(interaction.user.id, "top_10_servers"),
                value=top_servers_text if top_servers_text else self.get_text(interaction.user.id, "no_servers_found"),
                inline=False
            )
            embed.add_field(
                name="⚡ " + self.get_text(interaction.user.id, "performance"),
                value=f"**{self.get_text(interaction.user.id, 'bot_latency')}**: {round(self.bot.latency * 1000, 1)}ms\n"
                      f"**{self.get_text(interaction.user.id, 'uptime')}**: {self._format_uptime()}\n"
                      f"**{self.get_text(interaction.user.id, 'memory_usage')}**: {self._get_memory_usage()}",
                inline=True
            )
            embed.set_footer(text=self.get_text(interaction.user.id, "server_statistics_generated"))
            embed.timestamp = discord.utils.utcnow()

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"{self.get_text(interaction.user.id, 'error_generating_statistics')}: {str(e)}",
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

    @app_commands.command(name="manage_invites", description="Manage permanent invites (Admin only)")
    @app_commands.default_permissions(administrator=True)
    async def manage_invites(self, interaction: discord.Interaction):
        """Command to manage permanent invites for the current server."""
        try:
            await interaction.response.defer(ephemeral=True)
            
            guild = interaction.guild
            if not guild:
                embed = discord.Embed(
                    title="❌ Error",
                    description="This command can only be used in a server.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Get current invite
            current_invite = await self.bot.invite_manager.get_or_create_permanent_invite(guild)
            
            embed = discord.Embed(
                title="🔗 Permanent Invite Management",
                description=f"Server: **{guild.name}**",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Current Permanent Invite",
                value=current_invite if current_invite != "No permission to create invite" else "❌ No permission",
                inline=False
            )
            
            embed.add_field(
                name="Actions",
                value="• The bot will automatically reuse existing permanent invites\n• New invites are only created when needed\n• Invalid invites are automatically cleaned up",
                inline=False
            )
            
            embed.set_footer(text="Invite management is automatic and optimized")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"Error managing invites: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

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
                title="✅ " + self.get_text(interaction.user.id, "commands_refreshed"),
                description=f"{self.get_text(interaction.user.id, 'successfully_synced')} {len(synced)} slash command(s)",
                color=discord.Color.green()
            )
            all_commands = [f"`/{cmd.name}`" for cmd in self.bot.tree.get_commands()]
            embed.add_field(name="📋 " + self.get_text(interaction.user.id, "available_commands"), value=", ".join(all_commands), inline=False)
            embed.set_footer(text=self.get_text(interaction.user.id, "commands_now_available"))
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            try:
                embed = discord.Embed(
                    title="❌ " + self.get_text(interaction.user.id, "refresh_failed"),
                    description=f"{self.get_text(interaction.user.id, 'error_refreshing_commands')}: {str(e)}",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                try:
                    await interaction.followup.send(f"❌ {self.get_text(interaction.user.id, 'failed_refresh_commands')}", ephemeral=True)
                except:
                    pass



async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Utility(bot))
