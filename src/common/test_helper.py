import unittest
from datetime import date, datetime 

print(f"NAME: In TEST_Helper: {__name__}")
if __name__ == "__main__":
    import helper 
else:
    from . import helper

class test_helper(unittest.TestCase):
    def test_compose_bhav_csv_name(self):
        t_date = date(2023, 11, 21)
        expected_output = 'cm21NOV2023bhav.csv'
        self.assertEqual(expected_output,  helper.compose_bhav_csv_name(t_date))

        t_date = date(2023, 1, 1)
        expected_output = 'cm01JAN2023bhav.csv'
        self.assertEqual(expected_output,  helper.compose_bhav_csv_name(t_date))

    def test_check_cufoff_time(self):

        # # print("Checking check_cutoff_time")
        now = datetime.now()
        # # If this is executed before 7 PM expect a False
        if (int(now.strftime("%H")) < 19):
            self.assertFalse(helper.check_cutoff_time())
        else:
            self.assertTrue(helper.check_cutoff_time())
            pass
        # # Or expect a True
        #     self.assertTrue(helper.check_cutoff_time(now))
        # past_valid_datetime = datetime(year=2023, month=11, day=11, hour=20,
        #                                minute=30)
        # self.assertTrue(helper.check_cutoff_time(past_valid_datetime))
        #
        # past_invalid_datetime = datetime(year=2023, month=11, day=11, hour=2,
        #                                minute=30)
        # self.assertFalse(helper.check_cutoff_time(past_invalid_datetime))

    def test_is_trading_date_valid(self):
        # print("Testing for validity of trading date")
        # pass a weekend date and expect a False
        t_date = date(2023, 9, 30) # SEP-30-2023 is a Saturday
        self.assertFalse(helper.is_trading_date_valid(t_date))
        # pass a NSE holiday and expect a False return
        t_date = date(2022,8,9)
        self.assertFalse(helper.is_trading_date_valid(t_date))
        # pass a future date and expect a False return
        t_date = date(2099, 1, 1)
        self.assertFalse(helper.is_trading_date_valid(t_date))
        # Pass today's date and expect True/False after/before 7 PM
        # t_date = date.today()
        # self.assertTrue(helper.is_trading_date_valid(t_date))

    def test_is_csv_existing(self):
        csv_file_valid = "cm21NOV2023bhav.csv"
        self.assertTrue(helper.is_csv_existing(csv_file_valid))
        csv_file_invalid = "cm19NOV2023bhav.csv"
        self.assertFalse(helper.is_csv_existing(csv_file_invalid))

    def test_fetch_yearly_data(self):
        """
        This method does not work because the URL is not getting fetched
        """
        symbol = 'AXISBANK'
        # self.assertIsNotNone(helper.fetch_yearly_data(symbol))
        pass

    def test_compose_symbol_wise_data(self):
        # Passing an invalid period to get None
        self.assertIsNone(helper.get_symbol_wise_data("INFY", 'INVALID_PERIOD'))
        self.assertIsNotNone(helper.get_symbol_wise_data("AXISBANK", 'YEAR'))

    def test_de_structure_bhav_name(self):
        # Positive Test case for correct file name
        csv_name = 'cm10NOV2023bhav.csv'
        self.assertEqual(helper.de_structure_bhav_name(csv_name),\
                ('10', 'NOV', '2023'))
        # Negative Test case for blank file name
        csv_name = ''
        self.assertEqual(helper.de_structure_bhav_name(csv_name),\
                (None, None, None))

    def test_fetch_bhav_copy(self):
        # Positive test case for a valid csv_name
        csv_name = 'cm10NOV2020bhav.csv'
        self.assertTrue(helper.fetch_bhav_copy(csv_name))
        # Negative test for a invalid csv name
        csv_name = 'cm10NOV20223bhav.csv'
        self.assertFalse(helper.fetch_bhav_copy(csv_name))
        pass

    def test_get_bhav_copy(self):
        # pass a valid and existing bhav copy
        t_date = date(2020, 11, 10)
        self.assertIsNotNone(helper.get_bhav_copy(t_date))
        # Try getting a bhav copy that does not exist
        t_not_date = date(2020, 11, 11)
        # TODO set up methods are useful here to prepare test data
        # If the bhav does not exist, it should fetch and return
        self.assertIsNone(helper.get_bhav_copy(t_not_date))


if __name__ == "__main__":
    unittest.main()
