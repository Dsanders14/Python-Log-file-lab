#From AMIKEAL on GITHUB https://gist.github.com/amikeal/4e2847e3977a787e071e81014fe43390
from sre_constants import CATEGORY
from urllib.request import urlretrieve
import datetime
import re
from collections import Counter


#converting the month abv to a number; from https://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
def monthToNum(shortMonth):
    return {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9, 
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
    }[shortMonth]

date_6mth_ago_today = datetime.datetime(1995, 4, 11)

#Checks for local file. If not found, it downloads it
try:
    f = open("local_copy.log")
except FileNotFoundError:
    #retrieves files and saves it locally
    local_file, headers = urlretrieve('https://s3.amazonaws.com/tcmg476/http_access_log', 'local_copy.log')
    print("Fetching file and adding it to data base")
else:
    print("File exist")

#Split for logfile lines
regex = re.compile("\[(\d{2})/([A-Za-z]{3,4})/(\d{4}):(\d{2}:\d{2}:\d{2}).+\] \"([A-Z]{3,6}) (.+) HTTP/1.0\" (\d{3}) .*")

#opens log file
file = open("local_copy.log")
content = file.readlines()

#vars declared
Monday = 0
Tuesday = 0
Wednesday = 0
Thursday = 0
Friday = 0
Saturday = 0
Sunday = 0

count = 0
elsewhere_count = 0
not_successful = 0
not_successful_percent = 0
elsewhere_count_percent = 0

requested_files = {}

week_old_number = 0
week_new_number = 0
week_request_count = 0
week_print_list = []

month_old_number = 0
month_new_number = 0
month_request_count = 0
month_print_list = []

log_month_list = []

onetime = 0
onetime_month = 10


print("Please wait...")
print("")
print("")
print("Part 1:")

#loops through each line
for line in open("local_copy.log"):
    parts = regex.split(line)
    
    #checks to ensure the line isnt an extranious line
    if len(parts) > 8:
        #Total count
        count += 1
        #PT. 1: checking date
        temp_month_num = monthToNum(parts[2])
        date_year = int(parts[3])
        date_month = int(temp_month_num)
        date_day = int(parts[1])
        date_complete = datetime.datetime(date_year, date_month, date_day)
        #grabbing day of the week number to check for date
        day_Number = date_complete.weekday()
        if day_Number == 0:
            Monday += 1
        elif day_Number == 1:
            Tuesday += 1
        elif day_Number == 2:
            Wednesday += 1
        elif day_Number == 3:
            Thursday += 1
        elif day_Number == 4:
            Friday += 1
        elif day_Number == 5:
            Saturday += 1
        elif day_Number == 6:
            Sunday += 1

        #PT.2 Week by Week
        #get the first date one time
        if onetime == 0:
            week_old_number = datetime.date(date_year, date_month, date_day).isocalendar()[1]
            onetime = 1

        #if same, still the same week
        week_new_number = datetime.date(date_year, date_month, date_day).isocalendar()[1]
        if week_old_number == week_new_number:
            week_request_count +=1
        #if different, week has changed
        else:
            tempstring3 = "Week "+ str(week_old_number) + " of " +  str(date_year) + " contained " + str(week_request_count) + " requests"
            week_print_list.append(tempstring3)
            week_request_count = 0
            week_old_number = week_new_number


        #PT.3 Month by Month (set up the same as week above)
        #get the first date one time
        if onetime == 0:
            month_old_number = date_month
            onetime = 1

        month_new_number = date_month
        if month_old_number == month_new_number:
            month_request_count +=1
            log_month_list.append(line)
        elif month_old_number == 0:
            month_old_number = month_new_number
        else:
            tempstring2 = "Month " + str(month_old_number) + " of " + str(date_year) + " contained " + str(month_request_count) + " requests"
            month_print_list.append(tempstring2)
            month_request_count = 0
            month_old_number = month_new_number
            #SPLITTING MY MONTH AND ADDING TO A NEW FILE
            filename = "%(2)s_Month_%(1)s_log.txt" % {"1" :date_month, "2": date_year}
            filehandle = open(filename, 'w')
            for listitem in log_month_list:
                filehandle.write(f"{listitem}\n")




        #PT.3 & 4 Request not successful or from elsewhere
        if parts[7].startswith('4'):
            not_successful += 1
        elif parts[7].startswith('3'):
            elsewhere_count += 1

        #PT. 5: checking the number of times each file is called
        #if it exist, we add one, if not we set the file to 1 in a dict
        if parts[6] in requested_files:
            requested_files[parts[6]] += 1
        else:
            requested_files[parts[6]] = 1



