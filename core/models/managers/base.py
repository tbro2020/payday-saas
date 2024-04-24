from django.db import models

class QuerySet(models.Manager):
    def _all(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        subdomain = kwargs.pop('subdomain', None)
        if not subdomain: return super(QuerySet, self).all(*args, **kwargs)
        return self.filter(**{'organization__subdomain_prefix': subdomain})