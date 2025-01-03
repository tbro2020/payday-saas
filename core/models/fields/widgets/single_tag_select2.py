from dal import autocomplete

class SingleTagSelect2(autocomplete.TagSelect2):
    """Select2 in single-select mode with tag creation support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the base class to enforce single selection
        self.allow_multiple_selected = False

    def is_iterable(self, obj):
        """Check if an object is iterable (but not a string)."""
        from collections.abc import Iterable
        return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))

    def build_attrs(self, *args, **kwargs):
        """Automatically set data-tags=1 to allow tag creation."""
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('data-tags', 1)  # Enable tag creation
        attrs.setdefault('data-placeholder', 'Search or create a tag...')  # Add a placeholder
        attrs.setdefault('data-minimum-input-length', 1)  # Minimum characters to trigger search
        return attrs

    def value_from_datadict(self, data, files, name):
        """Return a single value instead of a comma-separated list."""
        value = super().value_from_datadict(data, files, name)
        if isinstance(value, list):
            return value[0] if value else None  # Return the first value (single selection)
        return value

    def format_value(self, value):
        """Return the list of HTML option values for a form field value."""
        if not value:
            return []

        # Handle single value (not a list or comma-separated string)
        if isinstance(value, str):
            value = [value]
        elif not self.is_iterable(value):
            value = [value]

        # Ensure unique values
        values = set()
        for v in value:
            if v:
                values.add(self.option_value(v))
        return list(values)

    def options(self, name, value, attrs=None):
        """Return only select options."""
        if not value:
            return

        # Handle single value (not a list or comma-separated string)
        if isinstance(value, str):
            value = [value]
        elif not self.is_iterable(value):
            value = [value]

        for v in value:
            if v:
                yield self.option_value(v)

    def optgroups(self, name, value, attrs=None):
        """Return a list of one optgroup and selected values."""
        default = (None, [], 0)
        groups = [default]

        for i, v in enumerate(self.options(name, value, attrs)):
            default[1].append(
                self.create_option(v, v, v, True, i)
            )
        return groups