import pandas as pd
from matplotlib import pyplot as plt


def ext_sel_da(df, country_code, start_year, end_year):
    """
    Select data from a fixed Dataframe based on the given country abbreviation and time period (from start_year
    to end_year) and form a dictionary with these data and their corresponding years. Finally, the dictionary
    is returned.

    :param df: Dataframe
    :param country_code: Abbreviation of country name. For example, China is "CHN"
    :param start_year: First year of required information
    :param end_year: Last year of required information
    :return: A dictionary containing years and fertility rate data for the corresponding years

        >>> fr_data = pd.read_csv('Data/Fertility rates.csv', skiprows=4)
        >>> ext_sel_da(fr_data, 'CHN', 2018, 2021)
        {'2018': 1.554, '2019': 1.496, '2020': 1.281, '2021': 1.164}
    """
    data = df[df['Country Code'] == country_code]
    year_columns = [str(year) for year in range(start_year, end_year + 1)]
    rates = data.iloc[0][year_columns]
    rate_dict = {year: rate for year, rate in zip(year_columns, rates)}
    return rate_dict


def ext_sel_covid(df, country_code):
    """
    Find the required data from the Dataframe that records COVID-19 related data based on the given country
    abbreviation and form a dictionary with these data and their corresponding years. Finally, the dictionary
    is returned.

    :param df: Dataframe
    :param country_code: Abbreviation of country name. For example, China is "CN"
    :return: A dictionary containing years and COVID-19 inflection data for the corresponding years

        >>> covid_data = pd.read_csv('Data/WHO-COVID-19-global-data.csv')
        >>> ext_sel_covid(covid_data, 'CN')
        Year
        2020       96673
        2021       35398
        2022    84792971
        2023    14394816
        Name: New_cases, dtype: int64
    """
    covid_data = df[df['Country_code'] == country_code].copy()
    covid_data['Year'] = pd.to_datetime(covid_data['Date_reported']).dt.year
    case_by_year = covid_data.groupby('Year')['New_cases'].sum()
    return case_by_year


def ext_sel_polio(df, country_code):
    """
    Find the required data from the Dataframe that records poliomyelitis related data based on the given country
    abbreviation and form a dictionary with these data and their corresponding years. Finally, the dictionary
    is returned.

    :param df: Dataframe
    :param country_code: Abbreviation of country name. For example, China is "CHN"
    :return: A dictionary containing years and poliomyelitis inflection data for the corresponding years

            >>> polio_data = pd.read_csv('Data/the-number-of-reported-paralytic-polio-cases.csv')
            >>> ext_sel_polio(polio_data, 'CHN')
                  Year  Total (reported) polio cases
            1426  1980                          7442
            1427  1981                          9625
            1428  1982                          7741
            1429  1983                          3296
            1430  1984                          1626
            1431  1985                          1537
            1432  1986                          1844
            1433  1987                           969
            1434  1988                           667
            1435  1989                          4623
            1436  1990                          5065
            1437  1991                          1926
            1438  1992                          1191
            1439  1993                           653
            1440  1994                           261
            1441  1995                           165
            1442  1996                             3
            1443  1997                             0
            1444  1998                             0
            1445  1999                             1
            1446  2000                             0
            1447  2001                             0
            1448  2002                             0
            1449  2003                             0
            1450  2004                             2
            1451  2005                             0
            1452  2006                             0
            1453  2007                             0
            1454  2008                             0
            1455  2009                             0
            1456  2010                             0
            1457  2011                            21
            1458  2012                             2
            1459  2013                             0
            1460  2014                             0
            1461  2015                             0
            1462  2016                             0
            1463  2017                             0
            1464  2018                             0
            1465  2019                             1
            1466  2020                             0
            1467  2021                             0
    """
    polio_data = df[df['Code'] == country_code]
    polio_cases = polio_data[['Year', 'Total (reported) polio cases']]
    return polio_cases


