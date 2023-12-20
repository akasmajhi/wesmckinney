if __name__ == "helper" or "__main__":
    from common.constants import BASE_DIR, D_LOGGER, LOGGER, NSE_HOLIDAYS,\
    BHAV_DIR, YEARLY_FETCH_URL, valid_periods, SYMBOLS_DATA_DIR,\
    BHAV_HEADER, BASE_URL
else:
    from .constants import BASE_DIR, D_LOGGER, LOGGER, NSE_HOLIDAYS, BHAV_DIR,\
    YEARLY_FETCH_URL, valid_periods, SYMBOLS_DATA_DIR, BHAV_HEADER, BASE_URL

from datetime import date, datetime, timedelta
import os
import requests

import pandas as pd
import zipfile
from requests.exceptions import HTTPError

f_name = __file__.split('/')[-1]

def get_equity_master(exchange: str = 'NSE'):
    """Returns the master data for all equities listed in NSE
    Fields:
        SYMBOL: str - Stock name    
        NAME OF COMPANY: str - Company name    
        SERIES: str - 'BE', 'EQ', etc    
        DATE OF LISTING: str - String representation of listing date    
        . . . 
    """
    # Read the master/equities,csv and return the data frame
    m_name = "get_equity_master"
    log_append = f"File: {f_name} Module: {m_name}"
    print(f"{log_append} Exchange: {exchange}")
    # print(pd.read_csv('master/equities.csv')['SERIES'])
    # print(pd.read_csv('master/equities.csv').columns)
    return pd.read_csv('master/equities.csv')
