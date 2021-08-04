import time
import pandas as pd
import numpy as np
from pprint import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    city = 'any_town'
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        try:
            city = input('Please select a city to explore (chicago, new york city, washington): \n').lower()
        except:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = 'any_month'
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in months:
        try:
            month = input('Now, enter a month (january >> june or all): \n').lower()
        except:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'any_day'
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
        try:
            day = input('Lastly, select a weekday (monday >> sunday or all): \n').lower()
        except:
            break

    print('-'*40, '\n')
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
    df = pd.read_csv(CITY_DATA[city], index_col = 0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month (number): ', popular_month, '\n')

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week: ', popular_day, '\n')

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour, '\n')

    print("\nThis took %s seconds." % format((time.time() - start_time), ".2f"))
    print('-'*40, '\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start, '\n')

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end, '\n')

    # TO DO: display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'] + ' >>> ' + df['End Station']
    popular_route = df['start_to_end'].mode()[0]
    print('Most Popular Route:', popular_route, '\n')

    print("\nThis took %s seconds." % format((time.time() - start_time), ".2f"))
    print('-'*40, '\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = format((df['Trip Duration'].sum())/3600, ".2f")
    print('The total travel time was: ', total, ' hours. \n')

    # TO DO: display mean travel time
    mean = format((df['Trip Duration'].mean())/3600, ".2f")
    print('The mean travel time was: ', mean, ' hours. \n')

    print("\nThis took %s seconds." % format((time.time() - start_time),".2f"))
    print('-'*40, '\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('The distribution of user counts:\n', user_counts, '\n')

    # TO DO: Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
    except:
        print('Gender is not available for the city selected. (whomp whomp) \n')
    else:
        print('The distribution of Genders:\n', gender_counts, '\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
    except:
        print('Birth Year is not available for the city selected. (whomp whomp) \n')
    else:
        print('The earliest birth year: ', min_year)
        print('The latest birth year: ', max_year)
        print('The most common birth year: ', common_year)

    print("\nThis took %s seconds." % format((time.time() - start_time),".2f"))
    print('-'*40, '\n')


def show_data(df):
    start_row = 0
    show_data = 'yes'

    while show_data == 'yes':
        show_data = input('\nWould you like to see some raw data? (yes or no) \n')
        if show_data.lower() == 'yes':
            result_df = (df.iloc[start_row:start_row+5, : ])
            #https://pythontic.com/pandas/serialization/dictionary
            result = result_df.to_dict(orient="index")
            pprint(result)
            start_row += 5+1
        else:
            break
    print('-'*40, '\n')


def main():
    while True:
        city, month, day = get_filters()
        try:
            df = load_data(city, month, day)
        except:
            print('One or more of the filters are invalid. Shutting down.')
            break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
