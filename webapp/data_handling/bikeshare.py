import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = {'chicago': 'webapp/data/chicago.csv',
             'new york city': 'webapp/data/new_york_city.csv',
             'washington': 'webapp/data/washington.csv'}
weekdays = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july']


def prompt_user(prompt, choices, aliases):
    while True:
        print(prompt, "answer with", choices)
        ans = input().lower().strip()
        if ans in choices or ans in aliases:
            return ans
        elif ans == 'exit':
            raise SystemExit
        else:
            print('please provide an answer from the given list')


def get_closest_match(city):
    city_match = {'new york city': 0, 'washington': 0, 'chicago': 0}
    ny = 'new york city'
    wa = 'washington'
    chi = 'chicago'
    for i in city:
        if i in ny:
            ny = ny[ny.index(i):]
            city_match['new york city'] += 1
        if i in wa:
            wa = wa[wa.index(i):]
            city_match['washington'] += 1
        if i in chi:
            chi = chi[chi.index(i):]
            city_match['chicago'] += 1
    return max(city_match, key=city_match.get)


def get_city(city):
    ny = 'new york city'
    wa = 'washington'
    chi = 'chicago'

    if city in [ny, wa, chi]:
        return city
    else:
        city = get_closest_match(city)
        prompt = "did you mean " + city + "?"
        return (city, prompt)


def get_filters():
    month_filter = day_filter = 0
    input_error = False
    while 1:
        month_filter = input("enter a month or a list of months between January and July: ").lower(
        ).strip().replace(' ', '').split(',')
        for month in month_filter:
            if month not in months:
                print("please enter a month within the specified range.")
                input_error = True
        if input_error:
            input_error = False
            continue
        else:
            break
    while 1:
        day_filter = input("enter a day or a list of days of the week: ").lower(
        ).strip().replace(' ', '').split(',')
        for day in day_filter:
            if day not in weekdays:
                print("please check your spelling. could not understand {}".format(day))

        if input_error:
            input_error = False
            continue
        else:
            break

    return day_filter, month_filter


def format_time(col_name, new_col_name, df, pattern):
    df[new_col_name] = pd.to_datetime(
        df[col_name]).dt.time.map(lambda t: t.strftime(pattern))
    return df[new_col_name]


def format_date(col_name, new_col_name, df, pattern):
    df[new_col_name] = pd.to_datetime(
        df[col_name]).dt.date.map(lambda t: t.strftime(pattern))
    return df[new_col_name]


def seconds_to_dhm(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 86400) // 60
    # return "{} Days, {} Hours and {} Minutes".format(days, hours, minutes)

    return "{} Hours and {} Minutes".format(hours, minutes)

    # FIX THIS AS SOON AS YOU GET BACK


def filter_data(df, month_list, day_list):
    # print("Month is: {}".format(month))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df = pd.concat(
        map(lambda month: df[df['Month'] == (months.index(month)+1)], month_list))
    df = pd.concat(
        map(lambda day: df[df['Weekday'] == (day.title())], day_list))
    df = df.sample(frac=1)

    return df


def load_city_data(city, month, day, row_count):
    try:
        print('loading data for ', city,
              "filtering by {}, {}".format(month, day))
        bikeshare_data = pd.DataFrame(
            pd.read_csv(CITY_DATA[city])).drop("Unnamed: 0", axis=1)
        bikeshare_data = filter_data(bikeshare_data, month, day)
        format_date(
            'Start Time', 'Date', bikeshare_data, '%d/%m/%Y')
        format_time(
            'Start Time', 'Start Time', bikeshare_data, '%H:%M')
        format_time(
            'End Time', 'End Time', bikeshare_data, '%H:%M')
        bikeshare_data['Trip Duration'] = bikeshare_data['Trip Duration'].apply(
            seconds_to_dhm)
        # print(bikeshare_data.head())
        return bikeshare_data.fillna('-').head(row_count)
    except Exception as e:
        print("caught error {}".format(e))
