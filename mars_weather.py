import time
import pandas as pd
from flask import Flask, render_template
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import re

def mars():
    
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')
    # print(soup.body.prettify())
    results = soup.find('div', class_='content_title')
    # print(results.text)
    content = soup.find('div', class_='rollover_description_inner')
    # print(content.text)
    news_title = []
    news_content = []
        
    # title = result.find(class_='content_title')
    news_title.append(results.text)
    # content = result.div.a
    news_content.append(content.text)
    # new_title = [word.strip('\n')for word in news_title]
    content_title = [word.strip('\n')for word in news_content]
    mars_data['news_title'] = news_content 
    mars_data['news_paragraph'] = content_title
    # # news_content = news_content.strip('\n')
    # print(new_title)
    # print(content_title)
    featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(featured_url)
    featured_soup = bs(response.text, "html.parser")
    
    featured_image = featured_soup.find('a', class_='fancybox')
    featured_image_url = featured_image['data-fancybox-href']
    featured_image_final = 'https://www.jpl.nasa.gov' + featured_image

    mars_data['jpl_url'] = featured_image_final


    res = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(res)
    mars_facts_df = mars_facts[0]
    # mars_facts_df
    # soup = bs(res.content,'lxml')
    # table = soup.find_all('table')
    mars_html = mars_facts_df.to_html(index= False, header= None)
    # mars_html
    
    mars_data['mars_facts'] = mars_html

    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(mars_url)
    mars_soup = bs(response.text, 'html.parser')
    browser = Browser('chrome', executable_path='chromedriver', headless=False)
    browser.visit(mars_url)
    mars_img_list = mars_soup.find_all('a', class_='itemLink')
    hemisphere_image_urls = []

    for hemisphere_img in mars_img_list:
        
        hemisphere_dict = {}
        
        title = hemisphere_img.h3.text
        
        browser.click_link_by_partial_text(title)
        
        image_url = browser.find_by_css('.wide-image').first['src']
        
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(hemisphere_dict) 
        
        browser.back()
    mars_data['mars_hem_urls'] = hemisphere_image_urls
    # hemisphere_image_urls
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(mars_twitter)

    mars_tweet_soup = bs(response.text, "html.parser")
    mars_tweets = mars_tweet_soup.find_all('div', class_='tweet')

    i = 0

    for tweet in mars_tweets:
        
        tweet_timestamp = int(tweet.find('span', class_= '_timestamp')['data-time'])
        
        tweet_text = tweet.find('p', class_ = 'tweet-text').text
        
        if (re.match(r'Sol \d\d\d\d \(', tweet_text) is not None) and (tweet_timestamp > i):
            
            mars_weather = tweet_text
            
            i = tweet_timestamp
    mars_data['mars_weather'] = mars_weather

    return mars