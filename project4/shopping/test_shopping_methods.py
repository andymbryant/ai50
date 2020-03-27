import unittest

from shopping import load_data

class TestMethods(unittest.TestCase):
    def test_load_data(self):
        filename0 = 'shopping'
        load_data(filename0)

if __name__ == '__main__':
    unittest.main()