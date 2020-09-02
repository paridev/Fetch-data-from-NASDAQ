# import sys
import json, requests, os, csv, time, subprocess
from datetime import date, timedelta
from tkinter import filedialog
from tkinter import *

print("Please enter the year:")

my_date = input()
if my_date == "":

    print("hoooooooooooooo hoo ho There is no date and we can not support anymore")

else:
    root = Tk()
    root.directory =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
    file_path = root.directory +"/" +my_date + ".csv"
    file_path.replace("/", "\\", -1)
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'x') as csvfile:        
        api_token = 'your_api_token'
        my_url = "https://api.nasdaq.com/api/calendar/earnings?date="
        sdate = date(int(my_date), 1, 1)   # start date
        if my_date == "2020":
            edate= date.today()
        else:
            edate = date(int(my_date), 12, 30)   # end date
        delta = edate - sdate       # as timedelta
        one_time_header = True
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            print(day)
            api_url_base = my_url + str(day)
            api_url = '{0}'.format(api_url_base)
            response = requests.get(api_url)
            r = json.loads(response.content.decode('utf-8'))
            data = r["data"]            
            if data["headers"] == None:
                continue
                
            else:
                headers = data["headers"]
                headers["date"] = "Date"                
                rows = data["rows"]
                w = csv.DictWriter(csvfile, fieldnames=headers)
                if one_time_header:
                    w.writeheader()
                    one_time_header = False
                csvfile.write("\n")
                len_rows = len(rows)
                for i in range(len_rows):     
                    w.writerow(rows[i])
                    csvfile.write(str(day))
                    csvfile.write("\n")
                    time.sleep(0.005)
    csvfile.close
