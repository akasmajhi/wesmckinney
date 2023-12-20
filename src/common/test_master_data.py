from datetime import date
import unittest 

if __name__ == "__main__":
    import master_data
else:
    from common import master_data

class test_weekly(unittest.TestCase):
    def test_equity_master(self):
        self.assertIsNotNone(master_data.get_equity_master(exchange='BSE'))

if __name__ == "__main__":
    unittest.main()


