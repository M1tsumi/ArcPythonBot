"""
Language System command module for Avatar Realms Collide Discord Bot.
Handles user language preferences and translations.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Dict, Any
import json
from pathlib import Path
from datetime import datetime, timezone

from utils.global_profile_manager import global_profile_manager
from utils.embed_generator import EmbedGenerator

class LanguageSystem(commands.Cog):
    """Language management system for user preferences."""
    
    def __init__(self, bot):
        self.bot = bot
        # Handle case where bot doesn't have a logger
        self.logger = getattr(bot, 'logger', None)
        self.supported_languages = {
            "EN": "English",
            "DE": "Deutsch",
            "ES": "Español"
        }
        
        # Load translations
        self.translations = self._load_translations()
        
        # Ensure language data directory exists
        language_dir = Path("data/users/language_preferences")
        try:
            language_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating language directory: {e}")
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load all translations from the translations file."""
        translations_file = Path("data/translations.json")
        
        # Default translations if file doesn't exist
        default_translations = {
            "EN": {
                # Language command
                "language_set_success": "✅ Language set to **English** successfully!",
                "language_set_error": "❌ Error setting language. Please try again.",
                "invalid_language": "❌ Invalid language code. Please use `EN` for English, `DE` for German, or `ES` for Spanish.",
                "current_language": "🌐 Your current language is set to: **{language}**",
                "available_languages": "Available languages: `EN` (English), `DE` (Deutsch), `ES` (Español)",
                
                # Profile system
                "profile_image_submitted": "📸 Profile Image Submitted",
                "profile_image_submitted_desc": "Your profile image has been submitted for approval!",
                "what_happens_next": "What happens next?",
                "what_happens_next_desc": "• The bot owner will review your image\n• You'll receive a DM when it's approved or rejected\n• Once approved, your image will appear on your profile",
                "note": "Note",
                "note_desc": "Please ensure your image shows a valid Avatar Realms account screenshot.",
                "invalid_file_type": "❌ Invalid file type! Please upload an image file (PNG, JPG, etc.).",
                "file_too_large": "❌ Image file too large! Please upload an image smaller than 10MB.",
                "download_failed": "❌ Failed to download image. Please try again.",
                "save_failed": "❌ Failed to save image. Please try again.",
                "processing_error": "❌ An error occurred while processing your image. Please try again.",
                
                # Approval system
                "approval_request_title": "🔍 Profile Image Approval Request",
                "approval_request_desc": "**User:** {user_mention} (`{user_id}`)\n**Server:** {guild_name}\n**Submitted:** {submitted_time}",
                "profile_approved_title": "✅ Profile Image Approved!",
                "profile_approved_desc": "Your profile image has been approved and is now active!",
                "next_steps": "Next Steps",
                "next_steps_desc": "Use `/profile` to view your profile with the new image.",
                "profile_rejected_title": "❌ Profile Image Rejected",
                "profile_rejected_desc": "Your profile image was not approved.\n\n**Reason:** {reason}",
                "what_to_do": "What to do",
                "what_to_do_desc": "Please submit a new image using `/setprofile` with a valid Avatar Realms account screenshot.",
                
                # Profile display
                "global_profile_title": "🌟 Global Profile - {display_name}",
                "global_profile_desc": "Cross-server Avatar Trivia statistics",
                "global_statistics": "📊 Global Statistics",
                "performance": "🎯 Performance",
                "global_ranking": "🏆 Global Ranking",
                "global_achievements": "🏅 Global Achievements",
                "account_info": "📅 Account Info",
                "server_profile_title": "🏠 Server Profile",
                "server_profile_desc": "Server-specific profiles are coming soon! Use `/profile global` to see cross-server stats.",
                "profile_private": "This user has chosen to keep their global profile private.",
                "profile_error": "❌ An error occurred while loading the profile. Please try again.",
                "profile_display_error": "❌ Failed to display profile. Please try again.",
                
                # Owner commands
                "no_permission": "You don't have permission to use this command.",
                "pending_approvals_title": "📋 Pending Approvals",
                "no_pending_approvals": "No pending profile image approvals.",
                "pending_approvals_desc": "**Total Pending:** {count}",
                "profile_image_info_title": "📸 Profile Image Info - {display_name}",
                "profile_image_found": "✅ Profile Image Found",
                "file_missing": "❌ File Missing",
                "no_profile_image": "❌ No Profile Image",
                "pending_approval_status": "⏳ Pending Approval",
                "profile_image_ok": "✅ Profile Image OK",
                "profile_image_fixed": "🔧 Profile Image Fixed",
                "what_was_fixed": "What was fixed",
                "no_pending_to_clear": "✅ No Pending Approvals",
                "no_pending_desc": "There are no pending approvals to clear.",
                "pending_cleared": "🧹 Pending Approvals Cleared",
                "pending_cleared_desc": "Cleared {total} pending approvals and {files} temporary files.",
                
                # Timeout messages
                "approval_expired_title": "⏰ Profile Image Approval Expired",
                "approval_expired_desc": "Your profile image approval request has expired (24 hours).",
                "what_happened": "What happened?",
                "what_happened_desc": "• Your approval request was not reviewed within 24 hours\n• The temporary file has been cleaned up\n• You can submit a new image using `/setprofile`",
                
                # Error messages
                "error_occurred": "❌ An error occurred. Please try again.",
                "already_processed": "This approval request has already been processed or has expired.",
                "error_approving": "Error approving profile image: {error}",
                "error_rejecting": "Error rejecting profile image: {error}",
                "error_getting_info": "Error getting profile image info: {error}",
                "error_fixing": "Error fixing profile image: {error}",
                "error_clearing": "Error clearing pending approvals: {error}",
                "error_notifying": "Error notifying user of approval result: {error}",
                "error_timeout": "Error notifying user of approval timeout: {error}",
                "error_handling_timeout": "Error handling approval timeout: {error}",
                
                # File operations
                "file_exists": "✅ Exists",
                "file_missing_status": "❌ Missing",
                "file_size_mb": "{size:.2f} MB",
                "file_size_bytes": "{size:,} bytes",
                "status_active": "Active",
                "status_file_not_found": "File not found on disk",
                "status_no_image": "User has no profile image set",
                "status_working": "Profile image for {user} is working correctly.",
                "status_broken": "Removed broken profile image reference for {user}.",
                "status_fixed_desc": "• Removed reference to missing image file\n• User can now submit a new profile image\n• Profile will use Discord avatar as fallback",
                
                # Statistics labels
                "level": "Level",
                "total_xp": "Total XP",
                "games_played": "Games Played",
                "accuracy": "Accuracy",
                "correct_answers": "Correct Answers",
                "best_streak": "Best Streak",
                "perfect_games": "Perfect Games",
                "servers_played": "Servers Played",
                "rank": "Rank",
                "category": "Category",
                "created": "Created",
                "last_active": "Last Active",
                "unknown": "Unknown",
                
                # Achievement names
                "global_novice": "🎓 Global Novice",
                "global_apprentice": "📚 Global Apprentice",
                "global_expert": "🔥 Global Expert",
                "global_master": "⭐ Global Master",
                "global_grandmaster": "👑 Global Grandmaster",
                "streak_champion": "🏆 Streak Champion",
                "streak_legend": "🌟 Streak Legend",
                "perfect_master": "💎 Perfect Master",
                "perfect_legend": "✨ Perfect Legend",
                "server_explorer": "🗺️ Server Explorer",
                "server_nomad": "🚀 Server Nomad",
                "dedicated_player": "❤️ Dedicated Player",
                "addicted_player": "🎮 Addicted Player",
                "trivia_god": "🔱 Trivia God"
            },
            "ES": {
                # Language command
                "language_set_success": "✅ ¡Idioma configurado a **Español** exitosamente!",
                "language_set_error": "❌ Error al configurar el idioma. Por favor, inténtalo de nuevo.",
                "invalid_language": "❌ Código de idioma inválido. Por favor usa `EN` para Inglés o `ES` para Español.",
                "current_language": "🌐 Tu idioma actual está configurado en: **{language}**",
                "available_languages": "Idiomas disponibles: `EN` (Inglés), `ES` (Español)",
                
                # Profile system
                "profile_image_submitted": "📸 Imagen de Perfil Enviada",
                "profile_image_submitted_desc": "¡Tu imagen de perfil ha sido enviada para aprobación!",
                "what_happens_next": "¿Qué pasa después?",
                "what_happens_next_desc": "• El propietario del bot revisará tu imagen\n• Recibirás un DM cuando sea aprobada o rechazada\n• Una vez aprobada, tu imagen aparecerá en tu perfil",
                "note": "Nota",
                "note_desc": "Por favor asegúrate de que tu imagen muestre una captura de pantalla válida de tu cuenta de Avatar Realms.",
                "invalid_file_type": "❌ ¡Tipo de archivo inválido! Por favor sube un archivo de imagen (PNG, JPG, etc.).",
                "file_too_large": "❌ ¡Archivo de imagen demasiado grande! Por favor sube una imagen menor a 10MB.",
                "download_failed": "❌ Error al descargar la imagen. Por favor inténtalo de nuevo.",
                "save_failed": "❌ Error al guardar la imagen. Por favor inténtalo de nuevo.",
                "processing_error": "❌ Ocurrió un error al procesar tu imagen. Por favor inténtalo de nuevo.",
                
                # Approval system
                "approval_request_title": "🔍 Solicitud de Aprobación de Imagen de Perfil",
                "approval_request_desc": "**Usuario:** {user_mention} (`{user_id}`)\n**Servidor:** {guild_name}\n**Enviado:** {submitted_time}",
                "profile_approved_title": "✅ ¡Imagen de Perfil Aprobada!",
                "profile_approved_desc": "¡Tu imagen de perfil ha sido aprobada y ahora está activa!",
                "next_steps": "Próximos Pasos",
                "next_steps_desc": "Usa `/profile` para ver tu perfil con la nueva imagen.",
                "profile_rejected_title": "❌ Imagen de Perfil Rechazada",
                "profile_rejected_desc": "Tu imagen de perfil no fue aprobada.\n\n**Razón:** {reason}",
                "what_to_do": "Qué hacer",
                "what_to_do_desc": "Por favor envía una nueva imagen usando `/setprofile` con una captura de pantalla válida de tu cuenta de Avatar Realms.",
                
                # Profile display
                "global_profile_title": "🌟 Perfil Global - {display_name}",
                "global_profile_desc": "Estadísticas de Trivia de Avatar entre servidores",
                "global_statistics": "📊 Estadísticas Globales",
                "performance": "🎯 Rendimiento",
                "global_ranking": "🏆 Ranking Global",
                "global_achievements": "🏅 Logros Globales",
                "account_info": "📅 Información de Cuenta",
                "server_profile_title": "🏠 Perfil del Servidor",
                "server_profile_desc": "¡Los perfiles específicos del servidor llegarán pronto! Usa `/profile global` para ver estadísticas entre servidores.",
                "profile_private": "Este usuario ha elegido mantener su perfil global privado.",
                "profile_error": "❌ Ocurrió un error al cargar el perfil. Por favor inténtalo de nuevo.",
                "profile_display_error": "❌ Error al mostrar el perfil. Por favor inténtalo de nuevo.",
                
                # Owner commands
                "no_permission": "No tienes permiso para usar este comando.",
                "pending_approvals_title": "📋 Aprobaciones Pendientes",
                "no_pending_approvals": "No hay aprobaciones de imágenes de perfil pendientes.",
                "pending_approvals_desc": "**Total Pendiente:** {count}",
                "profile_image_info_title": "📸 Información de Imagen de Perfil - {display_name}",
                "profile_image_found": "✅ Imagen de Perfil Encontrada",
                "file_missing": "❌ Archivo Faltante",
                "no_profile_image": "❌ Sin Imagen de Perfil",
                "pending_approval_status": "⏳ Aprobación Pendiente",
                "profile_image_ok": "✅ Imagen de Perfil OK",
                "profile_image_fixed": "🔧 Imagen de Perfil Reparada",
                "what_was_fixed": "Qué se reparó",
                "no_pending_to_clear": "✅ Sin Aprobaciones Pendientes",
                "no_pending_desc": "No hay aprobaciones pendientes para limpiar.",
                "pending_cleared": "🧹 Aprobaciones Pendientes Limpiadas",
                "pending_cleared_desc": "Limpiadas {total} aprobaciones pendientes y {files} archivos temporales.",
                
                # Timeout messages
                "approval_expired_title": "⏰ Aprobación de Imagen de Perfil Expirada",
                "approval_expired_desc": "Tu solicitud de aprobación de imagen de perfil ha expirado (24 horas).",
                "what_happened": "¿Qué pasó?",
                "what_happened_desc": "• Tu solicitud de aprobación no fue revisada dentro de 24 horas\n• El archivo temporal ha sido limpiado\n• Puedes enviar una nueva imagen usando `/setprofile`",
                
                # Error messages
                "error_occurred": "❌ Ocurrió un error. Por favor inténtalo de nuevo.",
                "already_processed": "Esta solicitud de aprobación ya ha sido procesada o ha expirado.",
                "error_approving": "Error al aprobar imagen de perfil: {error}",
                "error_rejecting": "Error al rechazar imagen de perfil: {error}",
                "error_getting_info": "Error al obtener información de imagen de perfil: {error}",
                "error_fixing": "Error al reparar imagen de perfil: {error}",
                "error_clearing": "Error al limpiar aprobaciones pendientes: {error}",
                "error_notifying": "Error al notificar al usuario del resultado de aprobación: {error}",
                "error_timeout": "Error al notificar al usuario del tiempo de espera: {error}",
                "error_handling_timeout": "Error al manejar el tiempo de espera: {error}",
                
                # File operations
                "file_exists": "✅ Existe",
                "file_missing_status": "❌ Faltante",
                "file_size_mb": "{size:.2f} MB",
                "file_size_bytes": "{size:,} bytes",
                "status_active": "Activo",
                "status_file_not_found": "Archivo no encontrado en disco",
                "status_no_image": "El usuario no tiene imagen de perfil configurada",
                "status_working": "La imagen de perfil para {user} está funcionando correctamente.",
                "status_broken": "Referencia de imagen de perfil rota eliminada para {user}.",
                "status_fixed_desc": "• Referencia a archivo de imagen faltante eliminada\n• El usuario puede enviar una nueva imagen de perfil\n• El perfil usará el avatar de Discord como respaldo",
                
                # Statistics labels
                "level": "Nivel",
                "total_xp": "XP Total",
                "games_played": "Juegos Jugados",
                "accuracy": "Precisión",
                "correct_answers": "Respuestas Correctas",
                "best_streak": "Mejor Racha",
                "perfect_games": "Juegos Perfectos",
                "servers_played": "Servidores Jugados",
                "rank": "Rango",
                "category": "Categoría",
                "created": "Creado",
                "last_active": "Última Actividad",
                "unknown": "Desconocido",
                
                # Achievement names
                "global_novice": "🎓 Novato Global",
                "global_apprentice": "📚 Aprendiz Global",
                "global_expert": "🔥 Experto Global",
                "global_master": "⭐ Maestro Global",
                "global_grandmaster": "👑 Gran Maestro Global",
                "streak_champion": "🏆 Campeón de Racha",
                "streak_legend": "🌟 Leyenda de Racha",
                "perfect_master": "💎 Maestro Perfecto",
                "perfect_legend": "✨ Leyenda Perfecta",
                "server_explorer": "🗺️ Explorador de Servidores",
                "server_nomad": "🚀 Nómada de Servidores",
                "dedicated_player": "❤️ Jugador Dedicado",
                "addicted_player": "🎮 Jugador Adicto",
                "trivia_god": "🔱 Dios de la Trivia"
            }
        }
        
        try:
            if translations_file.exists():
                with open(translations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create the translations file with default translations
                with open(translations_file, 'w', encoding='utf-8') as f:
                    json.dump(default_translations, f, indent=2, ensure_ascii=False)
                return default_translations
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error loading translations: {e}")
            return default_translations
    
    def get_user_language(self, user_id: int) -> str:
        """Get the user's preferred language."""
        try:
            profile = global_profile_manager.load_global_profile(user_id)
            preferences = profile.get("preferences", {})
            return preferences.get("language", "EN")  # Default to English
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting user language for {user_id}: {e}")
            return "EN"
    
    def set_user_language(self, user_id: int, language: str) -> bool:
        """Set the user's preferred language."""
        try:
            profile = global_profile_manager.load_global_profile(user_id)
            if "preferences" not in profile:
                profile["preferences"] = {}
            
            profile["preferences"]["language"] = language
            global_profile_manager.save_global_profile(user_id, profile)
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting user language for {user_id}: {e}")
            return False
    
    def get_text(self, user_id: int, key: str, **kwargs) -> str:
        """Get translated text for a user."""
        try:
            language = self.get_user_language(user_id)
            if language not in self.translations:
                language = "EN"  # Fallback to English
            
            if key not in self.translations[language]:
                # Fallback to English if translation not found
                if key in self.translations["EN"]:
                    text = self.translations["EN"][key]
                else:
                    return f"[Missing translation: {key}]"
            else:
                text = self.translations[language][key]
            
            # Format the text with any provided kwargs
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
            return f"[Translation error: {key}]"
    
    @app_commands.command(name="language", description="Set your preferred language for bot responses")
    @app_commands.describe(
        language_code="Language code (EN for English, ES for Spanish)"
    )
    async def set_language(
        self, 
        interaction: discord.Interaction, 
        language_code: str
    ):
        """Set user's preferred language."""
        await interaction.response.defer(ephemeral=True)
        
        # Validate language code
        language_code = language_code.upper()
        if language_code not in self.supported_languages:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "invalid_language")
            )
            embed.add_field(
                name="Available Languages",
                value=self.get_text(interaction.user.id, "available_languages"),
                inline=False
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Set the language
        success = self.set_user_language(interaction.user.id, language_code)
        
        if success:
            language_name = self.supported_languages[language_code]
            embed = EmbedGenerator.create_embed(
                title="🌐 Language Updated",
                description=self.get_text(interaction.user.id, "language_set_success"),
                color=discord.Color.green()
            )
            embed.add_field(
                name="Current Language",
                value=f"**{language_name}** ({language_code})",
                inline=False
            )
        else:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "language_set_error")
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="currentlanguage", description="Check your current language setting")
    async def current_language(self, interaction: discord.Interaction):
        """Check user's current language setting."""
        await interaction.response.defer(ephemeral=True)
        
        language_code = self.get_user_language(interaction.user.id)
        language_name = self.supported_languages.get(language_code, "Unknown")
        
        embed = EmbedGenerator.create_embed(
            title="🌐 Language Settings",
            description=self.get_text(interaction.user.id, "current_language", language=language_name),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Available Languages",
            value=self.get_text(interaction.user.id, "available_languages"),
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @commands.command(name="language", help="Set your preferred language for bot responses")
    async def language_command(self, ctx, language_code: str = None):
        """Regular command version of language setting."""
        if language_code is None:
            # Show current language
            language_code = self.get_user_language(ctx.author.id)
            language_name = self.supported_languages.get(language_code, "Unknown")
            
            embed = EmbedGenerator.create_embed(
                title="🌐 Language Settings",
                description=self.get_text(ctx.author.id, "current_language", language=language_name),
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Available Languages",
                value=self.get_text(ctx.author.id, "available_languages"),
                inline=False
            )
            embed.add_field(
                name="Usage",
                value="`!language <code>` or `/language <code>`\nExample: `!language EN`",
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        # Validate language code
        language_code = language_code.upper()
        if language_code not in self.supported_languages:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(ctx.author.id, "invalid_language")
            )
            embed.add_field(
                name="Available Languages",
                value=self.get_text(ctx.author.id, "available_languages"),
                inline=False
            )
            await ctx.send(embed=embed)
            return
        
        # Set the language
        success = self.set_user_language(ctx.author.id, language_code)
        
        if success:
            language_name = self.supported_languages[language_code]
            embed = EmbedGenerator.create_embed(
                title="🌐 Language Updated",
                description=self.get_text(ctx.author.id, "language_set_success"),
                color=discord.Color.green()
            )
            embed.add_field(
                name="Current Language",
                value=f"**{language_name}** ({language_code})",
                inline=False
            )
        else:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(ctx.author.id, "language_set_error")
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(LanguageSystem(bot))
