# Adding Imports
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    # defining browser using splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    
    browser = init_browser()
    # Step 1 - Scraping
    # NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()
    news = {"news_title": news_title, "news_details": news_p}

    # JPL Mars Space Images - Featured Image

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featured_image = soup.find('div', class_='img')
    featured_image = 'https://www.jpl.nasa.gov' + featured_image.img['src']

    # Mars Weather
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find(
        'p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    unwanted_anchor = mars_weather.find('a')
    # print(unwanted_anchor)
    unwanted_anchor.extract()
    mars_weather = mars_weather.get_text()
    print(mars_weather)

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_facts = mars_facts[0]
    mars_table = mars_facts.to_html(header=False, index=False)
    # print(table_html)

    # Mars Hemispheres
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    html = browser.html
    hemp_soup = BeautifulSoup(html, 'html.parser')
    # print(hemp_soup)
    hemispheres_info = hemp_soup.find_all('div', class_="item")
    # print(hemispheres_info)
    hemisphere_image_urls = []
    base_hem = 'https://astrogeology.usgs.gov'
    for hemisphere in hemispheres_info:
        title = hemisphere.find('div', class_="description").a.get_text()
        image_link = hemisphere.find('div', class_="description").a['href']
        print(image_link)
        browser.visit(base_hem+image_link)
        hem_html = browser.html
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        image_url = hem_soup.find('div', class_="downloads").ul.li.a['href']
        print(image_url)
        hem_dict = {'title': title, "image_url": image_url}
        hemisphere_image_urls.append(hem_dict)

    mars_info = {}

    mars_info["news"] = news

    mars_info["featured_image"] = featured_image

    mars_info["weather"] = mars_weather

    mars_info["facts"] = mars_table

    mars_info["hemispheres"] = hemisphere_image_urls
    return mars_info
