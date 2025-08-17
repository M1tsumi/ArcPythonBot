"""
Invite Manager for Avatar Realms Collide Discord Bot.
Handles permanent invite creation and storage to prevent duplicate invites.
"""

import discord
import json
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class InviteManager:
    """Manages permanent invites for servers to prevent duplicate creation."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.invites_file = self.data_dir / "permanent_invites.json"
        self.invites_data = self._load_invites()
        
    def _load_invites(self) -> Dict[str, str]:
        """Load existing permanent invites from file."""
        try:
            if self.invites_file.exists():
                with open(self.invites_file, 'r') as f:
                    return json.load(f)
            else:
                # Create directory if it doesn't exist
                self.data_dir.mkdir(parents=True, exist_ok=True)
                return {}
        except Exception as e:
            logger.error(f"Error loading invites: {e}")
            return {}
    
    def _save_invites(self):
        """Save permanent invites to file."""
        try:
            with open(self.invites_file, 'w') as f:
                json.dump(self.invites_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving invites: {e}")
    
    def get_invite(self, guild_id: str) -> Optional[str]:
        """Get existing permanent invite for a guild."""
        return self.invites_data.get(str(guild_id))
    
    def set_invite(self, guild_id: str, invite_url: str):
        """Store a permanent invite for a guild."""
        self.invites_data[str(guild_id)] = invite_url
        self._save_invites()
    
    async def get_or_create_permanent_invite(self, guild: discord.Guild) -> str:
        """
        Get existing permanent invite or create a new one for a guild.
        
        Args:
            guild: The Discord guild to get/create invite for
            
        Returns:
            str: The invite URL
        """
        guild_id = str(guild.id)
        
        # Check if we already have a stored invite
        existing_invite = self.get_invite(guild_id)
        if existing_invite:
            # Verify the invite still exists
            try:
                # Try to fetch the invite to verify it's still valid
                invite_code = existing_invite.split('/')[-1]
                await guild.fetch_invite(invite_code)
                return existing_invite
            except discord.NotFound:
                # Invite was deleted, remove from storage
                logger.info(f"Stored invite for guild {guild.name} ({guild_id}) was deleted, will create new one")
                del self.invites_data[guild_id]
                self._save_invites()
            except Exception as e:
                logger.warning(f"Error verifying invite for guild {guild.name}: {e}")
                # Continue to create new invite
        
        # Create new permanent invite
        try:
            invite_channel = None
            for channel in guild.channels:
                if (isinstance(channel, discord.TextChannel) and
                    channel.permissions_for(guild.me).create_instant_invite):
                    invite_channel = channel
                    break
            
            if invite_channel:
                invite = await invite_channel.create_invite(max_age=0, max_uses=0)
                invite_url = invite.url
                
                # Store the new invite
                self.set_invite(guild_id, invite_url)
                logger.info(f"Created new permanent invite for guild {guild.name} ({guild_id})")
                return invite_url
            else:
                logger.warning(f"No suitable channel found to create invite for guild {guild.name}")
                return "No permission to create invite"
                
        except Exception as e:
            logger.error(f"Error creating invite for guild {guild.name}: {e}")
            return "Error creating invite"
    
    async def cleanup_invalid_invites(self):
        """Clean up invalid invites from storage."""
        invalid_guilds = []
        
        for guild_id, invite_url in self.invites_data.items():
            try:
                # Try to fetch the invite to verify it's still valid
                invite_code = invite_url.split('/')[-1]
                # We can't fetch invites without guild context, so we'll just keep them
                # and let the get_or_create_permanent_invite method handle verification
                continue
            except Exception:
                invalid_guilds.append(guild_id)
        
        # Remove invalid invites
        for guild_id in invalid_guilds:
            del self.invites_data[guild_id]
            logger.info(f"Removed invalid invite for guild {guild_id}")
        
        if invalid_guilds:
            self._save_invites()
