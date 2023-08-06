from django.views.generic import TemplateView
from .rss_mapper import kassir, afisha, yandex
from .rss_parser import RSS
from .models import RssModel


class RSSView(TemplateView, RSS):
    template_name = "rss/rss.html"
    rss_rules = {"uri": 'rss/data/afisha.xml', "rule": afisha}
    # rss_rules = {"uri": 'https://news.yandex.ru/auto.rss', "rule": yandex}

    def get_context_data(self, **kwargs):
        context = super(RSSView, self).get_context_data(**kwargs)
        context['rss_obj'] = self.rss_to_object()
        context['rss_m'] = self.rss_to_model(RssModel)
        return context
