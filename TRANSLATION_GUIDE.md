# Translation System Guide

This guide explains how to add and manage translation keys in the Avatar Realms Collide Discord Bot.

## Overview

The bot uses a centralized translation system that supports multiple languages. Currently supported languages:
- **EN** (English) - Default language
- **ES** (Español) - Spanish

## File Structure

```
data/
├── translations.json          # Main translation file
└── users/
    └── language_preferences/  # User language preferences
```

## Adding Translation Keys

### 1. Identify the Text to Translate

When you encounter hardcoded text in a cog, you need to replace it with a translation key. For example:

```python
# Before (hardcoded)
embed = discord.Embed(title="Welcome!", description="Hello there!")

# After (translated)
embed = discord.Embed(
    title=self.get_text(user_id, "welcome_title"),
    description=self.get_text(user_id, "welcome_message")
)
```

### 2. Add Keys to translations.json

Open `data/translations.json` and add your new keys to both language sections:

```json
{
  "EN": {
    "welcome_title": "Welcome!",
    "welcome_message": "Hello there!",
    "your_new_key": "Your English text here"
  },
  "ES": {
    "welcome_title": "¡Bienvenido!",
    "welcome_message": "¡Hola!",
    "your_new_key": "Tu texto en español aquí"
  }
}
```

### 3. Use the Translation System in Cogs

In your cog, make sure you have access to the translation system:

```python
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
        self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
        return f"[Translation error: {key}]"
```

### 4. Using Translation Keys

```python
# Simple text
title = self.get_text(user_id, "welcome_title")

# Text with variables
message = self.get_text(user_id, "user_greeting", username=user.display_name)

# In embeds
embed = EmbedGenerator.create_embed(
    title=self.get_text(user_id, "command_success"),
    description=self.get_text(user_id, "operation_completed", 
                             count=5, 
                             type="items"),
    color=discord.Color.green()
)
```

## Translation Key Naming Conventions

Use descriptive, hierarchical names for your translation keys:

### Commands
- `command_name_title` - Command title
- `command_name_description` - Command description
- `command_name_success` - Success message
- `command_name_error` - Error message

### Errors
- `error_generic` - Generic error message
- `error_permission_denied` - Permission error
- `error_invalid_input` - Invalid input error
- `error_not_found` - Not found error

### UI Elements
- `button_confirm` - Confirm button text
- `button_cancel` - Cancel button text
- `field_name` - Field name
- `field_value` - Field value

### Status Messages
- `status_loading` - Loading message
- `status_success` - Success message
- `status_failed` - Failure message
- `status_pending` - Pending message

## Variable Substitution

You can use variables in your translation strings:

```json
{
  "EN": {
    "user_greeting": "Hello, {username}!",
    "item_count": "You have {count} {item_type}",
    "time_remaining": "Time remaining: {hours}h {minutes}m"
  },
  "ES": {
    "user_greeting": "¡Hola, {username}!",
    "item_count": "Tienes {count} {item_type}",
    "time_remaining": "Tiempo restante: {hours}h {minutes}m"
  }
}
```

Usage:
```python
greeting = self.get_text(user_id, "user_greeting", username="John")
count_msg = self.get_text(user_id, "item_count", count=5, item_type="items")
time_msg = self.get_text(user_id, "time_remaining", hours=2, minutes=30)
```

## Adding a New Language

To add a new language (e.g., French):

1. Add the language code to the `supported_languages` dictionary in `cogs/language_system.py`:

```python
self.supported_languages = {
    "EN": "English",
    "ES": "Español",
    "FR": "Français"  # New language
}
```

2. Add the French translations to `data/translations.json`:

```json
{
  "EN": { ... },
  "ES": { ... },
  "FR": {
    "welcome_title": "Bienvenue!",
    "welcome_message": "Bonjour!",
    // ... all other keys
  }
}
```

3. Update the available languages message:

```json
{
  "EN": {
    "available_languages": "Available languages: `EN` (English), `ES` (Español), `FR` (Français)"
  },
  "ES": {
    "available_languages": "Idiomas disponibles: `EN` (English), `ES` (Español), `FR` (Français)"
  },
  "FR": {
    "available_languages": "Langues disponibles: `EN` (English), `ES` (Español), `FR` (Français)"
  }
}
```

