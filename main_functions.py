import pandas as pd
from matplotlib import pyplot as plt


def ext_sel_da(df, country_code, start_year, end_year):
    data = df[df['Country Code'] == country_code]
    year_columns = [str(year) for year in range(start_year, end_year + 1)]
    rates = data.iloc[0][year_columns]
    rate_dict = {year: rate for year, rate in zip(year_columns, rates)}
    return rate_dict
    # year_columns = usa_data_series.columns[4:-2]
    # fertility_rates = usa_data_series.iloc[0][4:-2]
    # fertility_rate_dict = {year: rate for year, rate in zip(year_columns, fertility_rates)}


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


def plot_dt_draw(dt_dict, country_label, year_size):
    years = list(map(int, dt_dict.keys()))
    rates = list(dt_dict.values())
    plt.figure(figsize=(10, 6))
    plt.plot(years, rates, label=country_label, marker='o')
    plt.xticks(range(min(years), max(years) + 1, year_size))
    plt.title(f"Death Rate in {country_label} ({min(years)}-{max(years)})")
    plt.xlabel("Year")
    plt.ylabel("Death Rate")
    plt.grid(True)
    plt.legend()
    plt.show()
