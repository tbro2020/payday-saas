import logging
import os

from django.utils.translation import gettext as _
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from core.models import Widget

logger = logging.getLogger(__name__)

def create_widgets_from_defaults():
    """Create widgets from default templates if they don't already exist."""
    defaults_path = os.path.join(settings.BASE_DIR, "core/templates/widgets/defaults")

    if not os.path.exists(defaults_path):
        logger.warning(f"Defaults directory not found: {defaults_path}")
        return

    # Iterate over each folder in the defaults directory
    for folder in os.listdir(defaults_path):
        folder_path = os.path.join(defaults_path, folder)

        if not os.path.isdir(folder_path):
            continue

        # Define the expected file paths
        view_file = os.path.join(folder_path, 'view.py')
        template_file = os.path.join(folder_path, 'template.html')

        # Skip the folder if either file is missing
        if any([not os.path.exists(view_file), not os.path.exists(template_file)]):
            logger.warning(f"Missing 'view.py' or 'template.html' in folder: {folder}")
            continue

        # Read the content of the Python and HTML files
        try:
            with open(view_file, 'r') as f:
                py_content = f.read()

            with open(template_file, 'r') as f:
                html_content = f.read()
        except IOError as e:
            logger.error(f"Error reading files in folder {folder}: {e}")
            continue

        # Extract app_label and model from the folder name
        try:
            app_label, model = folder.split('.')
        except ValueError:
            logger.error(f"Invalid folder name format: {folder}")
            continue

        # Get the ContentType for the widget
        try:
            contenttype = ContentType.objects.get(app_label=app_label, model=model)
        except ObjectDoesNotExist:
            logger.error(f"ContentType not found for app_label={app_label}, model={model}")
            continue

        # Create or update the widget
        widget, created = Widget.objects.get_or_create(
            template=html_content,
            view=py_content,
            defaults={
                'content_type': contenttype,
                'name': folder,
                'column': 'col-md-3 col-xs-12'
            }
        )

        if created:
            logger.info(f"Widget created: {widget.name}")
        else:
            logger.info(f"Widget already exists: {widget.name}")

@receiver(post_migrate)
def saved(sender, **kwargs):
    """Signal handler for post_migrate."""
    create_widgets_from_defaults()