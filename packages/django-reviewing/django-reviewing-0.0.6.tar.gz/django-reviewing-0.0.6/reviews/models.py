from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import ActiveManager
from .settings import SCORE_CHOICES


@python_2_unicode_compatible
class Review(models.Model):
    """
    A ``Review`` consists on a comment and a rating.
    """
    content_type = models.ForeignKey(ContentType, verbose_name=_(u"Content type"), related_name="content_type_set_for_%(class)s")
    object_id = models.PositiveIntegerField(_(u"Content ID"), blank=True, null=True)
    content = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    active = models.BooleanField(_(u"Active"), default=False)
    # if the user is authenticated we save the user otherwise the name and the
    # email.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"User"), blank=True, null=True, related_name="%(class)s_comments")
    user_name = models.CharField(_(u"Name"), max_length=50, blank=True)
    user_email = models.EmailField(_(u"E-mail"), blank=True)

    comment = models.TextField(_(u"Comment"), blank=True)
    score = models.PositiveIntegerField(_(u"Score"), choices=SCORE_CHOICES)

    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_(u"IP address"), blank=True, null=True)

    objects = ActiveManager()

    def __str__(self):
        return "{} ({})".format(self.name, self.score)

    @property
    def name(self):
        """
        Returns the stored user name.
        """
        if self.user is not None:
            return self.user.get_full_name()
        else:
            return self.user_name

    @property
    def email(self):
        """
        Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        else:
            return self.user_email
