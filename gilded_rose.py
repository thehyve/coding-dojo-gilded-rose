# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def _decrease_quality(self, item):
        if item.quality > 0:
            item.quality -= GildedRose.get_degrade_factor(item)

    def _increase_quality(self, item):
        if item.quality < 50:
            item.quality += 1

    @staticmethod
    def get_degrade_factor(item):
        return 1

    def update_quality(self):
        for item in self.items:
            degrades_with_normal_rate = item.name not in {"Aged Brie", "Backstage passes to a TAFKAL80ETC concert",
                                                          "Sulfuras, Hand of Ragnaros"}
            if degrades_with_normal_rate:
                self._decrease_quality(item)
            else:
                self._increase_quality(item)
                if item.name == "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 11:
                        self._increase_quality(item)
                    if item.sell_in < 6:
                        self._increase_quality(item)
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    self._increase_quality(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
