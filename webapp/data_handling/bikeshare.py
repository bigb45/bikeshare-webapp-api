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
        # prompt = "did you mean " + city + "?"
        # ans = prompt_user(prompt, ['yes', 'no'], ['yes', 'no', 'y', 'n'])
        # if ans == 'n' or ans == 'no':
        #     return 0


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


def load_city_data(city):
    try:
        print('loading data for ', city)
        bikeshare_data = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
        return bikeshare_data.head()
    except Exception as e:
        print("caught error {}".format(e))
