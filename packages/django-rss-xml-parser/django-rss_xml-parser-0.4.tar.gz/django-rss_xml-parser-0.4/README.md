## Django rss/xml parser(django_rss_xml)
This parse is intended for XML / RSS, which does not conform to the standard:
https://tools.ietf.org/html/rfc5005

Use https://pypi.python.org/pypi/feedparser
for standard RSS

### install 

pip install django-rss_xml-parser


add to settings

```python
INSTALLED_APPS = [
    ...
    'django_rss_xml',
    ...
    ]
```


### usage
1) create mappers
```python
afisha = {
    "elements": "event",
    "items_to": {"id__attr": "event_id", "title": "title", "text": "text"}
}

yandex = {
    "elements": "item",
    "items_to": {"title": "title", "description": "text"}
}

kassir = {"elements": "item"}
...

```
2) create models

```python
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

```

3) add in view
```python
rss_rules = {"uri": 'rss/data/afisha.xml', "rule": afisha}
OR
rss_rules = {"uri": 'https://news.yandex.ru/auto.rss', "rule": yandex}
```
example:
```python
from django.views.generic import TemplateView
from .rss_mapper import kassir, afisha, yandex
from django_rss_xml.rss_parser import RSS
from .models import RssModel


class RSSView(TemplateView, RSS):
    template_name = "rss/rss.html"
    rss_rules = {"uri": 'rss/data/afisha.xml', "rule": afisha}

    def get_context_data(self, **kwargs):
        context = super(RSSView, self).get_context_data(**kwargs)
        context['rss_obj'] = self.rss_to_object()
        context['rss_m'] = self.rss_to_model(RssModel)
        return context
```

## Running tests

```bash
python manage.py test django_rss_xml
```

