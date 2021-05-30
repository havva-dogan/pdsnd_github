import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = [ 'chicago', 'new york city', 'washington']
months = [ 'january', 'february', 'march', 'april', 'may', 'june','all']
days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    city = input("Would you like to see data for Chicago, New York City, or Washington?\n")
    city = city.lower()
    while city not in cities:
        print("Please enter a valid input")
        city = input("Would you like to see data for Chicago, New York City, or Washington??\n")
        city = city.lower()
    
    month = input("Would you like to see data for which month? January, February, March, April, May or June? \n")
    month = month.lower()
    while month not in months:
        print ("Please enter a valid month")
        month = input("Would you like to see data for which month? January, February, March, April, May or June? \n")
        month = month.lower()
        
    day = input("Would you like to see data for which day?\n")
    day = day.lower()
    while day not in days:
        print ("Please enter a valid day")
        day = input("Would you like to see data for which day?\n")
        day = day.lower()
        
    print('-'*50)
    return (city, month, day)
            
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    
     """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if 'Start Time' in df.columns:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        most_common_month_idx = df['month'].mode()[0]
        most_common_month = months[most_common_month_idx-1]
        print('Most Common month is {}.'.format(most_common_month))
        
        df['day_of_week'] = df['Start Time'].dt.day_name()
        most_common_day = df['day_of_week'].mode()[0]
        print('Most Common day is {}.'.format(most_common_day))
        
        df['hour'] = df['Start Time'].dt.hour
        most_common_hour = df['hour'].mode()[0]
        print('Most Common hour is {}.'.format(most_common_hour))
        
        print('\nThis took {} seconds.\n'.format(time.time()-start_time))
        print('-'*50)
        
def station_stats(df):
    
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    most_common_start_station = str(df['Start Station'].mode()[0])
    print (most_common_start_station)
        
    most_common_end_station = str(df['End Station'].mode()[0])
    print (most_common_end_station)
    
    df['Start End Combination'] = (df['Start Station'] + '&' +df['End Station']) 
    most_common_start_end_combination = str(df['Start End Combination'].mode()[0])
    print (most_common_start_end_combination)
    
    print('\nThis took {} seconds.\n'.format(time.time()-start_time))
    print('-'*50)
    
def trip_duration_stats(df):
    
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {} seconds'.format(total_travel_time))
    
    average_travel_time = df['Trip Duration'].mean()
    print ('The average travel time is {} seconds'.format(average_travel_time))
    
    print('\nThis took {} seconds.\n'.format(time.time()-start_time))
    print('-'*50)

        


def user_stats(df):
     """Displays statistics on bikeshare users. 
        counts of each user type
        counts of each gender (only available for NYC and Chicago)
        earliest, most recent, most common year of birth (only available for NYC and Chicago)"""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())
        
    try:        
        if 'Gender' in df.columns:
            print(df['Gender'].value_counts())
        
    except:
        print("There is no gender data for the selected city.")
    
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        
        most_recent_year = df['Birth Year'].max()
        
        most_common_year = df['Birth Year'].mode()[0]
    
    print('\nThis took {} seconds.\n'.format(time.time()-start_time))
 

        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city,month,day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        answer = input('Would you like to see raw data? Please write Yes or No.\n')
        answer = answer.lower()
        row = 0
        while answer == 'yes':
            
            print (df.iloc[row:row+5,:])
            
            answer = input('Would you like to see more raw data? Please write Yes or No.\n')
            answer = answer.lower()
            row += 5
     
        restart = input("Would you like to restart? Please write Yes or No.\n")
        restart = restart.lower()
        if restart != 'yes':
            break
        
if __name__ == "__main__":
                       main()

