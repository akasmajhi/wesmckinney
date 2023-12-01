print(f"NAME: In Helper: {__name__}")
if __name__ == "helper" or "__main__":
    from common.constants import BASE_DIR, D_LOGGER, LOGGER, NSE_HOLIDAYS,\
    BHAV_DIR, YEARLY_FETCH_URL, valid_periods, SYMBOLS_DATA_DIR,\
    BHAV_HEADER
else:
    from .constants import BASE_DIR, D_LOGGER, LOGGER, NSE_HOLIDAYS, BHAV_DIR,\
    YEARLY_FETCH_URL, valid_periods, SYMBOLS_DATA_DIR, BHAV_HEADER

from datetime import date, datetime, timedelta
import os
import requests

import pandas as pd
from requests.exceptions import HTTPError


f_name = __file__.split('/')[-1]

def compose_bhav_csv_name(t_date: date):
    m_name = "compose_bhav_csv_name"
    log_append = f"File: {f_name} Module: {m_name}" 
    if(t_date):
        t_day, t_mon, t_year = t_date.strftime("%d"), \
                            t_date.strftime("%b").upper(),  \
                            t_date.strftime("%Y") 
        result = "cm" + t_day + t_mon + t_year + "bhav.csv"
        if LOGGER:
            print(f"{log_append}: result [{result}]")
        return result
    return None

def is_trading_date_valid(t_date: date):
    """
    Checks validity of a date
        This function takes a date and verifies wether the date is valid trading
        day or not(weekends, NSE holidays are invalid). Also, for the current date time shouldn't be before 7:00pm/19:00hrs for a valid date

    Parameters: 
    -----------
    t_date: datetime.date
        Date for which the validity check needs to be done

    Returns: 
    --------
    None or datetime.date
        None if the date is invalid else return the argument
    """
    m_name = "is_trading_date_valid"
    log_append = f"File: {f_name} Module: {m_name}" 
    print(f"{log_append}: date passed: [{t_date}]")
    if t_date:
        #Checks for Weekend
        if(t_date.strftime("%w") == "6" or t_date.strftime("%w") == "0"):
            print(f"{log_append}: Weekend, Market Closed")
            return False
        today =  date.today()
        #Checks for Holidays
        for i in range(0 , len(NSE_HOLIDAYS)):
            if ( t_date == NSE_HOLIDAYS[i] ):
                print(f"{log_append}:Holiday, Market closed")
                return False                
        #Checks for future date
        if (today < t_date):
            print(f"{log_append}: Future dates are not allowed until time-travel is cracked!")
            return False
        #Checks for same date
        if (t_date == today):
            # time_now = datetime.now()
            # bhav copy not available until cutoff time 
            if(check_cutoff_time()): 
                print(f"{log_append}: Work in progress, kindly wait till 7:00pm / 19:00hrs")
                return False
            else:
                return True
        # Checks for previous date
        # This code is possibly useless!
        # if(today > t_date):
        #     return t_date
    return True

def check_cutoff_time():
    """Checks if current time is less then 7:00pm/19:00hrs
        This function returns true if the current local time is less then 7:00pm/19:00hrs
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    True if time is less then 7:00pm/19:00hrs
    False if time is greater than 7:00pm/19:00hrs
    """
    m_name = "check_cutoff_time"
    log_append = f"File: {f_name} Module: {m_name}" 
    time_now = int(datetime.now().strftime("%H"))
    print(f"{log_append}: Current time is: [{time_now}]")
    if (time_now < 19):
        print(f"{log_append}: You cannot download bhav copy before the cutoff time!")
        return False
    else:
        print(f"{log_append}: Cut-Off Time Check passed!")
        return True
def is_csv_existing(csv_file: str):
    """
    Checks for the existance of the CSV file.
        The csv file name follows the standard convention 
    Parameters
    ----------
    csv_file_name: str
        Name of the CSV file (for example, cm23OCT2023bhav.csv)
    Returns
    -------
    True: If the CSV file exists in the disk
    False: If the CSV file does not exist on the disk
    """
    m_name = "is_csv_existing"
    log_append = f"File: {f_name} Module: {m_name}" 
    if LOGGER:
        print(f"{log_append}: CSV file in: [{csv_file}]")
    csv_file_full_path = os.path.join(BHAV_DIR, csv_file)
    if LOGGER:
        print(f"{log_append}: csv file full path: [{csv_file_full_path}]")
    if (os.path.exists(csv_file_full_path)):
        print(f"{log_append}: CSV File: [{csv_file}] is existing")
        return True
    print(f"{log_append}: CSV File: [{csv_file}] is NOT existing!")
    return False