#counting least requested
least_requested = 0
for key in requested_files.values():
    if key == 1:
        least_requested += 1


#getting most requested file
most_requested = Counter(requested_files)
temp = most_requested.most_common(1)

#Getting elements from the most requested file for print
regex2 = re.compile("'(.*)', (\d.*)")
str1 = ""
for ele in temp:
    str1 += str(ele)
parts2 = regex2.split(str1)
tempstring = parts2[2]
templength = len(tempstring)
shortened = tempstring[:templength-1]



not_successful_percent = not_successful/count
elsewhere_count_percent = elsewhere_count/count

#printing all information
print("")
print("")
#PT. 1
print("Part 1:")

print("Files printed for each day of the week:")
print("Monday:",Monday)
print("Tuesday:", Tuesday)
print("Wednesday:", Wednesday)
print("Thursday:", Thursday)
print("Friday:", Friday)
print("Saturday:", Saturday)
print("Sunday:",Sunday)
print("")

print("")
print("")
#PT. 2
print("Part 2:")
for item in week_print_list:
    print(item)
print("")
print("")
print("")
for item in month_print_list:
    print(item)
print("")
print("")
#PT. 3 & 4
print("Part 3 & 4:")

print(not_successful, "request or %.2f percent" % not_successful_percent, "were not successful")
print(elsewhere_count, "request or %.2f percent" % elsewhere_count_percent, "were redirected elsewhere")
print("")
#PT.5
print("")
print("Part 5:")
print("The most requested file was", parts2[1] ,"and was requested", shortened , "times")
#PT.6
print("")
print("Part 6:")
print("There were", least_requested, "files that were requested only one time making them tied for the least requested file")
print("(not printing the names of each file to keep the print looking clean)")
print("")
print("")
#Extra part
print("The log has been broken up my months and added to your local files")
print("")
print("") 






#
#
#print("The least requested files were:")
#for key, val in requested_files:
#    if val == 1:
#        print(requested_files[key])
#        



#for line in open("local_copy.log"):










#CODE FROM FIRST PART (INEFFICIENT)

#count = 0
#for line in open("local_copy.log"):
#    count += 1
#print()
#print("From 24/Oct/1994 until 11/Oct/1995 (the time period represented by the log),", count ,"number of request were made")
##print()
#
##Request made in the last 6 months - apr 11 1995 to present
#within_6mths = 0
#count2 = 0
#for line in open("local_copy.log"):
#    split_string = line.split()
#
#    if len(split_string) > 6 and (split_string[1] == split_string[2]):
#        try:
#
#            temp_string = split_string[3]
#            
#            temp_month_num = monthToNum(temp_string[4:7])
#            
#
#            #converted to ints becasue of random errors
#            date_year = int(temp_string[8:12])
#            date_month = int(temp_month_num)
#            date_day = int(temp_string[1:3])
#            date_check = datetime.datetime(date_year, date_month, date_day)
#            if date_check<= date_6mth_ago_today:
#                within_6mths += 1
#        except:
#            print(line)
#    elif len(split_string) > 5:
#        try:
#            
#            temp_string = split_string[3]
#            
#            temp_month_num = monthToNum(temp_string[4:7])
#            
#
#            #converted to ints becasue of random errors
#            date_year = int(temp_string[8:12])
#            date_month = int(temp_month_num)
#            date_day = int(temp_string[1:3])
#            date_check = datetime.datetime(date_year, date_month, date_day)
#            if date_check<= date_6mth_ago_today:
#                within_6mths += 1
#        except:
#            try:
#            
#                temp_string = split_string[2]
#                
#                temp_month_num = monthToNum(temp_string[4:7])
#
#                #converted to ints becasue of random errors
#                date_year = int(temp_string[8:12])
#                date_month = int(temp_month_num)
#                date_day = int(temp_string[1:3])
#                date_check = datetime.datetime(date_year, date_month, date_day)
#                if date_check<= date_6mth_ago_today:
#                    within_6mths += 1
#            except:
#                pass
#
#
#print ("Within the past 6 months from today, 11/Oct/1955, there were ", (within_6mths), " request excluding a few extranious request with no dates")
#print ("")            
#
#    
#