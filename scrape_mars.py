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

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # more here

        return mars_info

    finally:

        browser.quit()
