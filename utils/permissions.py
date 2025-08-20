import discord


def is_owner(interaction: discord.Interaction) -> bool:
    """Check whether the interaction user is the bot owner."""
    return interaction.user.id == 1051142172130422884
