import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def load_data(city):
    data_city = pd.read_csv(city)
    df = pd.DataFrame(data_city)
    return df

def time_stats(df):

    data_convert = pd.to_datetime(df['Start Time'])

    # most common month
    month = data_convert.dt.month.value_counts().idxmax()

    # most common day of week
    dayOfweek = data_convert.dt.day_name().value_counts().idxmax()

    # most common hour of day
    hourOfday = data_convert.dt.hour.value_counts().idxmax()
    
    return month, dayOfweek, hourOfday

def station_stats(df):
    start_station = df['Start Station'].value_counts().idxmax()
    end_station = df['End Station'].value_counts().idxmax()

    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    trip_counts = df['trip'].value_counts().idxmax()
    
    return start_station, end_station, trip_counts

def trip_duration_stats(df):
     
    # Convert 'start_time' and 'end_time' to datetime
    start_time = pd.to_datetime(df['Start Time'])
    end_time = pd.to_datetime(df['End Time'])

    # Calculate the duration for each trip
    df['duration'] = end_time - start_time

    total_duration = df.groupby(['Start Time','End Time'])['duration'].sum()

    avg_duration = df.groupby(['Start Time','End Time'])['duration'].mean()

    return total_duration, avg_duration

def user_stats(series, birthday = None):

    if birthday != None:
        birth_day = series
        birth_day_earliest = birth_day.min()
        birth_day_recent = birth_day.max()
        most_year = birth_day.value_counts().idxmax()
        return birth_day_earliest, birth_day_recent, most_year
    
    count_user_types = {}
    for user in series:
        if user in count_user_types:
            count_user_types[user] += 1
        else:
            count_user_types[user] = 1

    return count_user_types

def main():
    for key, city in CITY_DATA.items():
        df = load_data(city)

        #1 Popular times of travel
        month, dayOfweek, hourOfday = time_stats(df)
        print(f"CITY = {key}: ==== Most month = {month}: most day of week = {dayOfweek}: most hour of day = {hourOfday}")

        #2 Popular stations and trip
        start_station, end_station, trip_counts = station_stats(df)
        print(f"CITY = {key}: ==== Most start station = {start_station}: most end station = {end_station}: most trip = {trip_counts} ")

        #3 Trip duration
        total_duration, avg_duration = trip_duration_stats(df)
        print(f"CITY = {key}: ==== total_duration = {total_duration}: avg_duration = {avg_duration}" )

        #4 User info
        count_user_types = user_stats(df['User Type'])
        print(count_user_types)

        if key != "washington":
            gender_count = user_stats(df['Gender'])
            print(gender_count)

            birth_day_earliest, birth_day_recent, most_year = user_stats(df['Birth Year'], birthday=key)
            print(f"CITY = {key}: birth_day_earliest = {birth_day_earliest}: birth_day_recent = {birth_day_recent}: most_year = {most_year} ")

if __name__ == "__main__":
	main()
