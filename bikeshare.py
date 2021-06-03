import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# create an index of months for reference throughout the script
months_index = ['january', 'february', 'march', 'april', 'may', 'june','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # as each round of questions follows very similar logic, place user entry validation in loop
    # create tuple with loop inputs/outputs: valid input and question string for each category of city, month and day
    
    user_inputs = ((['chicago','new york city','washington'],str('Enter a city (Chicago, New York City, Washington): ')),
                   (months_index,str('Enter a month (January to June, or "all" for the whole period): ')),
                   (['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'],
                    str('Enter a day of the week (Monday to Sunday, or "all" for the whole week): ')))
    user_outputs = [0,0,0]
    i = 0
    while i < len(user_inputs):  
        valid_input,qn_string = user_inputs[i]  # unpack tuple of valid inputs and questions
        running = True
        while running:
            try:
                user_val = input(qn_string).lower()
                running = user_val not in valid_input  # keep running until user input is valid
                if running == False:
                    check = input('Fetching data for {} - is this correct? (Y/N)'.format(user_val.title()))
                    if check.lower() in ['y','yes']:  # confirms correct selection
                        user_outputs[i] = user_val
                        i += 1
                        break
                else:
                    print('Invalid entry - please try again')
            except KeyboardInterrupt:  # allow possibility for user to interrupt code
                x = input('Interrupted - enter any key to continue or "Y" to exit: ')
                if x.lower() in ['y','yes']:
                    i = 3
                    break
            else:
                running = True  # offer exit possibility if invalid user input is provided
                ex = input('Press any key to continue or "bye" to exit: ')
                if ex.lower() == 'bye':
                    i = 3
                    break
    city = user_outputs[0]  # write to variables
    month = user_outputs[1]
    day = user_outputs[2]
    print('')
    print("\n".join(["Fetching data for: {}".format(city.title()),"Month: {}".format(month.title()),"Day: {}".format(day.title())]))
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
    df = pd.read_csv(CITY_DATA[city.lower()])
        
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
            
    # extract month and day of week from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        month = months_index.index(month.lower()) + 1  # refer to pre-defined months_index, +1 due to zero indexing
        df = df[df['month'] == month]  # filter dataframe to selected month
            
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]  # filter dataframe to selected day
  
    return df

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel within user selection."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
           
    if month == 'all':
        # display the most common month
        month_mode = df['month'].mode()[0]
        print("The most popular month for travel is: {}.".format(months_index[month_mode-1].title()))
    else:
        # display the month selected
        print('Your selected month is: {}.'.format(month.title()))

    if day == 'all':
        # if all days selected:
        # use loop to display the most common day of week and the most common start hour
        i_range = [0,1]  # set range of tuple to be used in loop
    else:
        # if specific day selected, display selected day
        # use loop to display the most common start hour
        print('Your selected day is: {}.'.format(day.title()))
        i_range = [1]  # set range of tuple to be used in loop

    df['Hour'] = df['Start Time'].dt.strftime('%H')  # convert to 24h timeseries 
    # create tuple with loop inputs and outputs: filter variable, string output, error message if more than one mode
    time_inputs = (('day_of_week','The most popular day of week for travel is: {}.','day of week!'),
                   ('Hour','The most popular hour for travel is: {}00 hours.','hour!'))
    
    for i in i_range:  # calculate mode for day of week and hour
        time_filter,info_string,error_msg = time_inputs[i]  # unpack tuple
        mode_val = df[time_filter].mode()
        if len(mode_val) > 1:  # check if more than one most popular day or time for travel, then print all modes
            print(" ".join(["There is more than one most popular",error_msg,"They are:"]))
            countr = 1
            for vals in mode_val:
                print(" {}. {}".format(countr,vals))
                countr += 1
        else:
            print(info_string.format(mode_val[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # display most commonly used end station
    # display most frequent combination of start station and end station trip
    
    # create new column with all combinations of start and end station trip
    df['Trip'] = df['Start Station'] +' to ' + df['End Station']
    
    # create tuple with loop inputs and outputs: filter, output string and error message if more than one mode
    stn_inputs = (('Start Station','The most commonly used start station is: {}.','start station!'),
                  ('End Station','The most commonly used end station is: {}.','end station!'),
                  ('Trip','The most commonly used combination of start station and end station trip is: {}.','combination of start station and end station trip!'))
    # loop through all station stats
    for stn_input in stn_inputs:
        stn_filter,info_string,error_msg = stn_input  # unpack tuple
        mode_val = df[stn_filter].mode()
        if len(mode_val) > 1:  # check if more than one mode for the parameter of interest, then print all modes
            print(" ".join(["There is more than one most commonly used",error_msg,"They are:"]))
            countr = 1
            for vals in mode_val:
                print(" {}. {}".format(countr,vals))
                countr += 1
        else:
            print(info_string.format(mode_val[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
        
    # display total travel time
    trip_total = df['Trip Duration'].sum()
    print("Total travel time across your selections was {} seconds, or approximately {} days."
          .format(round(trip_total,2),int(trip_total//(3600*24))))
    
    # display mean travel time
    trip_mean = df['Trip Duration'].mean()
    print("Mean travel time across your selections was {} seconds, or approximately {} minutes."
          .format(round(trip_mean,2),int(trip_mean//60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    while True:
        try:
            # Display counts of user types
            count_user_types = df['User Type'].value_counts()
            print("Count of user types in your selection:")
            for i in range(0,len(count_user_types)):  # print user type and count of each type
                print("{}: {}".format(count_user_types.index[i],count_user_types[i]))
            nan_check = df['User Type'].isnull().sum()  # count the number of NaN values in this column
            if nan_check > 0:
                print("Note: There are {} missing datapoints which were not counted.".format(nan_check))
            print(' ')
            
            # Display counts of gender
            count_gender = df['Gender'].value_counts()
            print("Count of gender types in your selection:")
            for i in range(0,len(count_gender)):  # print gender type and count of each type
                print("{}: {}".format(count_gender.index[i],count_gender[i]))
            nan_check = df['Gender'].isnull().sum()  # count the number of NaN values in this column
            if nan_check > 0:
                print("Note: There are {} missing datapoints which were not counted.".format(nan_check))
            print(' ')
        
            # Display earliest, most recent, and most common year of birth
            birth_year_info = df['Birth Year'].describe()
            print("In your selection, the earliest and most recent year of birth are {} and {} respctively."
                  .format(int(birth_year_info.loc['min']),int(birth_year_info.loc['max'])))
            birth_year_mode = df['Birth Year'].mode()
            if len(birth_year_mode) > 1:
                print("There is more than one most common birth year in your selection! They are:")
                countr = 1
                for vals in birth_year_mode:
                    print(" {}. {}".format(countr,vals))
                    countr += 1
            else:
                print("{} is the most common year of birth in your selection.".format(int(birth_year_mode[0])))
            nan_check = df['Birth Year'].isnull().sum()
            if nan_check > 0:
                print("Note: There are {} missing datapoints which were not counted.".format(nan_check))
            break
        except KeyError:  # consider case where only user type data is available (eg. Washington)
            print("No other user stats are available.")
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw(df):
    """ Prints 5 lines of raw code"""
    
    n_row = 0
    viewData = input("Would you like to see the raw data? Type 'Yes' or 'No'.")
    if viewData.lower() in ("yes","y"):
        while n_row < len(df):  # print rows up to the end of the dataframe
            try:
                pd.set_option('display.max_columns', None)  # print all columns in code
                print(df.iloc[n_row:n_row+5])
                n_row += 5
                cont = input("Type 'Yes' to view the next 5 lines of data or 'bye' to exit: ")
                if cont.lower() in ("yes","y"):
                    continue
                else:
                    break
            except KeyboardInterrupt:
                x = input('Interrupted - enter any key to continue or "Y" to exit: ')
                if x.lower() in ['y','yes']:
                    break 

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            print_raw(df)
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ['yes','y']:
                break
        except (KeyError,AttributeError,IndexError):  # catch errors that may arise when user requests early exit
            print('-'*40)
            print("Thanks for exploring the data, have a nice day.")  # display exit message
            break
        except KeyboardInterrupt:
            x = input('Interrupted - enter any key to continue or "Y" to exit: ')
            if x.lower() in ['y','yes']:
                print('-'*40)
                print("Thanks for exploring the data, have a nice day.")  # display exit message
                break

if __name__ == "__main__":
    main()