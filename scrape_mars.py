################################## SET UP ##################################

# import dependencies
import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 

executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# empty dictionary for info to be added after each scrape
mars_info = {}

############################## NASA MARS NEWS ##############################
def scrape_mars_nasa_news():
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



################## JPL MARS SPACE IMAGES - FEATURED IMAGE ##################
def scrape_mars_featured_image():
        # store full and base urls
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        image_base_url = 'https://www.jpl.nasa.gov'

        # visit site
        browser.visit(image_url)

        # parse through html
        image_soup = bs(browser.html, 'html.parser')

        # previous attempt to click FULL IMAGE was having hiccups so tried to parse through style content
        partial_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # combine base url with partial url
        featured_image_url = image_base_url + partial_image_url

        # add info to dictionary
        mars_info['featured_image_url'] = featured_image_url

        # return results
        return mars_info



############################### MARS WEATHER ###############################
def scrape_mars_weather_tweet():
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
def scrape_mars_hemispheres():        
        # store full and base urls
        astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        astro_base_url = "https://astrogeology.usgs.gov"

        # visit url
        browser.visit(astro_url)
        astro_soup = bs(browser.html, 'html.parser')

        # creating empty lists to append scraped data
        hemi_image_list = []
        title_list = []
        url_list = []

        # loop through links and avoid two links that are the same
        div_list = astro_soup.find_all('a', class_='itemLink')
        for link in div_list:
            image_url = link.get('href')
            if image_url not in hemi_image_list:
                hemi_image_list.append(image_url)
                browser.visit(astro_base_url + image_url)
                title_list.append(browser.find_by_tag('h2').text)
                browser.find_link_by_text('Sample').click()
                
        for i in range(4,0,-1):
            url_list.append(browser.windows[i].url)
            
        # create list of hemisphere titles and hemisphere urls in dictionaries
        featured_hemisphere_list = [
            {'title': title_list[0], 'img_url': url_list[0]},
            {'title': title_list[1], 'img_url': url_list[1]},
            {'title': title_list[2], 'img_url': url_list[2]},
            {'title': title_list[3], 'img_url': url_list[3]}
            ]

        # add info to dictionary
        mars_info['mars_hemispheres'] = featured_hemisphere_list

        browser.quit()

        # return results
        return mars_info