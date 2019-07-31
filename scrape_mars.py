    
# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 

    #Windows Users
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest element that contains news title and news_paragraph
        title = soup.find('div', class_='content_title').find('a').text
        par = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['title'] = title
        mars_info['par'] = par

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Space Images through splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        img_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        nasa_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        complete_url = nasa_url + img_url

        # Display full link to featured image
        complete_url

        # Dictionary entry from FEATURED IMAGE
        mars_info['complete_url'] = complete_url 
        
        return mars_info
    finally:

        browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in latest_tweets: 
            mars_tweet = tweet.find('p').text
            if 'Sol' and 'gusting' in mars_tweet:
                print(mars_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['mars_tweet'] = mars_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hem = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hem_image_urls = []

        # Store the main_ul 
        hem_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hem_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hem_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hem_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hem_image_urls'] = hem_image_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()
