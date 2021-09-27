#From AMIKEAL on GITHUB https://gist.github.com/amikeal/4e2847e3977a787e071e81014fe43390
from urllib.request import urlretrieve

#Checks for local file. If not found, it downloads it
try:
    f = open("local_copy.log")
except FileNotFoundError:
    #retrieves files and saves it locally
    local_file, headers = urlretrieve('https://s3.amazonaws.com/tcmg476/http_access_log', 'local_copy.log')
    print("File retrieved")
else:
    print("File exist")

count = 0
for line in open("local_copy.log"):
    count += 1

print("From 24/Oct/1994 until 11/Oct/1995 (the time period represented by the log), ", count ,"number of request were made")