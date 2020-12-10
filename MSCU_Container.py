"""
    Title: Container_MSCU
    Author: Sunny Lee
    Description: This program scrapes container event data from MSCU's website
        and spits out an Excel file. Selenium is used for navigating the website.
        Pandas is used to sort and export data into Excel.

    Last Update: 1/30/2020


"""


import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

"""
    Splitting up previous main function
"""
def webscrape_options():
    print("wso-1: chrome_options")
    #Set up driver for webscraping
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    cwd = os.path.dirname(os.path.realpath(__file__))   #current directory
    
    #install if we need to
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except Exception as exc:
        print('%r generated an exception: %s' % (cntr, exc))

    return driver



def web_scrape(cntr_nbr, driver):

    driver.get('https://www.msc.com/track-a-shipment?agencyPath=usa')  #go to website

    time.sleep(15)

    #Subscribe
    popup_subscribe = driver.find_element_by_css_selector("#ctl00_ctl00_ucNewsetterSignupPopup_btnReject")
    popup_subscribe.click()
    time.sleep(2)


    #Cookies
    popup_cookies = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/button")
    popup_cookies.click()
    time.sleep(5)


    #Search
    search_box = driver.find_element_by_css_selector("#ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
    search_box.click()
    search_box.send_keys(cntr_nbr)
    search_button = driver.find_element_by_xpath("/html/body/form/div[4]/div/div[3]/main/div/div[1]/div/div/div[1]/div/div/div/div[2]/a/span")
    search_button.click()
    time.sleep(20)

    #Result table
    datatable =  driver.find_element_by_xpath("/html/body/form/div[4]/div/div[3]/main/div/div[2]/div/div/div[2]/dl/dd/div/dl/dd/div/table[2]")
    datatable_element = datatable.get_attribute('outerHTML')
    df = pd.read_html(datatable_element)
    df = df[0]

    #done with website, quit. 
    driver.quit()

    return(df)


def get_cntrlist():
    """
        Normally, webscraper will connect to SQL databases to pull containers we needed events for.
        Since this is a public repository, we'll be pulling from a pre-defined list.
        Please note, some of these containers might not be used anymore, and thus no data. 
    """

    cntrlst = ['MEDU5808268', 'MSCU7268922', 'MSCU9861623', 'MEDU7196520', 'TCLU5470670']
    
    return cntrlst



def main():
    """
        Get the list of containers we want to scrape, scrape them one by one and put them into excel. 
    """

    cntrlst = get_cntrlist() #get containers we want to scrape

    for cntr in cntrlst:
        print("Looking up ", cntr)

        driver = webscrape_options()

        #try to scrape that container information
        try:
            result = web_scrape(cntr, driver)
            result.to_excel("MSCU_Output.xlsx")
            print("Container ", cntr, " added to Excel"))
        
        except:
            print("Failed to scrape container ", cntr)




main()





