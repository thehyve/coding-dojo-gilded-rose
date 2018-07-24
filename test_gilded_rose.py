# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        "Check if item foo is still in items after update quality"
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].name, "foo")

    def test_no_negative_quality(self):
        "Check that item doesnt get negative quality"
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertGreaterEqual(items[0].quality, 0)

    def test_decreasing_quality(self):
        "Check that quality decreases"
        items = [Item("foo", 0, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertLess(items[0].quality, 1)

if __name__ == '__main__':
    unittest.main()
