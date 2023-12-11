import pandas as pd
from matplotlib import pyplot as plt


def ext_sel_da(df, country_code, start_year, end_year):
    """
        Reads the dataset from the given path and then converts it to a dataframe, where it then drops the unwanted columns
        and sets an index based on the user input. It will then transpose the data and return the converted dataframe.

        param df: Dataframe
        param country_code: Abbreviation of country name. For example, China is "CHN"
        param start_year: First year of required information
        param end_year: Last year of required information
        return: A dictionary containing years and fertility information for the corresponding years

        """
    data = df[df['Country Code'] == country_code]
    year_columns = [str(year) for year in range(start_year, end_year + 1)]
    rates = data.iloc[0][year_columns]
    rate_dict = {year: rate for year, rate in zip(year_columns, rates)}
    return rate_dict


def ext_sel_covid(df, country_code):
    covid_data = df[df['Country_code'] == country_code].copy()
    covid_data['Year'] = pd.to_datetime(covid_data['Date_reported']).dt.year
    case_by_year = covid_data.groupby('Year')['New_cases'].sum()
    return case_by_year


def ext_sel_polio(df, country_code):
    polio_data = df[df['Code'] == country_code]
    polio_cases = polio_data[['Year', 'Total (reported) polio cases']]
    return polio_cases


def ext_sel_hiv(df, country_code):
    hiv_data = df[df['Code'] == country_code]
    hiv_cases = hiv_data[['Year', 'Current number of cases of hiv/aids per 100 people, in both sexes aged 15-49 years']]
    return hiv_cases


def plot_dt_draw(dt_dict, country_code, country, year_size):
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
    df = pd.DataFrame({'Fertility_Rates': fertility_rates, 'Death_Rates': death_rates})
    df_normalized = (df - df.min()) / (df.max() - df.min())
    df_normalized.plot()
    plt.title('Normalized Fertility and Death Rates Over Years')
    plt.xlabel('Year')
    plt.ylabel('Normalized Rates')
    plt.show()
