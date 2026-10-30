import unittest

from mqtt.utils import normalize_name_to_id


class TestUnitNormalizeNameToId(unittest.TestCase):

    def test_unit_returns_same_value_if_already_normalized(self):
        self.assertEqual('normalized_value',
                         normalize_name_to_id('normalized_value'))

    def test_unit_returns_lowercase(self):
        self.assertEqual('normalized_value',
                         normalize_name_to_id('NoRmAlIzEd VaLuE'))

    def test_unit_returns_value_with_special_chars_replaced(self):
        self.assertEqual('n0r_v_aliz3d',
                         normalize_name_to_id('n0r|v!aliz3d'))

    def test_unit_returns_value_with_special_chars_unicode_1_replaced(self):
        self.assertEqual('kozuscek',
                         normalize_name_to_id('køžuščêk'))

    def test_unit_returns_value_with_special_chars_unicode_2_replaced(self):
        self.assertEqual('__',
                         normalize_name_to_id('北亰'))

    def test_coffee_machine_zone_has_ascii_discovery_identifier(self):
        self.assertEqual('flood_machine_cafe',
                         normalize_name_to_id('FLOOD Machine Café'))

    def test_decomposed_accent_keeps_the_same_identifier(self):
        self.assertEqual(normalize_name_to_id('FLOOD Machine Café'),
                         normalize_name_to_id('FLOOD Machine Cafe\u0301'))

    def test_unnamed_unicode_control_character_does_not_stop_gateway(self):
        self.assertEqual('zone_name', normalize_name_to_id('Zone\x00Name'))


if __name__ == '__main__':
    unittest.main()
