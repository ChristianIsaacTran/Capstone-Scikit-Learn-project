#note: I had to setup my own virtual environment in python and allow this computer to be able
#      to run scripts. I changed the user's permissions in windows admin powershell manually.
#import pandas
import pandas as pd

#import date time??? as dt
import datetime as dt

from scipy.stats import pearsonr

#Pull .csv file from online link to practice pulling data every 3 months
df = pd.read_csv('https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/people/people-10000.csv')

#making a temp data frame to test counting unique names:
#data = {'Date of birth': ['1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-08-11', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10', '1938-11-10'],    
#'First Name': ['John', 'IUN', '00A', '0BA', 'IUN', 'BRO', 'GET', 'BRO', 'BRUH', '00A', 'John', 'IUN', '00A', '0BA', 'IUN', 'BRO', 'GET', 'BRO', 'BRUH', '00A' ],
#'Index':[500, 100, 23, 444, 51, 233, 1023, 46, 934, 10, 500, 100, 23, 444, 51, 233, 1023, 46, 934, 10]}
#df = pd.DataFrame(data) #making it a temporary dataframe to test this case:

#Test display to see if I read the .csv file correctly and stored into a dataframe correctly.
#print(dataframe)

#Check to see if date column is a datetime object
#print(df.dtypes)

#drop unrelated columns to only have numerical data:
#df = df.drop('User Id', axis=1)
#df = df.drop('Last Name', axis=1)
#df = df.drop('Sex', axis= 1)
#df = df.drop('Phone', axis = 1)
#df = df.drop('Email', axis = 1)
#df = df.drop('Job Title', axis = 1)

#Convert the date column into a datetime object to be used to manipulate datetime
df['Date of birth'] = pd.to_datetime(df['Date of birth'])

#Check datatype again of the date column
#print(df.dtypes)

#check df.dtypes again
#print(df.dtypes)

#Check to see if the datetime object got converted into correct format
#print(df)
#print(df['Date of birth'].dt.day)
#print(df['Date of birth'].dt.month)
#print(df['Date of birth'].dt.year)



#Try to sort the dates by year first before trying to pull data every month
df = df.sort_values(by='Date of birth') #first, try using the sort_values function to sort the dates by the date column
#print('------- TESTING -------')
#print(df) #df has been sorted by the soonest date to the most current date
#print(df.head(20))

#We get the start_date by just looking at the first record in the .csv file, and we get the end_date by
#using jake gonzales recommendation which is datetime.timedelta()

#-----------------------------------------This Section makes the 3 month mask, starting with the date on the first record--------------------------------------------
#ATTEMPTING TO MAKE A THING THAT CAN ITERATE THROUGH THE DATA EVERY 3 MONTHS FROM A START DATE
Original_start_date = pd.to_datetime('1906-05-31') #For display testing
starting_date = pd.to_datetime(df['Date of birth'].iloc[0]) #Get the starting date from the first record (the first row) from the dataframe and make it a datetime64 object
#print("iloc starting date:::::::")
#print(starting_date)
#3 months = around 90~ or 91 days
end_date = starting_date + dt.timedelta(days = 91) #calculate the future date/end_date by adding a dt.timedelta of 90 days
Original_end_date = end_date #For display testing

print("Starting date:")
print(starting_date)
print("New end date detected:")
print(end_date)

mask = (df['Date of birth'] >= starting_date) & (df['Date of birth'] < end_date) #starting_date is inclusive, end_date is exclusive because we plan to start at the new_starting_date (which is the end_date) on next iteration

df_every_3_months = df.loc[mask] #make a new dataframe that only contains the data from the 3 months

