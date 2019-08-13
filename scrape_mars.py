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

# empty dictionary for info to be added after each scrape
mars_info = {}


############################## NASA MARS NEWS ##############################
def scrape_mars_nasa_news():
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

        # add info to dictionary
        mars_info['news_title'] = news_title
        mars_info['news_p'] = news_p

        # return results
        return mars_info

    finally:
        # close browser
        browser.quit()

################## JPL MARS SPACE IMAGES - FEATURED IMAGE ##################
def scrape_mars_featured_image():
    try:
        # initial browser
        browser = init_browser()

        # store full and base urls
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        image_base_url = 'https://www.jpl.nasa.gov'

        # visit site
        browser.visit(image_url)

        # click on 'full image' to open the image in full
        browser.click_link_by_partial_text('FULL IMAGE')

        # scrape page into soup
        image_soup = bs(browser.html, 'html.parser')

        # store partial url
        img = image_soup.find('img', class_='fancybox-image')['src']

        # combine base url with partial url to get the featured_image_url
        featured_image_url = image_base_url + img

        # add info to dictionary
        mars_info['featured_image_url'] = featured_image_url

        # return results
        return mars_info

    finally:
        # close browser
        browser.quit()

############################### MARS WEATHER ###############################
def scrape_mars_weather_tweet():
    try:
        # initial browser
        browser = init_browser()

        # store full and base urls
        weather_url = 'https://twitter.com/marswxreport?lang=en'

        # visit site
        browser.visit(weather_url)

        # scrape page into soup
        weather_soup = bs(browser.html, 'html.parser')

        # store latest tweet
        latest_weather_tweet = weather_soup.find('p', class_='TweetTextSize').text

        # add info to dictionary
        mars_info['latest_weather_tweet'] = latest_weather_tweet

        # return results
        return mars_info

    finally:
        # close browser
        browser.quit()

################################ MARS FACTS ################################
def scrape_mars_facts_table():

    # store full url
    facts_url = 'https://space-facts.com/mars/'

    # reading html into a dataframe
    facts_table = pd.read_html(facts_url)

    # store only mars facts
    mars_table = facts_table[1]

    # renaming columns
    facts_mapping = {0:'Description', 1:'Value'}
    mars_table = mars_table.rename(columns=facts_mapping)

    # saving as html table format
    mars_facts_table = mars_table.to_html('mars_table.html', index=False)

    # add info to dictionary
    mars_info['mars_facts_table'] = mars_facts_table

    # return results
    return mars_info

############################# MARS HEMISPHERES #############################

