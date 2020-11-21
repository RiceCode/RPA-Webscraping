"""
    Title: MATS Schedule Bot
    Author: Sunny Lee
    Description: A simplified version of the Matson schedule webscraper.
                This program scrapes container schedule data from MATS website and prints it out.
                It does so by using Matson's unpublished API (which can be discovered by "insepct element" in the webpage. 
                Target website: https://www.matson.com/matnav/schedules/interactive_vessel_schedule.html
    Last Update: 11/16/2020


"""
import requests
from datetime import datetime, timedelta




def run_script(loadport,dischargeport):
    """
        Goes to carrier's website to gather data, and prints it out
    """

    #get the start date and end date
    startdate = datetime.today()
    enddate = startdate + timedelta(days=60)


    #change start date and end date into API call format
    startdateapi = startdate.strftime("%m%d%Y")
    enddateapi = enddate.strftime("%m%d%Y")

    #data used for API 
    url = "https://www.matson.com/wp-content/plugins//matson-plugin/Api_calls/search.php"
    data = {
        "selectedOrigin" : loadport,
        "selectedDestination" : dischargeport,
        "selectedStartDate" : startdateapi,
        "selectedEndDate" : enddateapi
    }

    #Get the data from the site
    r = requests.post(url, data=data)
    data = r.json()

    
    #Parse through the data
    for item in data:
        arrival = item['arrive']
        departure = item['depart']
        vessvoy = item['vessvoy'] #contains vessel + voyage
        vessel = vessvoy.split('*')[0] 
        voyage = vessvoy.split('*')[1]
        
        #format the dates so it can go into SQL database
        arrival = datetime.strptime(arrival, '%A %m/%d/%Y %H:%M')
        departure = datetime.strptime(departure, '%A %m/%d/%Y %H:%M')

        print("Vessel ", vessel, " will depart from ", loadport, " on ", departure, " and arrive at ", dischargeport, " on ", arrival)        







def main():
    """
        putting everything together
        get the load ports we need to scrape, loop through and scrape them all
    """
    print("Please enter the load port code. Example: XMN, SHA, or NGB")
    loadport = input()
    print("Please enter the discharge port code. Example: LAX, NORF")
    dischargeport = input() 

    run_script(loadport, dischargeport) 



main() 
