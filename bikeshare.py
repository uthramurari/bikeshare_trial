import numpy as np
import time
import pandas as pd
import calendar
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def check_user_entry(prompt, valid_entries):
    """
    Args:
        (str) prompt: Specific prompt text
        (list) valid_entries: List of all possible valid entries

    Returns:
        (str) user_input: Valid user input

    """
    user_input = input(prompt).lower()
    while user_input not in valid_entries:
        print('Wrong Input. Please try again')
        user_input = input(prompt).lower()
    return user_input


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).

    valid_entries = CITY_DATA.keys()
    print('\nCity list:')
    print(*valid_entries, sep=', ')
    prompt = 'Select a city: '
    city = check_user_entry(prompt, valid_entries)

    # get user input for month (all, january, february, ... , june)

    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_entries = month_list
    print('\nMonth list:')
    print(*valid_entries, sep=', ')
    prompt = 'Select a month for which you need data: '
    month = check_user_entry(prompt, valid_entries)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    weekday_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    valid_entries = weekday_list
    print('\nDay of Week list:')
    print(*valid_entries, sep=', ')
    prompt = 'Select a weekday for which you need data: '
    day = check_user_entry(prompt, valid_entries)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # month filter
    df['Month'] = df['Start Time'].dt.month_name()
    if month != 'all':
        df = df[df['Month'] == month.title()]

    # day of week filter
    df['Week Day'] = df['Start Time'].dt.day_name()
    if day != 'all':
        df = df[df['Week Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel in the chosen subset of data."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mc_month = df['Month'].mode().values[0]
    mc_month_count = (df['Month'] == mc_month).sum()
    print('The most common month: {}, Count: {}'.format(mc_month, mc_month_count))

    # display the most common day of week
    mc_dow = df['Week Day'].mode().values[0]
    mc_dow_count = (df['Week Day'] == mc_dow).sum()
    print('The most common day of week: {}, Count: {}'.format(mc_dow, mc_dow_count))

    # display the most common start hour
    mc_start_hr = df['Start Time'].dt.hour.mode().values[0]
    mc_start_hr_count = (df['Start Time'].dt.hour == mc_start_hr).sum()
    print('The most common start hour: {}, Count: {}'.format(mc_start_hr, mc_start_hr_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip in the chosen subset of data."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_stn = df['Start Station'].mode().values[0]
    mc_start_stn_count = (df['Start Station'] == mc_start_stn).sum()
    print('The most common start station: {}, Count: {}'.format(mc_start_stn, mc_start_stn_count))

    # display most commonly used end station
    mc_end_stn = df['End Station'].mode().values[0]
    mc_end_stn_count = (df['End Station'] == mc_end_stn).sum()
    print('The most common end station: {}, Count: {}'.format(mc_end_stn, mc_end_stn_count))

    # display most frequent combination of start station and end station trip
    start_end_stn = df['Start Station'] + ' - ' + df['End Station']
    mc_start_end = start_end_stn.mode().values[0]
    mc_start_end_count = (start_end_stn == mc_start_end).sum()
    print('The most common start-end trip combination: {}, Count: {}'.format(mc_start_end, mc_start_end_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration of the chosen subset of data"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())
    # display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
     > Count of: User type, Gender type
     > Statistics based on year of birth - max, min and most common year of birth
     """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user type:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nCount of gender:')
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('The column \'Gender\' does not exist in {}.csv'.format(city))

    # Display earliest, most recent, and most common year of birth
    print('\nBirth Year details:')
    if 'Birth Year' in df.columns:
        print('Earliest Year of Birth:', df['Birth Year'].min())
        print('Most recent Year of Birth:', df['Birth Year'].max())
        print('Most common Year of Birth:', df['Birth Year'].mode().values[0])
    else:
        print('The column \'Birth Year\' does not exist in {}.csv'.format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def print_records(df):
    """Prints the first 5 records by default and
    prints the next 5 records based on user response"""

    print('\nDisplaying the first 5 records:')
    for i in range(0, len(df), 5):
        print(tabulate(df[i:i + 5], headers=df.columns))
        next_5 = input('Do you want to display the next 5 records? Y / N : ')
        if next_5 in ('Y', 'y'):
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print_records(df)

        restart = input('\n Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
