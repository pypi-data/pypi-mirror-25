from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import now


class Tags(models.Model):
    tag = models.CharField(max_length=50, verbose_name=_("Tag"))


class RssModel(models.Model):
    event_id = models.IntegerField(verbose_name=_("event ID"), null=True)
    title = models.CharField(max_length=550, verbose_name=_("Title"), null=True)
    text = models.TextField(verbose_name=_("Description"), null=True)
    time = models.DateTimeField(verbose_name=_("Time and Date"), default=now, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name=_('Tags'), null=True, blank=True)
