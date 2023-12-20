from datetime import date
import unittest 

if __name__ == "__main__":
    import weekly
else:
    from analytics import weekly

class test_weekly(unittest.TestCase):
    def test_weekly_price_gainers(self):
        t_start_date = date(2023, 12, 3)
        filter = {
            "start_date": t_start_date,
            "stock_type": "FNO",
            "duration": "WEEK",
        }
        self.assertIsNotNone(weekly.weekly_price_gainers(filter), "Weekly gainers worked!")

if __name__ == "__main__":
    unittest.main()