def get_bhav_copy(t_date: date):
    """Gets the bhav copy for the specified date 
    Parameters
    ----------
    t_date: date 
    Returns
    -------
    df: pandas.DataFrame
        Pandas DataFrame containing the bhav copy for the given date

    Description
    -----------
    If the data exists for that date then return dataFrame or None.

    """
    m_name = "get_bhav_copy"
    log_append = f"File: {f_name} Module: {m_name}" 
    if LOGGER:
        print(f"{log_append} Trading Date: [{t_date}] X1")
    # Check if this a valid date 
    if (is_trading_date_valid(t_date)):
        csv_name = compose_bhav_csv_name(t_date)
        if D_LOGGER:
            print(f"{log_append}: csv_name: {csv_name}")
            print(f"{log_append}: BHAV_DIR: {BHAV_DIR}")
        csv_file_path = os.path.join(BHAV_DIR, csv_name)
        if D_LOGGER:
            print(f"{log_append}: csv_file_path: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        # if D_LOGGER:
        #     print(f"{log_append}: CSV file as DF: {df}")
        return df
    # If the date is valid then check if this file is existing locally
    # If CSV exists locally then return it
    # If the CSV does not exist then fetch the bhav copy and store it and return
    # it.
    return None

def fetch_yearly_data(symbol: str):
    # https://www.nseindia.com/api/historical/cm/equity?symbol=EASEMYTRIP&series=[%22BE%22]&from=01-04-2021&to=31-03-2022
    m_name = "fetch_yearly_data"
    log_append = f"File: {f_name} Module: {m_name}" 
    if LOGGER:
        print(f"{log_append} Symbol Date: [{symbol}]")
    response = None
    try:
        symbol_yearly_url = YEARLY_FETCH_URL + symbol
        print(f"{log_append} symbol_yearly_url: [{symbol_yearly_url}]")
        response = requests.get(symbol_yearly_url)
        response.raise_for_status()
    except HTTPError as http_error:
        print(f"{log_append} HTTP Error Occured: [{http_error}]")
    except Exception as err:
        print(f"{log_append} Error Occured: [{err}]")
    else:
        print(f"{log_append} HTTP Request was successful")
    if response and response.content:
        return response.content
    return None

def create_symbol_wise_data(symbol: str, period: str):
    """Read the daily bhav copies and read the data specific to the symbol
    passed in the parameter. Each row (present in the daily bhav) needs to go
    into the symbol specific file.
    Parameters
    ----------
    symbol: str
        The symbol (for the stock)
    duration: str
        Refer to the constants.valid_periods array
    Return: pd.DataFrame
        DataFrame consisting of the data for the concerned symbol.
    """
    m_name = "create_symbol_wise_data"
    log_append = f"File: {f_name} Module: {m_name}" 
    if D_LOGGER:
        print(f"{log_append}: Params: symbol: [{symbol}] Period: [{period}]")
    symbols_data = pd.DataFrame(data=[], columns=BHAV_HEADER)
    # Check for valid period
    if period and period in valid_periods:
        # Read the daily bhav copies
        if period.upper() == 'YEAR':
            # Read data from last 365 days
            today = date.today()
            for d in pd.date_range(today-timedelta(days=365),today, freq='d'):
                # The following lines are most in-elegant code
                day = int(d.strftime("%d"))
                mon = int(d.strftime("%m"))
                year = int(d.strftime("%Y"))
                a_date = date(year, mon, day)
                bhav = get_bhav_copy(a_date)
                if bhav is not None:
                    # Extract data for the specific symbol
                    tmp = bhav[bhav["SYMBOL"] == symbol]
                    # append it to the symbol specific construct
                    symbols_data = pd.concat([symbols_data, tmp]) 
            # Write the data to the CSV and 
            csv_file = symbol + ".csv"
            symbols_data.to_csv(os.path.join(SYMBOLS_DATA_DIR, csv_file))
            return symbols_data

    else:
        print(f"{log_append}: Invalid period: {period}")
        return None
    # Return the data

def get_symbol_wise_data(symbol: str, period: str):
    """
    Helper function that collates data from bhav copies and creates a file that
    contains all the data related to the symbol that is passed in the parameter
    Parameters
    ----------
    symbol: str
        Name of the stock for which data is sought!
    period: str
        'Year', 'month', etc. Refer to common/constants/valid_periods
    Returns: pd.DataFrame
        DataFrame containing symbol data
    """
    m_name = "compose_symbol_wise_data"
    log_append = f"File: {f_name} Module: {m_name}" 
    if D_LOGGER:
        print(f"{log_append}: Params: symbol: [{symbol}] Period: [{period}]")
    # Verify if symbol and period are valid
    if period == '':
        period = "YEAR"
    if (symbol and period.upper() in valid_periods):
        # print(f"{log_append}: symbol and period are valid")
        # TODO Create a masterlist for valid symbols
        # Verify if the symbol file is present
        csv_file = symbol + '.csv'
        csv_file_full_path = os.path.join(SYMBOLS_DATA_DIR, csv_file)
        if (os.path.exists(csv_file_full_path)):
            print(f"{log_append}: {symbol}.csv file exists!")
            # If the symbol file is present then read it and return the DataFrame
            data = pd.read_csv(csv_file_full_path)
            # TODO The data in the CSV file may not be the latest / upto-date
            return data 
        else:
            print(f"{log_append}: {symbol}.csv file DOES NOT exists!")
            # If it is not present then create it and populate the data 
            return create_symbol_wise_data(symbol, period)
            # Return the data 

    # If you are here then either the symbol is invalid or the period
    print(f"{log_append}: Either Symbol or period is invalid") 
    return None

if __name__ == "__main__":
    if LOGGER:
        print("Main called!" + BASE_DIR)
    # get_bhav_copy(date(2023, 10, 10))
    check_cutoff_time()
