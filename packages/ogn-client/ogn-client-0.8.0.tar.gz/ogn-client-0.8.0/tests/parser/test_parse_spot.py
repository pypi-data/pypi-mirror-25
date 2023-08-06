import unittest

from ogn.parser.parse import parse_spot_beacon


class TestStringMethods(unittest.TestCase):
    def test(self):
        message = parse_spot_beacon("id0-2860357 SPOT3 GOOD")

        self.assertEqual(message['id'], "0-2860357")
        self.assertEqual(message['hw_version'], 3)
        self.assertEqual(message['wtf'], "GOOD")


if __name__ == '__main__':
    unittest.main()
