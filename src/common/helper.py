print(f"NAME: In Helper: {__name__}")
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

def is_csv_file_name_valid(csv_name: str):
    """Performs validation on bhav csv file name.
    Parameter
    ---------
    csv_name: str
        Name of the CSV file. (cm10NOV2023bhav.csv)
    Return
        True if CSV file name is valid; False otherwise.
    """
    m_name = "is_csv_file_name_valid"
    log_append = f"File: {f_name} Module: {m_name}" 
    print(f"{log_append}: input csv_name: [{csv_name}]")
    # Is the file name valid (length is exactly 19)
    if (csv_name is not None and len(csv_name) != 19):
        if D_LOGGER:
            print(f"{log_append}: Invalid csv_name: [{csv_name}]")
        return False
    if D_LOGGER:
        print(f"{log_append}: Valid csv_name: [{csv_name}]")
    return True

def de_structure_bhav_name(csv_name: str):
    """Destructures the parts from a bhav CSV file name
        For a given bhav csv file name, extract it's parts.
    Parameter
    ---------
    bhav_csv_name: str
        String representation of the bhav csv name; for example, cm01DEC2022bhav.csv

    Return
    bahv_parts: tuple
        A tuple representing (DD, MM, YYYY) parts
    None: If the file name is invalid
    """
    m_name = "de_structure_bhav_name"
    log_append = f"File: {f_name} Module: {m_name}" 
    print(f"{log_append}: input csv_name: [{csv_name}]")
    if (not is_csv_file_name_valid(csv_name)):
        if D_LOGGER:
            print(f"{log_append}: Invalid CSV name passed: [{csv_name}]")
        return (None, None, None)
    if D_LOGGER:
        print(f"{log_append}: (dd, mmm, yyyy): [{(csv_name[2:4], csv_name[4:7],\
            csv_name[7:11]) }]")
    return (csv_name[2:4], csv_name[4:7], csv_name[7:11])

def fetch_bhav_copy(csv_name: str):
    """Fetches the bhav copy.
        This function will fetch the bhav copy from NSE site.
    Parameter
    ---------
    csv_name: str
        Name of the CSV file. (for example. cm10NOV2023bhav.csv)
    Return
    ------
    True if the fetch was successful. False otherwise.

    Validations
    -----------
    None
    """
    m_name = "fetch_bhav_copy"
    log_append = f"File: {f_name} Module: {m_name}" 
    print(f"{log_append}: csv_name: [{csv_name}]")
    (dd, mmm, yyyy) = de_structure_bhav_name(csv_name)
    if(dd is None or mmm is None or yyyy is None):
        return False
    print(f"{log_append}: (dd, mmm, yyyy): [{(dd, mmm, yyyy)}]")
    fetch_url = ""
    if (dd and mmm and yyyy):
        fetch_url = BASE_URL + "/" + yyyy + "/" + mmm + "/" + csv_name + ".zip"
        if D_LOGGER:
            print(f"{log_append}: Fetching for: [{dd}], [{mmm}], [{yyyy}]")
            print(f"{log_append}: fetch_url: [{fetch_url}]")
            # Download the ZIP file
        try:
            res = requests.get(fetch_url, allow_redirects=True,timeout=5.00)
            print(f"{log_append}: HTTP Response Code: [{res.status_code}]")
            if res.status_code == 200:
                # All well so far
                csv_zip_file_name = csv_name + ".zip"
                # Change path to store zip file
                with open(BHAV_DIR + csv_zip_file_name, "wb") as f:
                    f.write(res.content)
                    f.close()
                    # Extract the ZIP file to the destination folder
                    # Change path to extrtact zip file
                    with zipfile.ZipFile(BHAV_DIR + csv_zip_file_name, "r") as bhavzip:
                        bhavzip.extractall(path=BHAV_DIR)
                    # Change path to delete zip file
                    # delete the ZIP file 
                    if os.path.exists(BHAV_DIR + csv_zip_file_name):
                        print("f{log_append}: Removing ZIP file")
                        os.remove(BHAV_DIR + csv_zip_file_name)
                return True
            else:
                print("f{log_append}: Something Wrong with the fetch")
        except Exception as e:
            print(f"{log_append}: fetch_url: [{fetch_url}]")
            print(f"{log_append}:  Error in fetch: {e}")
            return False
        finally:
            # TODO What should be the return here?
            pass
    return False

def compose_bhav_csv_name(t_date: date):
    """Composes a bhav CSV file name based on the date passed. 
        This method does not perform any kind of validation check on the input.
        It is assumed that the caller will make the validation of date depending
        on whether it is a weekend or trading holiday!
    Parameter
    ---------
    t_date: datetime.date 
        The date for which bhav copy CSV name is to be composed.
    Return
    ------
    bhav_name: str 
        Bhav file name (for example, cm10NOV2023bhav.csv)
    """
    m_name = "compose_bhav_csv_name"
    log_append = f"File: {f_name} Module: {m_name}" 
    if(t_date):
        t_day, t_mon, t_year = t_date.strftime("%d"), \
                            t_date.strftime("%b").upper(),  \
                            t_date.strftime("%Y") 
        result = "cm" + t_day + t_mon + t_year + "bhav.csv"
        if D_LOGGER:
            print(f"{log_append}: result [{result}]")
        return result
    return None

def is_trading_date_valid(t_date: date):
    """
    Checks validity of a date
        This function takes a date and verifies wether the date is valid trading
        day or not(weekends, NSE holidays are invalid). Also, for the current
        date time shouldn't be before 7:00pm/19:00hrs for a valid date

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
    if D_LOGGER:
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

    Validations
    -----------
    checks for validity of trading date (holidays, weekdns, etc.)

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
        # If the date is valid then check if this file is existing locally
        if is_csv_existing(csv_file_path):
            # If CSV exists locally then read it and return it
            df = pd.read_csv(csv_file_path)
            # if D_LOGGER:
            #     print(f"{log_append}: CSV file as DF: {df}")
            return df
        else: # CSV doees NOT exist locally
            # If the CSV does not exist then fetch the bhav copy and store it and return it.
            if fetch_bhav_copy(str(csv_name)):
                df = pd.read_csv(csv_file_path)
            pass
    return None

def fetch_yearly_data(symbol: str):
    """Currently unusable. TODO
    """
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
    # check_cutoff_time()
