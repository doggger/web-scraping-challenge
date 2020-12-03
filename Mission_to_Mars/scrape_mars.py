#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

#Single function that scrapes all data
def scrape_mars():

    #sets up chrome driver
    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #scrapes first site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find_all('div', class_='content_title')
    news_title=divs[1].a.text
    
    news_p = soup.find('div', class_='article_teaser_body').text

    #scrapes second site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    sub_img = soup.find( 'figure', class_='lede')
    name=sub_img.a['href']
    featured_image_url='https://www.jpl.nasa.gov'+ name

    #scrapes table from third site
    url = "https://space-facts.com/mars/"
    tables=pd.read_html(url)
    table_string=tables[0].to_html()

    #scrapes forth site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    lister = soup.find_all('div', class_='description')
    click_list=[]
    hemisphere_image_urls=[]
    #generates a list of 4 hemispheres to click on
    for thing in lister:
        click_list.append(thing.a.h3.text)
    #follows link for each hemisphere
    for thingy in click_list:
        browser.click_link_by_partial_text(thingy)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        linky=soup.find('li').a['href']
        dic = {'title': thingy, 'img_url': linky}
        hemisphere_image_urls.append(dic)
        browser.visit(url)
    
    browser.quit()

    #stores scraped data into a single dictionary
    listing = {
        'title': news_title,
        'teaser': news_p,
        'featured_image_url': featured_image_url,
        'table_string': table_string,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return listing