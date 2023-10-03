import datetime as dt
import pandas as pd
import numpy as np
from datetime import datetime
from utils import *

def split_into_chunks(skyscanner_input_data):
    """
    Split the input data into chunks, calculate percentages, and create DataFrames.

    Args:
    skyscanner_input_data (pandas.DataFrame): The input DataFrame to be processed.

    Returns:
    tuple: A tuple containing two DataFrames - percentage_df and passenger_df.
           - percentage_df: Contains percentage values rounded to 1 decimal place.
           - passenger_df: Contains passenger values rounded to 1 decimal place.

    Note:
    This function splits the input data into chunks, calculates percentages based on 'redirects',
    and creates two DataFrames - one for percentage values and one for passenger values.

    LAST_MONTHS_COUNT is used to determine the number of rows to keep in each chunk.
    """
    LAST_MONTHS_COUNT=6
    chunk_count = len(skyscanner_input_data) / 13
    chunks = np.array_split(skyscanner_input_data, chunk_count)

    chunk_list = []
    for chunk_df in chunks:
        chunk_df['percentage'] = (chunk_df['redirects'] / chunk_df['redirects'].sum()) * 100
        valid_indices = list(range(int(chunk_df.index[0]), int(chunk_df.index[12]) - LAST_MONTHS_COUNT))
        chunk_df = chunk_df.drop(valid_indices)
        chunk_df.reset_index(inplace=True, drop=True)
        chunk_list.append(chunk_df)

    percentage_df = pd.DataFrame()
    passenger_df = pd.DataFrame()
    
    for df in chunk_list:
        percentage_df[str(df['travel_month'].iloc[0])] = df['percentage'].apply(lambda x: round(x, 1))
        passenger_df[str(df['travel_month'].iloc[0])] = df['redirects'].apply(lambda x: round(x, 1))

    return percentage_df, passenger_df

def get_next_12_months():
    """
    Returns a tuple containing the current month and the next 11 months 
    starting from the current date.

    Returns:
        tuple: A tuple containing the year and month information for the current month 
               and the next 11 months. Each month is represented as a string in "YYYYMM" format.

    Example:
        >>> get_next_12_months()
        ('202309', '202310', '202311', '202312', '202401', '202402', '202403', '202404', '202405', '202406', '202407', '202408')
    """
    today = datetime.today()
    current_month = today.strftime("%Y%m")
    end_month = DateMonth.from_str(current_month)
    result = []
    for _ in range(12):
        result.append(str(end_month))
        end_month = end_month.next_month()
    return tuple(result)

def calculate_years(input_date:str, ignore_years:List[int]):
    """
    Calculate a list of years with the same month as the input date, 
    excluding specified years from the calculation.

    Args:
        input_date (str): A date in "YYYYMM" format to extract the month.
        ignore_years (List[int]): A list of years to exclude from the calculation.

    Returns:
        List[str]: A list of years in "YYYYMM" format that have the same month as input_date, 
                   excluding the specified years in ignore_years.

    Example:
        >>> calculate_years("202309", [2020])
        '202309': ['201909', '202109', '202209']
        '202310': ['201910', '202110', '202210']
        '202311': ['201911', '202111', '202211']
        '202312': ['201912', '202112', '202212']
        '202401': ['201901', '202101', '202201', '202301']
        '202402': ['201902', '202102', '202202', '202302']
        ...
    """ 
    year = int(input_date[:4])
    month = int(input_date[4:])
    years_to_include = []
    for i in range(2019, year):
        candidate_year = i
        if candidate_year not in ignore_years:
            years_to_include.append(str(candidate_year))
    result_dates = [year + str(month).zfill(2) for year in years_to_include]
    return result_dates



def compare_monthly_indices_and_passengers(result, IndexMean, passenger_df, CALCULATE_MONTHS_COUNT, LAST_MONTHS_COUNT):
    """
    Karşılaştırma yapar ve sonuçları ekrana basar.

    Parameters:
    - result (list): Sonuç verileri listesi.
    - IndexMean (dict): Ay bazında endeks ortalamalarını içeren sözlük.
    - passenger_df (dict): Ay bazında yolcu verilerini içeren sözlük.
    - CALCULATE_MONTHS_COUNT (int): Hesaplama için kullanılacak ay sayısı.
    - LAST_MONTHS_COUNT (int): Son ayların sayısı.

    Returns:
    - None
    """

    for month in result:
        for i in range(CALCULATE_MONTHS_COUNT):
            # print(month)
            A = round((IndexMean[month][LAST_MONTHS_COUNT-1]/IndexMean[month][LAST_MONTHS_COUNT-1-i]),2) 
            B = round((passenger_df[month][LAST_MONTHS_COUNT-1]/passenger_df[month][LAST_MONTHS_COUNT-1-i]),2)
            print( A==B)

# compare_monthly_indices_and_passengers(result, passenger_df_MODEL2, passenger_df_MODEL1, CALCULATE_MONTHS_COUNT, LAST_MONTHS_COUNT)

def update_redirect_passenger(df_file_, passenger_df_, result, CALCULATE_MONTHS_COUNT):
    """
    Belirli tarihler için "redirect_passenger" sütununu günceller.

    Parametreler:
    - df_file (DataFrame): Verilerin bulunduğu DataFrame.
    - passenger_df_ (DataFrame): Yolcu verilerinin bulunduğu DataFrame.
    - result (list): Hesaplama sonuçlarının bulunduğu liste.
    - CALCULATE_MONTHS_COUNT (int): Hesaplama yapılacak ay sayısı.

    Geri Dönüş Değeri:
    - None: DataFrame doğrudan güncellenir.
    """

    index_number = []
    for i in range(0,CALCULATE_MONTHS_COUNT):
        search_date = result[i]

        formatted_date = datetime.strptime(search_date, "%Y%m").strftime("%Y-%m-%d")

        filtered_df = df_file_[df_file_["date"] == pd.Timestamp(formatted_date)]
        index_number.append(filtered_df.index[0])


    for i in range(0,len(result)):
        df_file_["redirect_passenger"][index_number[i]] = passenger_df_[result[i]].sum()

    return df_file_
