# RPA-Webscraping
Sample code to demonstrate gathering data from non-traditional data sources. In this case, from an ocean container shipping company. There's two types of webscraping demonstrated here. One is to use "hidden" API calls, and the other is to mimic user's input in the browser. 


## "Hidden" API Calls
MATS_Schedule uses "hidden" API calls to the carrier website to gather the vessel scheduled sailing data. The user will need to specify the load port and discharge port they want to search. The result is printed to the terminal. 
- requests
- datetime


## Browser Automation (to mimic user input)
MSCU_Container uses selenium to mimic a user going through a website, clicking search boxes etc to gather data. This script hardcoded a list of containers to demonstrate the browser automation. The result is outputted to an Excel file. 
Required packages:
- selenium
- pandas
- webdriver_manager
