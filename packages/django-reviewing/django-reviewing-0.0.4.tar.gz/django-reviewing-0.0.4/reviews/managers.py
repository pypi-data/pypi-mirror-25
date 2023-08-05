from django.db.models import Manager
from django.db.models.query import QuerySet


class ActiveMixin(object):
    """
    An extended manager to return active objects.
    """
    def active(self):
        return self.filter(active=True)


class ActiveQuerySet(ActiveMixin, QuerySet):
    pass


class ActiveManager(ActiveMixin, Manager):
    def get_query_set(self):
        return ActiveQuerySet(self.model, using=self._db)
