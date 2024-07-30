from django.db import models
from functools import reduce
from operator import or_

class CustomQuerySet(models.QuerySet):
    def _all(self, subdomain=None, user=None, *args, **kwargs):
        # Check if required parameters are provided
        if not subdomain or not user:
            return self.none()

        # Get the initial queryset
        qs = super().all(*args, **kwargs)

        # If the user is a superuser, return all objects
        if user.is_superuser:
            return qs

        # Filter by subdomain
        qs = qs.filter(organization__subdomain_prefix=subdomain)

        # If the user is staff, return the filtered queryset
        if user.is_staff:
            return qs

        # Filter by user for non-staff users
        qs = qs.filter(user=user)

        # Get related fields to the User model
        related_fields = [
            field.name for field in qs.model._meta.fields
            if field.is_relation and field.related_model._meta.model_name.lower() == 'user'
        ]

        # Get nested related fields to the User model
        nested_related_fields = [
            f"{field.name}__{subfield.name}" for field in qs.model._meta.fields
            if field.is_relation for subfield in field.related_model._meta.fields
            if subfield.is_relation and subfield.related_model._meta.model_name.lower() == 'user'
        ]

        # Combine related and nested related fields
        all_related_fields = related_fields + nested_related_fields

        # Apply filters on all related fields
        filters = [models.Q(**{field: user}) for field in all_related_fields]
        filters = reduce(or_, filters)
        qs = qs.filter(**filters)

        return qs

class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset()._all(*args, **kwargs)