from django.utils.translation import gettext as _
from django.core.cache import cache
from django.apps import AppConfig



class CoreConfig(AppConfig):
    """Configuration class for the 'core' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Method called when the app is ready."""
        import core.signals  # Import signals to ensure they are registered
        self.sync_preferences()


    def sync_preferences(self):
        """Sync application preferences with the cache."""
        PREFERENCES = [
            ('AUTO_SAVE_FORM:BOOL', _('Sauvegarde automatique du formulaire').upper()),
            ('DEFAULT_USER_PASSWORD:STR', _('Mot de passe par défaut').upper()),
            ('DEFAULT_USER_ROLE:STR', _('Groupe par défaut').upper()),
        ]

        # Retrieve existing preferences from the cache
        preferences = cache.get('PREFERENCES', [])

        # Add new preferences if they don't already exist
        for key, label in PREFERENCES:
            if not any(existing_key == key for existing_key, _ in preferences):
                preferences.append((key, label))

        # Update the cache with the new preferences
        cache.set('PREFERENCES', preferences)