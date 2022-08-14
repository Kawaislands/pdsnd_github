import time
import pandas as pd
import numpy as np
import json

#Refactor1
#Refactor2


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


class text():
    def spin(self, string, num):
        self.clear = "\b" * (8 + len(string))
        for _ in range(num):
            for ch in '-\\|/':
                print('__' + '(' + ch + ')' + string + '(' + ch +
                      ')' + '_', end='', flush=True)
                time.sleep(0.1)
                print(self.clear, end='', flush=True)


def print_spin(message, num):
    fido = text()
    fido.spin(message, num)


def get_filters():
    print('\n')
    print_spin('Bikeshare', 8)
    print('_(/)Bikeshare(/)______________________________')
    print(' Hello! Let\'s explore some US bikeshare data! '.center(78, '='))

    city = None
    city_filter = ['chicago', 'new york', 'washington']
    while city not in city_filter:
        city = input("\nFilter data by city\n[ Chicago, "
                     "New York or Washington ] : ").lower()

    month = None
    month_filter = ['all', 'january', 'february', 'march',
                    'april', 'may', 'june']
    while month not in month_filter:
        month = input("\nFilter data by month\n[ all, january, february,"
                      "march, april, may, or june ] : ").lower()

    day = None
    day_filter = ['all', 'sunday', 'monday', 'tuesday',
                  'wednesday', 'thursday', 'friday', 'saturday']
    while day not in day_filter:
        day = input("\nFilter data by day of the week\n['all', "
                    "'sunday', 'monday', ...., 'saturday'] : ").lower()

    print('-' * 78, '\n')
    return city, month, day


def load_data(city, month, day):
    print()
    print(" Filters applied : "
          "[ {}, {}, {}] ".format(city, month, day).center(78, '*'))
    print()

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    if 'Start Time' in df.columns:
        print()
        print(' Calculating The Most Frequent Times '
              'of Travel '.center(78, '='))
        start_time = time.time()
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month

        popular_month = df['month'].mode()[0]
        print('Most common Month'.ljust(40, '.'), popular_month)
        df['day_of_week'] = df['Start Time'].dt.day_name()

        popular_day = df['day_of_week'].mode()[0]
        print('Most common day of the week'.ljust(40, '.'), popular_day)
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most common Start Hour'.ljust(40, '.'), popular_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 78, '\n')


def station_stats(df):
    print()
    print(' Calculating The Most Popular Stations and Trip '.center(78, '='))
    start_time = time.time()
    print(' Station Stats '.center(78, '-'))
    if 'Start Station' in df.columns:
        print('Most commonly used Start '
              'station '.ljust(40, '.'), df['Start Station'].mode()[0])

    if 'End Station' in df.columns:
        print('Most commonly used End '
              'station '.ljust(40, '.'), df['End Station'].mode()[0])

    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -> ' + df['End Station']
        print('Most frequent route '.ljust(40, '.'), df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 78, '\n')


def trip_duration_stats(df):
    print()
    if 'Trip Duration' in df.columns:
        print(' Calculating Trip Duration '.center(78, '='))
        start_time = time.time()

        print(' Trip Duration stats '.center(78, '-'))
        print('Max Travel Time '.ljust(40, '.'), df['Trip Duration'].max())
        print('Min Travel Time '.ljust(40, '.'), df['Trip Duration'].min())

        print('Avg Travel Time '.ljust(40, '.'), df['Trip Duration'].mean())
        print('Most Travel '
              'Time '.ljust(40, '.'), df['Trip Duration'].mode()[0])

        print('Total Travel Time '.ljust(40, '.'), df['Trip Duration'].sum())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 78, '\n')


def user_stats(df):
    print()
    print(' Calculating User Stats '.center(78, '='))
    start_time = time.time()

    if 'User Type' in df.columns:
        print(' User type stats '.center(78, '-'))
        print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print(' Gender stats '.center(78, '-'))
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))

    if 'Birth Year' in df.columns:
        print(' Age stats '.center(78, '-'))
        print('Earliest Birth '
              'Year '.ljust(40, '.'), int(df['Birth Year'].min()))
        print('Most recent Birth '
              'Year '.ljust(40, '.'), int(df['Birth Year'].max()))
        print('Most common Birth '
              'Year '.ljust(40, '.'), int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 78, '\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        row = 5
        raw_data = input('Would you like to see raw data? '
                         'Enter (yes / no) : ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        while raw_data == 'yes':
            print(json.dumps(df.head(row).to_dict('index'), indent=1))
            raw_data = input('Would you like to see more '
                             'raw data? Enter (yes / no) : ').lower()
            row += 5

        restart = input('\nWould you like to restart? '
                        'Enter (yes / no) : ').lower()
        if restart.lower() != 'yes':
            print()
            print(' Python Script Terminated '.center(78, '*'))
            print()
            break


if __name__ == "__main__":
    main()