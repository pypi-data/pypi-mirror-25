from django.db.models import Manager, Avg
from django.db.models.query import QuerySet

from django.contrib.contenttypes.models import ContentType


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

    def get_average(self, instance):
        queryset = ActiveQuerySet(self.model, using=self._db)
        queryset = queryset.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(instance))
        avg_dict = queryset.aggregate(average=Avg('score'))
        return avg_dict['average']

    def average(self):
        queryset = ActiveQuerySet(self.model, using=self._db)
        avg_dict = queryset.aggregate(average=Avg('score'))
        return avg_dict['average']
