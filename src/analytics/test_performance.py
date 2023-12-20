from datetime import date
import unittest 

if __name__ == "__main__":
    import performance
else:
    from analytics import performance

class test_weekly(unittest.TestCase):

    def test_since_listing(self):
        self.assertIsNotNone(performance.since_listing(None))
        # self.assertIsNotNone(performance.since_listing(2022))

if __name__ == "__main__":
    unittest.main()


