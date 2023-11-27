import pandas as pd


def ext_sel_fr(df, country_code, start_year, end_year):
    data = df[df['Country Code'] == country_code]
    year_columns = [str(year) for year in range(start_year, end_year + 1)]
    fertility_rates = data.iloc[0][year_columns]
    fertility_rate_dict = {year: rate for year, rate in zip(year_columns, fertility_rates)}
    return fertility_rate_dict
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
