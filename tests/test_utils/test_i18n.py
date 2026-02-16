"""
Test suite for i18n (internationalization) utilities
"""
import pytest
import os
import json
import tempfile
from pathlib import Path
from yamlconverter.utils.i18n import I18n


class TestI18n:
    """Test cases for internationalization functionality"""
    
    @pytest.fixture
    def temp_translations_dir(self):
        """Create a temporary translations directory"""
        temp_dir = tempfile.mkdtemp()
        
        # Create English translations
        en_translations = {
            "app_title": "YAML Excel Converter",
            "button_convert": "Convert",
            "button_browse": "Browse",
            "error_file_not_found": "File not found",
            "success_conversion": "Conversion successful"
        }
        
        # Create Italian translations
        it_translations = {
            "app_title": "Convertitore YAML Excel",
            "button_convert": "Converti",
            "button_browse": "Sfoglia",
            "error_file_not_found": "File non trovato",
            "success_conversion": "Conversione riuscita"
        }
        
        # Write translation files
        with open(os.path.join(temp_dir, 'en.json'), 'w', encoding='utf-8') as f:
            json.dump(en_translations, f, ensure_ascii=False, indent=2)
        
        with open(os.path.join(temp_dir, 'it.json'), 'w', encoding='utf-8') as f:
            json.dump(it_translations, f, ensure_ascii=False, indent=2)
        
        yield temp_dir
        
        # Cleanup
        for file in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
    
    def test_i18n_initialization_default_language(self, temp_translations_dir):
        """Test I18n initialization with default language"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        # Should use specified or default language
        assert i18n.current_language in ['en', 'it']
    
    def test_i18n_get_translation_english(self, temp_translations_dir):
        """Test getting translations in English"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        assert i18n.get('app_title') == 'YAML Excel Converter'
        assert i18n.get('button_convert') == 'Convert'
        assert i18n.get('button_browse') == 'Browse'
    
    def test_i18n_get_translation_italian(self, temp_translations_dir):
        """Test getting translations in Italian"""
        i18n = I18n(translations_dir=temp_translations_dir, language='it')
        
        assert i18n.get('app_title') == 'Convertitore YAML Excel'
        assert i18n.get('button_convert') == 'Converti'
        assert i18n.get('button_browse') == 'Sfoglia'
    
    def test_i18n_switch_language(self, temp_translations_dir):
        """Test switching languages"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        # Start with English
        assert i18n.get('button_convert') == 'Convert'
        
        # Switch to Italian
        i18n.set_language('it')
        assert i18n.get('button_convert') == 'Converti'
        
        # Switch back to English
        i18n.set_language('en')
        assert i18n.get('button_convert') == 'Convert'
    
    def test_i18n_missing_key_returns_key(self, temp_translations_dir):
        """Test that missing translation keys return the key itself"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        missing_key = 'nonexistent_translation_key'
        result = i18n.get(missing_key)
        
        # Should return the key or a placeholder
        assert missing_key in result or result == missing_key
    
    def test_i18n_get_available_languages(self, temp_translations_dir):
        """Test getting list of available languages"""
        i18n = I18n(translations_dir=temp_translations_dir)
        
        languages = i18n.get_available_languages()
        
        assert 'en' in languages
        assert 'it' in languages
        assert len(languages) >= 2
    
    def test_i18n_invalid_language_fallback(self, temp_translations_dir):
        """Test fallback when invalid language is set"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        # Try to set invalid language
        i18n.set_language('invalid_lang')
        
        # Should still return valid translations (fallback to default)
        result = i18n.get('app_title')
        assert result is not None
        assert len(result) > 0
    
    def test_i18n_empty_key(self, temp_translations_dir):
        """Test getting translation with empty key"""
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        result = i18n.get('')
        
        # Should handle gracefully
        assert result == '' or result is not None
    
    def test_i18n_special_characters_in_translations(self, temp_translations_dir):
        """Test translations with special characters"""
        # Add translation with special characters
        with open(os.path.join(temp_translations_dir, 'en.json'), 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        translations['special_chars'] = 'Special: ä, ö, ü, é, ñ, 中文'
        
        with open(os.path.join(temp_translations_dir, 'en.json'), 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        
        i18n = I18n(translations_dir=temp_translations_dir, language='en')
        
        result = i18n.get('special_chars')
        assert 'ä' in result
        assert '中文' in result


class TestI18nEdgeCases:
    """Test edge cases and error scenarios"""
    
    def test_i18n_nonexistent_translations_dir(self):
        """Test initialization with nonexistent translations directory"""
        # This should use fallback translations instead of raising exception
        i18n = I18n(translations_dir='/nonexistent/path/to/translations', language='en')
        # Should have fallback translations
        assert i18n.get('app_title') is not None
    
    def test_i18n_empty_translations_dir(self):
        """Test initialization with empty translations directory"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Should use fallback translations
            i18n = I18n(translations_dir=temp_dir, language='en')
            assert i18n.get('app_title') is not None
        finally:
            os.rmdir(temp_dir)
    
    def test_i18n_malformed_json(self):
        """Test handling of malformed translation JSON"""
        temp_dir = tempfile.mkdtemp()
        
        # Create malformed JSON
        with open(os.path.join(temp_dir, 'en.json'), 'w') as f:
            f.write('{invalid json: syntax}')
        
        try:
            # Should fail or use fallback
            try:
                i18n = I18n(translations_dir=temp_dir, language='en')
                # If it doesn't raise, should have some translations
                assert i18n.get('app_title') is not None
            except json.JSONDecodeError:
                pass  # This is acceptable
        finally:
            os.unlink(os.path.join(temp_dir, 'en.json'))
            os.rmdir(temp_dir)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
