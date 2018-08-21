# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class UpdateQualityTestCase(unittest.TestCase):
    "Tests for GildedRose().update_quality()"

    def test_foo(self):
        "Check if item foo is still in items after update quality"
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(items[0].name, "foo")

    def test_decreasing_sell_in(self):
        "Check that sell in decreases"
        items = [Item("foo", 1, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertLess(items[0].sell_in, 1)

    def test_decreasing_quality(self):
        "Check that quality decreases"
        items = [Item("foo", 0, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertLess(items[0].quality, 1)

    def test_decreasing_quality_when_sellby_date_passed(self):
        "Check that quality decreases faster after the sell-by date"
        items = [Item("foo", sell_in=-1, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEquals(items[0].quality, 8)

    def test_no_negative_quality(self):
        "Check that item doesnt get negative quality"
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertGreaterEqual(items[0].quality, 0)

    def test_sell_in_is_negative(self):
        "Check that sell in negative"
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertLess(items[0].sell_in, 0)

    def test_quality_never_more_than_50(self):
        "Quality stays 50"
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 30, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(items[0].quality, 50)

    def test_quality_increase_by_2(self):
        "Quality += 2"
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(items[0].quality, 42)

    def test_quality_increase_by_3(self):
        "Quality += 3"
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 39)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(items[0].quality, 42)

    def test_backstage_pass_past_concert(self):
        "Check if a backstage pass has 0 quality after the concert."
        items = [Item(
            "Backstage passes to a TAFKAL80ETC concert",
            sell_in=-1,
            quality=3)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertEqual(items[0].quality, 0)

    @unittest.skip('do later')
    def test_conjured_option_exist(self):
        """Check if a conjured item can be added"""
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_items()
        self.assertLess(items[0].sell_in, 0)


class DegradeFactorTestcase(unittest.TestCase):
    def test_normal_item_degrade_factor_before_sellby(self):
        "Degrade factor should be 1 before sell by date passes"
        item = Item("foo", 1, 0)
        factor = GildedRose.get_degrade_factor(item)
        self.assertEqual(factor, 1)

    def test_exception_item_degrade_factor(self):
        "Degrade factor should be negative before sell by date passes"
        item = Item("foo", 1, 0)
        factor = GildedRose.get_degrade_factor(item)
        self.assertEqual(factor, 1)


class GildedRoseApprovalTest(unittest.TestCase):
    "Test functionality on a mixed set of items"

    def test_various_items(self):
        "Test that sensible results come out in a mixed list"
        # given
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
        ]
        gilded_rose = GildedRose(items)
        # when
        gilded_rose.update_items()
        # then
        items_expected = [
            Item(name="+5 Dexterity Vest", sell_in=9, quality=19),
            Item(name="Aged Brie", sell_in=1, quality=1),
            Item(name="Elixir of the Mongoose", sell_in=4, quality=6),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=14, quality=21),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=50),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=4, quality=50),
            Item(name="Conjured Mana Cake", sell_in=2, quality=5),  # <-- :O
        ]

        self.assertListEqual(
            [repr(item) for item in gilded_rose.items],
            [repr(item) for item in items_expected])

        # also when?
        gilded_rose.update_items()

        items_expected = [
            Item(name="+5 Dexterity Vest", sell_in=8, quality=18),
            Item(name="Aged Brie", sell_in=0, quality=2),
            Item(name="Elixir of the Mongoose", sell_in=3, quality=5),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=13, quality=22),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=8, quality=50),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=50),
            Item(name="Conjured Mana Cake", sell_in=1, quality=4),  # <-- :O
        ]

        self.assertListEqual(
            [repr(item) for item in gilded_rose.items],
            [repr(item) for item in items_expected])


if __name__ == '__main__':
    unittest.main()
