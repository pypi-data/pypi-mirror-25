from unittest import TestCase

import testpackage_ammar

class TestJoke(TestCase):
    def test_is_string(self):
        s = testpackage_ammar.joke()
        self.assertTrue(isinstance(s, basestring))