#print('--------test for 3 month mask ----------------')
#print(df_every_3_months)
#-----------------------------------------This section attempts to sum up all the columns (# of flights, # of landings, # of flight hours) for the FIRST 3-month interval--------------------------------------------
#Tally up the sum of the index 
array_of_index_counts = []
Total_sum_index = df_every_3_months['Index'].sum() #Sums up the Index column with .sum()
#print('Total sum of the indexes within 3 month interval: '+ str(Total_sum_index))
array_of_index_counts.append(Total_sum_index) #add the total_sum_index to the end of the list


#-----------------------------------------This section identifys all the unique names in a certain column, then counts all the appearances of each name for the FIRST 3-month interval--------------------------------------------
#Tally up the number of unique names show up:
#oliver came up with using numpy to assign all the unique names in a dictionary
#Im going to try a different method to tally up unique names
#first, make a list of all the unique names for indexing:
list_of_unique_names = df['First Name'].unique().tolist() #list of unique names with the .tolist()
#print(list_of_unique_names)
list_of_unique_names_counts = [] #Use the list_of_unique_names to index where to put the count values in this other array

#First, run through the unique # of names and add lists to list_of_unique_names_coutns to make a list of lists of equal length:
for j in list_of_unique_names:
    list_of_unique_names_counts.append([]) 

#Test display 
#print(list_of_unique_names_counts)
#print("length of both lists:") 
#print(len(list_of_unique_names))
#print(len(list_of_unique_names_counts))

#iterate through the list of names to count them and assign them to their appropriate index in the other list:
for i in list_of_unique_names:
    if (df_every_3_months['First Name'] == i).any(): #If the current unique name shows up at all in the current 3_month_interval, then count it
        count_of_current_unique_name = df_every_3_months['First Name'].value_counts()[i]
    else: #if the current unique name does not show up at all in the current 3_month_interval, then set the count to 0 because its not in this interval
        count_of_current_unique_name = 0

    #Add whatever the count is for the unique name into the index of the unique name    
    list_of_unique_names_counts[list_of_unique_names.index(i)].append(count_of_current_unique_name) #Assign the count variable to the index of the current unique name

#Test display
#print(list_of_unique_names_counts)


#-----------------------------------------This while loop gets the rest of the sum data in 3 month intervals for the rest of the dataset--------------------------------------------
flag = True #flag for the while loop #changed to false, turn back to true to activate while loop
while(flag != False):

    starting_date = end_date #make the new starting date the end date 

    end_date = starting_date + dt.timedelta(days = 91) #Calculate new end_date from the updated starting date

    #Test display for updated starting and ending date values
    #print("New Starting date:")
    #print(starting_date)
    #print("New end date detected:")
    #print(end_date)


    mask = (df['Date of birth'] >= starting_date) & (df['Date of birth'] < end_date) #starting_date is inclusive, end_date is exclusive because we plan to start at the new_starting_date (which is the end_date) on next iteration

    df_every_3_months = df.loc[mask] #Make a new dataframe based off of the original dataframe, but with the 3 month mask on it.
    
    #Test display for the data that was gathered within that time frame
    #print('--------test for 3 month mask ----------------')
    #print(df_every_3_months)
    #print("Amount of Rows: "+ str(len(df_every_3_months)))
    #print('----------------------------------------------')


    if df_every_3_months.empty: #if the dataframe is empty (there are no more rows that I can get from the time interval), then make flag false
        flag = False
        break

    #For every df_every_3_months, tally up the sum of all indexes (# of flight hours and # of landings) and tally up the number of times unique first names appear (# maintenance actions)
    # (# of flights for the flight dataframe can just be totaled by counting how many rows are in this time interval, so len(df_every_3_months) should be fine)

    #sum up the total index
    Total_sum_index = df_every_3_months['Index'].sum() #Sums up the Index column with .sum()
    array_of_index_counts.append(Total_sum_index) #add the total_sum_index to the end of the list

    #count the amount of times the unique names appear in every 3 month interval:
    #iterate through the list of names to count them and assign them to their appropriate index in the other list:
    for i in list_of_unique_names:
        if (df_every_3_months['First Name'] == i).any(): #If the current unique name shows up at all in the current 3_month_interval, then count it
            count_of_current_unique_name = df_every_3_months['First Name'].value_counts()[i]
        else: #if the current unique name does not show up at all in the current 3_month_interval, then set the count to 0 because its not in this interval
            count_of_current_unique_name = 0

        #Add whatever the count is for the unique name into the index of the unique name    
        list_of_unique_names_counts[list_of_unique_names.index(i)].append(count_of_current_unique_name) #Assign the count variable to the index of the current unique name


