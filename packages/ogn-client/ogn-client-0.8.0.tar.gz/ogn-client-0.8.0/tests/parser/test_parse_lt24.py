import unittest

from ogn.parser.utils import ms2fpm
from ogn.parser.parse import parse_lt24_beacon


class TestStringMethods(unittest.TestCase):
    def test(self):
        message = parse_lt24_beacon("id25387 +000fpm GPS")

        self.assertEqual(message['id'], 25387)
        self.assertAlmostEqual(message['climb_rate'] * ms2fpm, 0, 2)
        self.assertEqual(message['wtf'], 'GPS')


if __name__ == '__main__':
    unittest.main()
