#From AMIKEAL on GITHUB https://gist.github.com/amikeal/4e2847e3977a787e071e81014fe43390
from urllib.request import urlretrieve
import datetime


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

count = 0
for line in open("local_copy.log"):
    count += 1
print()
print("From 24/Oct/1994 until 11/Oct/1995 (the time period represented by the log),", count ,"number of request were made")
print()

#Request made in the last 6 months - apr 11 1995 to present
within_6mths = 0
count2 = 0
for line in open("local_copy.log"):
    split_string = line.split()

    if len(split_string) > 6 and (split_string[1] == split_string[2]):
        try:

            temp_string = split_string[3]
            
            temp_month_num = monthToNum(temp_string[4:7])
            

            #converted to ints becasue of random errors
            date_year = int(temp_string[8:12])
            date_month = int(temp_month_num)
            date_day = int(temp_string[1:3])
            date_check = datetime.datetime(date_year, date_month, date_day)
            if date_check<= date_6mth_ago_today:
                within_6mths += 1
        except:
            print(line)
    elif len(split_string) > 5:
        try:
            
            temp_string = split_string[3]
            
            temp_month_num = monthToNum(temp_string[4:7])
            

            #converted to ints becasue of random errors
            date_year = int(temp_string[8:12])
            date_month = int(temp_month_num)
            date_day = int(temp_string[1:3])
            date_check = datetime.datetime(date_year, date_month, date_day)
            if date_check<= date_6mth_ago_today:
                within_6mths += 1
        except:
            try:
            
                temp_string = split_string[2]
                
                temp_month_num = monthToNum(temp_string[4:7])

                #converted to ints becasue of random errors
                date_year = int(temp_string[8:12])
                date_month = int(temp_month_num)
                date_day = int(temp_string[1:3])
                date_check = datetime.datetime(date_year, date_month, date_day)
                if date_check<= date_6mth_ago_today:
                    within_6mths += 1
            except:
                pass


print ("Within the past 6 months from today, 11/Oct/1955, there were ", (within_6mths), " request excluding a few extranious request with no dates")
print ("")            

    
