################################## SET UP ##################################

# import dependencies
import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 

# initialize browser
def init_browser(): 
    executable_path = {'executable_path': '../chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

# dictionary imported into Mongo
mars_info = {}


############################## NASA MARS NEWS ##############################
def scrape_mars_news():
    try: 
        # initialize browser 
        browser = init_browser()

        # store full url
        news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

        # visit site
        browser.visit(news_url)

        # scrape page into soup
        news_soup = bs(browser.html, 'html.parser')

        # store title and headline
        news_title = news_soup.find_all('div', class_='content_title')[0].text
        news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text
        
        # return results
        return mars_info
    finally:
        # close browser
        browser.quit()

################## JPL MARS SPACE IMAGES - FEATURED IMAGE ##################

############################### MARS WEATHER ###############################

################################ MARS FACTS ################################

############################# MARS HEMISPHERES #############################