#Starting and Final dates
print("\n\nOriginal Starting date:")
print(Original_start_date)
print("Original end date:")
print(Original_end_date)
print("Final Starting date:")
print(starting_date)
print("Final end date detected:")
print(end_date)

#test display for the unique names (# of unique names of maintenenace actions to index into unique names counts) and unique names counts (# of maintenance actions), and the array of index counts (# of flights, # of landings, # of flight hrs)
#print(list_of_unique_names)
#print(list_of_unique_names_counts)
#print(array_of_index_counts)

#Test display for the lengths of every list:
#print(len(list_of_unique_names)) #list_of_unique names is used for indexing the list_of_unique_names_counts
#for i in list_of_unique_names_counts: #Since list_of_unique names is a list of lists, print out the length of every inner list
    #print("Length of inner array of list_of_unique_names_counts: "+ str(len(i)))
print("Length of unique_name_counts (every list should be the same length since they're all using the same time inteval): " +str(len(list_of_unique_names_counts[0])))
print("Length of array of index counts: "+ str(len(array_of_index_counts)))


#-----------------------------------------This section takes all of the lists of every feature we want to compare (# of flights, # of landings, # of flight hours, # of maintenance actions) and makes correlation score list for each case--------------------------------------------

#Now that we have our arrays, test to see if I can do the correlation scores between them since they are all equal length

#list to store correlation scores of case1.
# case 1 is:
#   list_of_unique_names_counts[i] (# of maintenance actions) vs. array_of_index_counts (# of flight hours, or # of flights, or # of landings)
list_of_case1_correlation = [] #list to store correlation scores of case1.

#Test to see if pearsonr correlation scores work
corr, p_val = pearsonr(array_of_index_counts, list_of_unique_names_counts[0])
print("This is the correlation score: "+str(corr)) #display correlation score
print("This is the p_val: "+str(p_val)) # We dont need the p_val (as far as I know) for now. Ignore.

#Make correlation scores for ALL unique names for ALL cases by iterating through the list and store the correlation scores for this specific case into list_of_case1_correlation:
for current_unique_name in list_of_unique_names_counts: #current_unique_name is also the WUC names
    corr, p_val = pearsonr(array_of_index_counts, current_unique_name)
    list_of_case1_correlation.append(corr) #because we only care about the correlation score

#test display
#print(list_of_case1_correlation)
print("This is the list_of_case1 length: "+str(len(list_of_case1_correlation)))
print("This is the number of UNIQUE NAMES: "+str(len(list_of_unique_names)))
#note: the length of the list_of_case1_correlation changes depending on the number of unique names there are.

#after generating a list of all of the correlation scores for a specific case, make a new list of tuples??? or lists??? that associates the unique_name with the correlation score for the case
combined_list_of_unique_names_with_their_correlation_scores = [] #combines both lists and makes a list of lists (or a list of tuples?) that associate each unique name with their correlation score for case1

for i in range(len(list_of_unique_names)):
    #make a tuple with unique names, WITH their correlation value and add that tuple to the combined_list_of_unique_names_with_their_correlation_scores
    combined_tuple = (list_of_unique_names[i], list_of_case1_correlation[i])
    combined_list_of_unique_names_with_their_correlation_scores.append(combined_tuple)


#Then, display the final list of names with their correlation scores:

for i in combined_list_of_unique_names_with_their_correlation_scores:
    print(i)