## Best Practices

### 1. Always Use Translation Keys
Never hardcode text in your cogs. Always use the translation system.

### 2. Use Descriptive Key Names
Make your keys self-documenting:
```python
# Good
self.get_text(user_id, "profile_image_upload_success")

# Bad
self.get_text(user_id, "msg1")
```

### 3. Keep Keys Consistent
Use the same key across different parts of the bot for the same concept:
```python
# Use the same key everywhere
self.get_text(user_id, "no_permission")  # Instead of "permission_denied", "access_denied", etc.
```

### 4. Test Both Languages
Always test your translations in both English and Spanish to ensure they make sense.

### 5. Use Variables for Dynamic Content
Don't concatenate strings. Use variables instead:
```python
# Good
self.get_text(user_id, "user_level", level=5, username="John")

# Bad
self.get_text(user_id, "user_level") + " " + str(level) + " " + username
```

## Common Translation Keys

Here are some commonly used keys you can reuse:

### General
- `no_permission` - Permission denied
- `error_occurred` - Generic error
- `success` - Success message
- `loading` - Loading message
- `not_found` - Not found message

### Commands
- `command_success` - Command completed successfully
- `command_error` - Command failed
- `command_usage` - How to use the command
- `command_cooldown` - Command on cooldown

### User Interface
- `confirm` - Confirm action
- `cancel` - Cancel action
- `yes` - Yes
- `no` - No
- `back` - Go back
- `next` - Next
- `previous` - Previous

### Time and Numbers
- `seconds` - Seconds
- `minutes` - Minutes
- `hours` - Hours
- `days` - Days
- `level` - Level
- `rank` - Rank
- `score` - Score
- `xp` - Experience points

## Troubleshooting

### Missing Translation Key
If you see `[Missing translation: key_name]`, it means the key doesn't exist in the translations file. Add it to both language sections.

### Translation Error
If you see `[Translation error: key_name]`, there's an error in the translation system. Check the logs for more details.

### Variables Not Working
Make sure all variables used in the translation string are provided when calling `get_text()`:

```python
# If translation is "Hello {name}!"
# This will work:
self.get_text(user_id, "greeting", name="John")

# This will fail:
self.get_text(user_id, "greeting")  # Missing 'name' variable
```

## Testing Translations

To test your translations:

1. Set your language to Spanish: `/language ES`
2. Test your commands
3. Switch back to English: `/language EN`
4. Test again

Make sure all text appears correctly in both languages.

## Maintenance

- Keep translation keys organized and consistent
- Remove unused keys periodically
- Update translations when adding new features
- Consider using a translation management tool for larger projects

## Example: Adding a New Command

Here's a complete example of adding a new command with translations:

### 1. Add to translations.json
```json
{
  "EN": {
    "weather_title": "🌤️ Weather Information",
    "weather_current": "Current weather in {city}: {temperature}°C, {condition}",
    "weather_error": "❌ Could not fetch weather information for {city}",
    "weather_invalid_city": "❌ Invalid city name: {city}"
  },
  "ES": {
    "weather_title": "🌤️ Información del Clima",
    "weather_current": "Clima actual en {city}: {temperature}°C, {condition}",
    "weather_error": "❌ No se pudo obtener información del clima para {city}",
    "weather_invalid_city": "❌ Nombre de ciudad inválido: {city}"
  }
}
```

### 2. Use in Cog
```python
@app_commands.command(name="weather", description="Get weather information")
@app_commands.describe(city="City name")
async def weather(self, interaction: discord.Interaction, city: str):
    await interaction.response.defer()
    
    try:
        # Get weather data (example)
        weather_data = await self.get_weather_data(city)
        
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "weather_title"),
            description=self.get_text(
                interaction.user.id, 
                "weather_current",
                city=city,
                temperature=weather_data['temp'],
                condition=weather_data['condition']
            ),
            color=discord.Color.blue()
        )
        
        await interaction.followup.send(embed=embed)
        
    except ValueError:
        embed = EmbedGenerator.create_error_embed(
            self.get_text(interaction.user.id, "weather_invalid_city", city=city)
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        embed = EmbedGenerator.create_error_embed(
            self.get_text(interaction.user.id, "weather_error", city=city)
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
```

This ensures your command works in both English and Spanish automatically!
