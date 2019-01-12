import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
isMonthSpecified = False
isDayOfWeekSpecified = False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print ('\n\nWhich of the below city data would you like to explore?')
    print ('Chicago, New York City, Washington')    

    while True:
        try:
            city = input('Type City name to begin: ')
            city = city.lower()
            CITY_DATA[city]
            break
        except KeyError:
            print ('Incorrect Entry, please try again')

    # TO DO: get user input for month (all, january, february, ... , june)
    print ('\n\nWhich of the below months are you interested in ?')
    print ('January, February, March, April, May, June or all')
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month = input('Type Month name to begin: ')
            month = month.lower()
            if month == 'all':
                break
            months.index(month)
            global isMonthSpecified
            isMonthSpecified = True
            break
        except ValueError:
            print ('Incorrect Entry, please try again')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print ('\n\nWhich of the below days would you like to look into ?')
    print ('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all')    
    while True:
        try:
            day = input('Type Day name to begin: ')
            day = day.lower()
            if day == 'all':
                break
            days.index(day.lower())
            global isDayOfWeekSpecified
            isDayOfWeekSpecified = True
            break
        except ValueError:
            print ('Incorrect Entry, please try again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])    

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int        
        month = months.index(month)
        month += 1
    
        # filter by month to create the new dataframe
        is_it_month = df['month']==month
        df = df[is_it_month]
        #print ('\nPrint:\n')
        #print (df.head())

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
    
        # filter by day to create the new dataframe
        is_it_day = df['day_of_week']==day
        df = df[is_it_day]
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    #print (df.head())
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if isMonthSpecified == False:
        # display the most common month
        df['month'] = df['Start Time'].dt.month
        #print (df['month'].value_counts().idxmax())
        most_common_month_index = df['month'].value_counts().idxmax()
        print (months[most_common_month_index-1].title(), 'is the most common month')

    if isDayOfWeekSpecified == False:
        # display the most common day of week
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        #print (df['day_of_week'].value_counts().idxmax())
        most_common_day_of_week_index = df['day_of_week'].value_counts().idxmax()
        print (days[most_common_day_of_week_index].title(), 'is the most common day of the week')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    #print (df['hour'].value_counts().idxmax())
    most_common_hour_index = df['hour'].value_counts().idxmax()
    print (most_common_hour_index, 'is the most common hour of the day')
    print ('\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station_index = df['Start Station'].value_counts().idxmax()
    print (most_common_start_station_index, 'is the commonly used Start Station')

    # display most commonly used end station
    most_common_end_station_index = df['End Station'].value_counts().idxmax()
    print (most_common_end_station_index, 'is the commonly used End Station')
    print ('\n')

    # display most frequent combination of start station and end station trip
    df = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'count'})
    #print(df['count'].head())
    most_common_start_end_station_index = df['count'].value_counts().idxmax()
    start_station = df.iloc[most_common_start_end_station_index, df.columns.get_loc("Start Station")]
    end_station = df.iloc[most_common_start_end_station_index, df.columns.get_loc("End Station")]
    print (start_station, '-', end_station, 'are the commonly used combination of Start and End Station')
    print ('\n')
    #print (most_common_start_end_station_index, ' is the commonly used Start-End Station')
    #print (df.iloc[most_common_start_end_station_index, df.columns.get_loc("Start Station")])
    #print (df.columns.get_loc("Start Station"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print (df['Trip Duration'].sum(), 'seconds is the total travel time')

    # display mean travel time
    print (df['Trip Duration'].mean(), 'seconds is the mean travel time')
    print ('\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #print (df.groupby(['User Type']).size().reset_index().rename(columns={0:'count'}))
    if 'User Type' in df:
        mod_df = df.groupby(['User Type']).size().reset_index().rename(columns={0:'count'})
        #print (mod_df.head())
        #column_loc = mod_df.columns.get_loc("User Type")
        #print (mod_df.iloc[0, column_loc], "are", mod_df.iloc[0, column_loc+1], "in number")
        #print (mod_df.iloc[1, column_loc], "are", mod_df.iloc[1, column_loc+1], "in number")

        for index, row in mod_df.iterrows():
            print(row['User Type'], "are", row['count'], "in number")
        print ('\n')
    
    # Display counts of gender
    if 'Gender' in df:
        mod_df = df.groupby(['Gender']).size().reset_index().rename(columns={0:'count'})
        #print (mod_df.head())
        #print (mod_df.iloc[0, column_loc], "are", mod_df.iloc[0, column_loc+1], "in number")
        #print (mod_df.iloc[1, column_loc], "are", mod_df.iloc[1, column_loc+1], "in number")
        for index, row in mod_df.iterrows():
            print(row['Gender'], "are", row['count'], "in number")
        print ('\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print (df['Birth Year'].min(), 'is the oldest person\'s year of birth')
        print (df['Birth Year'].max(), 'is the youngest person\'s year of birth')
        print (df['Birth Year'].value_counts().idxmax(), 'is the common person\'s year of birth')
        print ('\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        global isDayOfWeekSpecified
        isDayOfWeekSpecified = False
        global isMonthSpecified
        isMonthSpecified = False

        city, month, day = get_filters()
        #city = 'chicago'
        #month = 'all'
        #day = 'all'
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
