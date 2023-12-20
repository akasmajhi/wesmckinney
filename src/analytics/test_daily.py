from datetime import date
import unittest 

print(f"NAME: In TEST_Daily: {__name__}")
if __name__ == "__main__":
    import daily
else:
    from analytics import daily

class test_daily(unittest.TestCase):
    def test_volume_gainers(self):
        self.assertIsNone(daily.volume_gainers(None, None))
        pass 

    def test_price_gainers(self):
        pass 
    def test_daily_price_gainers(self):
        # TODO For today's bhav, you need to check cutoff time
        # self.assertIsNone(daily.daily_price_gainers(date.today()))
        # For a valid trading date
        self.assertIsNotNone(daily.daily_price_gainers(date(2023, 11, 22)))
        self.assertGreater(len(daily.daily_price_gainers(date(2023, 11, 22))), 1)
        # For a weekend you should get None
        # self.assertIsNone(daily.daily_price_gainers(date(2023, 11, 19)))
        # For a market close day, you should get None
        # self.assertIsNone(daily.daily_price_gainers(date(2022,8,9)))


if __name__ == "__main__":
    unittest.main()
