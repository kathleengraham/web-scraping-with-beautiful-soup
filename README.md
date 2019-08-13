# <h1 align='center'>Web Scraping with Beautiful Soup</h1>


## Web Scraping Objective

Scrape the following websites with Jupyter Notebooks first and then with Flask and MongoDB:
* [NASA Mars News](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
* [JPL Mars Space Images - Featured Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
* [Mars Weather](https://twitter.com/marswxreport?lang=en)
* [Mars Facts](https://space-facts.com/mars/)
* [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)



## Initial Scraping

The initial scraping of five websites was done using:
* Python Jupyter Notebook.
* pandas.
* Beautiful Soup.
* Splinter.


### Set Up

```python
# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
```

### NASA Mars News

```python
# scrape latest news article title and headline

# initialize browser
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# store full url
news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# visit site
browser.visit(news_url)

# parse through html
news_soup = bs(browser.html, 'html.parser')

# store title and headline
news_title = news_soup.find_all('div', class_='content_title')[0].text
news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

# close browser
browser.quit()

# print title and headline
print(news_title)
print(news_p)
```

![latest-mars-news-headline](images/latest-mars-news-headline.png)


### JPL Mars Space Images - Featured Image

```python
# scrape featured_image_url

# initialize browser
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# store full and base urls
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
image_base_url = 'https://www.jpl.nasa.gov'

# visit site
browser.visit(image_url)

# click on 'full image' to open the image in full
browser.click_link_by_partial_text('FULL IMAGE')

# parse through html
image_soup = bs(browser.html, 'html.parser')

# store partial url
img = image_soup.find('img', class_='fancybox-image')['src']

# combine base url with partial url
featured_image_url = image_base_url + img

# close browser
browser.quit()

# print url
featured_image_url
```

![latest-mars-featured-image](images/latest-mars-featured-image.png)
[Featured Image Url Here](https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19382_ip.jpg)


### Mars Weather

```python
# scrape latest weather tweet

# initialize browser
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# store full and base urls
weather_url = 'https://twitter.com/marswxreport?lang=en'

# visit site
browser.visit(weather_url)

# parse through html
weather_soup = bs(browser.html, 'html.parser')

# store latest tweet
latest_weather_tweet = weather_soup.find('p', class_='TweetTextSize').text

# close browser
browser.quit()

# print latest tweet
latest_weather_tweet
```

![latest-mars-tweet](images/latest-mars-tweet.png)
Latest Mars Weather Tweet: 'InSight sol 250 (2019-08-10) low -100.0ºC (-148.1ºF) high -26.2ºC (-15.1ºF)\nwinds from the SSE at 4.4 m/s (9.8 mph) gusting to 16.2 m/s (36.2 mph)\npressure at 7.60 hPapic.twitter.com/9sZRRUi3dm'


### Mars Facts

```python
# scrape table with facts about mars

# initialize browser
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# store full url
facts_url = 'https://space-facts.com/mars/'

# reading html into a dataframe
facts_table = pd.read_html(facts_url)

# store only mars facts
mars_table = facts_table[1]

# renaming columns
facts_mapping = {0:'Specifications', 1:'Measurements'}
mars_table = mars_table.rename(columns=facts_mapping)

# saving as html table format
mars_table.to_html('mars_table.html', index=False)

# close browser
browser.quit()

# print data frame
print(mars_table)
```

![latest-mars-data-table](images/latest-mars-data-table.png)


### Mars Hemispheres

```python
# scrape hemisphere images

# initialize browser
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

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
    
# close browser
browser.quit()

# create list of hemisphere titles and hemisphere urls in dictionaries
featured_hemisphere_list = [{'title': title_list[0], 'img_url': url_list[0]},
                            {'title': title_list[1], 'img_url': url_list[1]},
                            {'title': title_list[2], 'img_url': url_list[2]},
                            {'title': title_list[3], 'img_url': url_list[3]}]
featured_hemisphere_list
```
Featured Hemisphere List: [{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]

## Python Scraping with Flask and MongoDB

The next scraping of the same five websites was done using:
* Python
* pandas
* Beautiful Soup
* Splinter
* Redirect
* Flask
* PyMongo

### Set Up
### NASA Mars News
### JPL Mars Space Images - Featured Image
### Mars Weather
### Mars Facts
### Mars Hemispheres
