"""
This parse is intended for XML / RSS, which does not conform to the standard:rfc5005
https://tools.ietf.org/html/rfc5005
"""

from urllib.request import urlopen
import xml.etree.cElementTree as etree


class RSS(object):
    rule = None
    rss_rules = None

    def __init__(self, rss_rules=None):
        if rss_rules:
            self.rss_rules = rss_rules

    def rss_to_model(self, model=None):
        """
        save to xml/rss to model by map.
        :param model:
        :return: None
        """
        self.rule = self.rss_rules.get('rule')
        items = self.get_elements()
        model_list = []
        for item in items:
            model_list.append(self.item_to_model(item, model))

        model.objects.bulk_create(model_list)

    def rss_to_object(self):
        """
        :return: list
        """
        self.rule = self.rss_rules.get('rule')
        items = self.get_elements()
        lst = []
        for item in items:
            lst.append(self.item_to_obj(item))

        yield lst

    def item_to_model(self, item, model):
        items_to = self.rule.get("items_to")
        m = model()
        for it_to, val in items_to.items():
            try:
                if it_to.endswith("__attr"):
                    id, attr = it_to.split("__")
                    v = item.get(id)
                    setattr(m, val, v)
                else:
                    v = item.find(it_to).text
                    setattr(m, val, v)
            except Exception as e:
                pass
        return m

    def item_to_obj(self, item):
        obj = {}
        items_to = self.rule.get("items_to")
        for it_to, val in items_to.items():
            if it_to.endswith("__attr"):
                id, attr = it_to.split("__")
                obj[val] = item.get(id)
            else:
                obj[val] = item.find(it_to).text
        yield obj

    def get_elements(self):
        """
        get and parse xml/
        :return:  elements list
        """
        uri = self.rss_rules.get('uri')
        if uri.startswith('http'):
            uri = urlopen(uri)

        tree = etree.parse(uri, etree.XMLParser(encoding='utf-8'))
        root = tree.getroot()
        element = ".//{0}".format(self.rule.get('elements'))
        items = root.findall(element)
        return items
