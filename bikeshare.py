import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' }

Months = {
    'january', 'february', 'march', 'april',
    'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all'
}

days_of_week = {
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'
}

# Function to filter DataFrame by month name input
def filter_by_month_name(df, month_name, columnDate):
    # Extract month names from the datetime column
    month_name = month_name.capitalize()  # Ensure the input is correctly capitalized
    filtered_df = df[df[columnDate].dt.strftime('%B') == month_name]
    return filtered_df

# Function to filter DataFrame by day name input
def filter_by_day_name(df, day_name, columnDate):
    # Extract day names from the datetime column
    day_name = day_name.capitalize()  # Ensure the input is correctly capitalized
    filtered_df = df[df[columnDate].dt.strftime('%A') == day_name]
    return filtered_df

def load_data(city, month, day):
    file_data_city = pd.read_csv(CITY_DATA[city])
    df = pd.DataFrame(file_data_city)
    if month != 'All':
       df['Start Time'] = pd.to_datetime(df['Start Time'])
       df = filter_by_month_name(df, month, 'Start Time')

    if day != 'All':
       df['Start Time'] = pd.to_datetime(df['Start Time'])
       df = filter_by_day_name(df, day,'Start Time')
    return df

# Function to validate City input
def validate_City(city):
    if city in CITY_DATA:
        return True
    else:
        return False

# Function to validate month input
def validate_month(month):
    if month in Months:
        return True
    else:
        return False

# Function to validate day input
def validate_day_of_week(day):
    if day in days_of_week:
        return True
    else:
        return False

def get_filters():
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter City name:")
        if validate_City(city.lower()) == True:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter month name:")
        if validate_month(month.lower()) == True:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter day name:")
        if validate_day_of_week(day.lower()) == True:
            break
    
    return city.lower(), month, day

def time_stats(df):

    if df.empty:
        return False
    
    data_convert = pd.to_datetime(df['Start Time'])

    # most common month
    month = data_convert.dt.month.mode()

    # most common day of week
    day_of_week = data_convert.dt.day_name().mode()[0]

    # most common hour of day
    hour_of_day = data_convert.dt.hour.mode()[0]
    
    print(f"Most month = {month}:==> most day of week = {day_of_week}:==> most hour of day = {hour_of_day}")

def station_stats(df):

    if df.empty:
        return False
    
    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]

    df['trip'] = df['Start Station'] + ' TO ' + df['End Station']

    trip_counts = df['trip'].mode()[0]
    
    print(f"Most start station = {start_station}:==> most end station = {end_station}:==> most trip = {trip_counts} ")

def trip_duration_stats(df):

    if df.empty:
        return False
     
    # Convert 'start_time' and 'end_time' to datetime
    start_time = pd.to_datetime(df['Start Time'])
    end_time = pd.to_datetime(df['End Time'])

    # Calculate the duration for each trip
    df['duration'] = end_time - start_time

    #caculation total travel time
    total_duration = df['duration'].sum()

    #caculation mean travel time
    avg_duration = df['duration'].mean()

    print(f"total_duration = {total_duration}:==> avg_duration = {avg_duration}" )

def count_by_series(series):

    if series.empty:
        return False
    count_user_types = {}
    for user in series:
        if user in count_user_types:
            count_user_types[user] += 1
        else:
            count_user_types[user] = 1
    
    return count_user_types
def user_stats(df, city = None):

    if df.empty:
        return False
    #counts of each user type
    counts_user_type = count_by_series(df['User Type'])

    if city != 'washington':
        #counts of each gender (only available for NYC and Chicago)
        counts_user_gender = count_by_series(df['Gender'])

        #earliest, most recent, most common year of birth (only available for NYC and Chicago)
        birth_day = df['Birth Year']
        birth_day_earliest = birth_day.min()
        birth_day_recent = birth_day.max()
        most_year = birth_day.value_counts().idxmax()

        print(f"counts of each gender = {counts_user_gender}")
        print(f"birth_day_earliest = {birth_day_earliest}: birth_day_recent = {birth_day_recent}: most_year = {most_year} ")

    print(f"counts of each user type = {counts_user_type})")

# Function to display records in batches
def display_next_batch(df, start, batch_size):
    end_index = min(start + batch_size, len(df))
    if start >= len(df):
        print("No more rows to display.")
        return start
    
    print(df.iloc[start:end_index])
    return end_index

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print('No data matches the input condition')
        else:
            # Initialize index for slicing the DataFrame
            start_index = 0
            batch_size = 5
            while start_index < len(df):
                user_input = input("Do you go to access more data (YES/NO)?")
                if user_input.strip().upper() == 'YES':
                    start_index = display_next_batch(df, start_index, batch_size)
                else:
                    break

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
