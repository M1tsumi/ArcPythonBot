import pytest
from data.translations.translation_loader import TranslationLoader


def test_fallback_to_english():
    """Requesting an unsupported language should fall back to English."""
    loader = TranslationLoader()
    # choose a key we know exists
    english_value = loader.get_translation("help_title", language="EN")
    missing_language_value = loader.get_translation("help_title", language="FR")
    assert missing_language_value == english_value
