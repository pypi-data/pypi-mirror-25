import types
from django.test import TestCase
from .rss_parser import RSS


class RssTests(TestCase):
    rss_rules = {
        "uri": 'rss/data/afisha.xml', "rule": {
            "elements": "event",
            "items_to": {"id__attr": "event_id", "title": "title", "text": "text"}
        }}

    def test_rss_obj_generator(self):
        rp = RSS(self.rss_rules)
        rss_obj_list = rp.rss_to_object()
        self.assertIsInstance(rss_obj_list, types.GeneratorType)

    def test_rss_obj(self):
        rp = RSS(self.rss_rules)
        rss_obj_list = next(rp.rss_to_object())[0]
        obj = next(rss_obj_list)
        self.assertIsInstance(obj, dict)

