# Bot Setup Guide

## Discord Application Page Setup

Unfortunately, Discord doesn't allow bots to have clickable buttons on their profile page. However, you can set up your bot's application page with proper links and information.

### Steps to Configure Bot Application Page:

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Select your bot application

2. **Configure Application Information**
   - **Name**: Avatar Realms Collide Bot
   - **Description**: Unofficial community bot for Avatar Realms Collide game
   - **Icon**: Upload a custom bot icon (recommended: 1024x1024 PNG)

3. **Add Application Links**
   - **Terms of Service URL**: (Optional - your terms if you have them)
   - **Privacy Policy URL**: (Optional - your privacy policy if you have one)
   - **Custom Authorization URL**: (Optional - for OAuth2 flows)

4. **Bot Configuration**
   - **Bot Username**: Avatar Realms Collide Bot
   - **Bot Avatar**: Same as application icon
   - **Public Bot**: Enable this to allow other servers to add your bot

5. **OAuth2 Configuration**
   - **Redirect URLs**: Add your Discord server invite link
   - **Scopes**: bot, applications.commands
   - **Bot Permissions**: 
     - Send Messages
     - Embed Links
     - Attach Files
     - Use Slash Commands
     - Read Message History

### Bot Invite Link
Your bot invite link is: `https://discord.com/oauth2/authorize?client_id=1242988284347420673&permissions=8&scope=bot%20applications.commands`

### Discord Server Link
Your Discord server link is: `https://discord.gg/a3tGyAwVRc`

## Commands Added

I've added the following new commands to your bot:

### `/help`
- Provides help information and links to your Discord server
- Lists all available commands
- Encourages users to join your Discord for support

### `/addtoserver`
- Shows an embed with bot features and information
- Includes a button that links to the bot invite URL
- Lists required permissions
- Links to your Discord server for support

### Updated `/links`
- Now uses the configured links from settings
- More comprehensive information about bot features
- Cleaner formatting

## Note About Bot Profile Buttons

Discord doesn't allow bots to have clickable buttons on their profile page. This is a platform limitation, not something that can be controlled from the bot code. The best alternatives are:

1. **Use the `/addtoserver` command** - This provides an embed with a button to add the bot
2. **Use the `/help` command** - This provides links to your Discord server
3. **Use the `/links` command** - This provides all relevant links

These commands provide the same functionality that buttons would provide, just through slash commands instead.

## Testing the Commands

After restarting your bot, you can test the new commands:

1. `/help` - Should show help information with Discord server link
2. `/addtoserver` - Should show an embed with an "Add to Server" button
3. `/links` - Should show all bot links and information

The commands will automatically sync when the bot starts up. 