from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pandas as pd

def scrape():
    #set up dict to return data
    scrapped_data = {}
    
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # url ='https://mars.nasa.gov/news/'
    url ='https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')
    news_title=soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_ ='article_teaser_body').text
    scrapped_data["news_title"] = news_title
    scrapped_data["news_paragraph"] = news_p
    print(news_p)
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, 'html.parser')
    link_image = soup.findAll('img', class_='headerimage')[0]["src"]
    featured_image_url =url + link_image
    scrapped_data["featured_image_url"] = featured_image_url
    
    
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    tables = pd.read_html(url)
    mars_fact=tables[0]
    print(mars_fact)
    table = mars_fact[:].to_html(index=False, header=False, border=2)
    table.replace('\n', '')
    scrapped_data["mars_facts"] = table  #table1.to_html()
    

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html=browser.html
    soup = bs(html, 'html.parser')
    list_of_images=soup.findAll('img', class_='thumb')
    hemisphere_image_urls = [] #list of dictionary to add the links to images and titles
    for image in list_of_images:
            link_to_image = url+image["src"]
            title = image["alt"][:-10]
            print(link_to_image)
            print(title)
            hem_dict={
                'title':title,
                'image_url':link_to_image
            }
            hemisphere_image_urls.append(hem_dict)
    scrapped_data["mars_hemispheres"] = hemisphere_image_urls
            
    return scrapped_data