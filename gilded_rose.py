# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    @staticmethod
    def _update_quality(item):
        """Update the item quality without exceeding boundaries."""
        factor = GildedRose.get_degrade_factor(item)
        item.quality -= factor
        if item.quality < 0:
            item.quality = 0
        if item.quality > 50 and item.name != "Sulfuras, Hand of Ragnaros":
            item.quality = 50

    @staticmethod
    def get_degrade_factor(item):
        """Return number by which the item degrades."""
        def backstage_pass_degrade_factor(item):
            if item.sell_in < 0:
                return item.quality
            elif item.sell_in < 6:
                return -3
            elif item.sell_in < 11:
                return -2
            else:
                return -1

        def aged_brie_degrade_factor(item):
            return -2 if item.sell_in < 0 else -1

        def default_item_degrade_factor(item):
            factor = 2 if item.sell_in < 0 else 1
            if "conjured" in item.name.lower():
                factor *= 2
            return factor

        item_degrade = {
            "Aged Brie": aged_brie_degrade_factor,
            "Backstage passes to a TAFKAL80ETC concert": backstage_pass_degrade_factor,
            "Sulfuras, Hand of Ragnaros": lambda __: 0
        }

        degrade_fun = item_degrade.get(item.name, default_item_degrade_factor)
        return degrade_fun(item)

    def update_items(self):
        for item in self.items:
            self._update_quality(item)
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