def ext_sel_hiv(df, country_code):
    """
    Find the required data from the Dataframe that records HIV related data based on the given country
    abbreviation and form a dictionary with these data and their corresponding years. Finally, the dictionary
    is returned.

    :param df: Dataframe
    :param country_code: Abbreviation of country name. For example, China is "CHN"
    :return: A dictionary containing years and HIV inflection data for the corresponding years
    """
    hiv_data = df[df['Code'] == country_code]
    hiv_cases = hiv_data[['Year', 'Current number of cases of hiv/aids per 100 people, in both sexes aged 15-49 years']]
    return hiv_cases


def plot_dt_draw(dt_dict, country_code, country, year_size):
    """
    Filter the corresponding information in the dictionary based on the abbreviation of the country name and
    the complete name of the country to draw a line chart. The X-axis interval of the line chart is
    year-size

    :param dt_dict: Dictionary
    :param country_code: Abbreviation of country name. For example, Syrian is "SYR"
    :param country: Complete name of the country. For example, Syrian is "Syrian Arab Republic"
    :param year_size: The X-axis interval of the line chart
    """
    years = list(map(int, dt_dict.keys()))
    rates = list(dt_dict.values())
    plt.figure(figsize=(10, 6))
    plt.plot(years, rates, label=country_code, marker='o')
    plt.xticks(range(min(years), max(years) + 1, year_size))
    plt.title(f"Death Rate in {country} ({min(years)}-{max(years)})")
    plt.xlabel("Year")
    plt.ylabel("Death Rate")
    plt.grid(True)
    plt.legend()
    plt.show()


def calculate_change_rate(data_dict):
    """
    Calculate the annual change rate of the values in the dictionary value.

    :param data_dict: A dictionary with year as key and data as value
    :return: A dictionary with year as key and change rate as value

    >>> fr_data = pd.read_csv('Data/Fertility rates.csv', skiprows=4)
    >>> usa_fr = ext_sel_da(fr_data, 'USA', 2018, 2021)
    >>> calculate_change_rate(usa_fr)
    {'2019': -0.013587742122000621, '2020': -0.03780773739742087, '2021': 0.013706975327444389}
    """
    change_rates = {}
    previous_value = None
    for year, value in data_dict.items():
        if previous_value is not None:
            if previous_value != 0:
                change_rate = (value - previous_value) / previous_value
            else:
                change_rate = 0
            change_rates[year] = change_rate
        previous_value = value
    return change_rates


# def calculate_covid_change_rate(covid_cases_series):
#     covid_cases_df = covid_cases_series.to_frame(name='New_cases')
#     covid_cases_df['Change Rate'] = covid_cases_df['New_cases'].pct_change()
#     return covid_cases_df['Change Rate'].to_dict()


def plot_fertility_rates(data_dict, country_name, start_year, end_year, step=3):
    """
    Based on the country name and the selected time period (from start_year to end_year), draw a line chart from
    the corresponding fertility rate information in the filter dictionary. The X-axis interval of the line chart
    is step.

    :param data_dict: Dictionary
    :param country_name: Country name
    :param start_year: First year of required information
    :param end_year: Last year of required information
    :param step: The X-axis interval of the line chart
    """
    years = list(map(int, data_dict.keys()))
    rates = list(data_dict.values())
    plt.figure(figsize=(10, 6))
    plt.plot(years, rates, label=country_name, marker='o')
    plt.xticks(range(start_year, end_year + 1, step))
    plt.title(f"Fertility Rates in {country_name} ({start_year}-{end_year})")
    plt.xlabel("Year")
    plt.ylabel("Fertility Rate")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_normalized_rates(fertility_rates, death_rates):
    """
    Draw a line chart based on data from the fertility dictionary and data from the mortality dictionary.

    :param fertility_rates: Dictionary containing fertility data
    :param death_rates: Dictionary containing fertility data
    """
    df = pd.DataFrame({'Fertility_Rates': fertility_rates, 'Death_Rates': death_rates})
    df_normalized = (df - df.min()) / (df.max() - df.min())
    df_normalized.plot()
    plt.title('Normalized Fertility and Death Rates Over Years')
    plt.xlabel('Year')
    plt.ylabel('Normalized Rates')
    plt.show()
