from datetime import date
import pandas as pd 

import common.helper as helper

# from common import helper
f_name = __file__.split('/')[-1]

def daily_volume_gainers(stk_category: str):
    """
    Returns the daily volume gainers for a specified type 
    Parameters:
    ----------
    stk_category: str
        The stock category (NIFTY50, FNO, Cash, etc.)
    Returns:
    -------
    pandas.DataFrame
    """
    m_name = "volume_gainers"
    log_append = f"File: {f_name} Module: {m_name}"
    print(f"{log_append} Entry with stock type: [{stk_category}]")
    return None

def volume_gainers(trading_date, duration):
    """
    Returns the top-n volume gainers
        The individual volume gainer is calculated on the basis of specific
    time period. (weekly, monthly, quarterly or yearly)
    Parameters:
    -----------
    trading_date: date 
    time_period: str 

    Returns:
    -------
    pandas.DataFrame
    """
    m_name = "volume_gainers"
    log_append = f"File: {f_name} Module: {m_name}"
    print(f"{log_append} date: [{trading_date}] duration: [{duration}]")

    if (trading_date == None and duration == None):
        print(f"{log_append} Both params None. Calling daily_volume_gainers")
        return None

def daily_price_gainers(trading_date: date):
    m_name = "daily_price_gainers"
    log_append = f"File: {f_name} Module: {m_name}"
    print(f"{log_append} date: [{trading_date}]")
    df:pd.DataFrame = pd.DataFrame(helper.get_bhav_copy(trading_date))
    df_eq: pd.DataFrame = pd.DataFrame(df[df.SERIES == 'EQ'])
    print(f"{log_append}: Length of Equities DF: {len(df_eq.SERIES)}")
    # print(df_eq["SERIES"])
    
    return df_eq

def price_gainers(trading_date, duration):
    """
    Returns the top-n price gainers
        The individual price gainer is calculated on the basis of last clsoing
        price
    Parameters:
    -----------
    trading_date: date 
    time_period: str 

    Returns:
    -------
    pandas.DataFrame
    """
    m_name = "price_gainers"
    log_append = f"File: {f_name} Module: {m_name}"
    print(f"{log_append} date: [{trading_date}] duration: [{duration}]")

    if (trading_date == None and duration == None):
        print(f"{log_append} Both params None. Calling daily_price_gainers")
        df = daily_price_gainers(date.today())
        print(f"{log_append}: daily data: [{df}]")
        # Filter out unwanted series. Keep only EQ

    if (trading_date and duration == None):
        print(f"{log_append}: Trading date: [{trading_date}] and duration is None")
        df = daily_price_gainers(trading_date)

    return None
if __name__ == "__main__":
    pass
