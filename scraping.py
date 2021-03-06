
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup

# import numpy as np
import pandas as pd
import datetime as dt

from webdriver_manager.chrome import ChromeDriverManager

def button_click():

    hello_messsage = "<H2>Buenos Dias El Mundo</H2>"

    return hello_message

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "images": mission_to_mars(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # the next line is not included in the graphic in the course material but it was exported from our earlie code 
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None    

    return news_title, news_p

def featured_image(browser):
    # JPL Space Images Featured Image

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # Use the base url to create an absolute url
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    except AttributeError:
        return None
   
    return img_url


def mars_facts():
    # Mars Facts - with try/except added 20210825
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()

def mission_to_mars(browser):

    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    mars_soup = soup(html, 'html.parser')


    # hemisphere_dict = {"image":"placeholder". "title":"placeholder2"}

    item_list = mars_soup.select('div.item')

    for item in item_list:
        next_part = item.find('a', class_='itemLink product-item').get('href')
        item_title = item.find('h3').get_text()
        url_second_page = f'{url}{next_part}'
        # print(item_title)
    
        browser.visit(url_second_page)
        html2 = browser.html
        soup_page2 = soup(html2, 'html.parser')
        img_url_rel2 = soup_page2.find('img', class_='wide-image').get('src')
        # print(img_url_rel2)

        img_url_full = f'{url}{img_url_rel2}'
    
        hemisphere_dict = {"image":"", "title":""}
        hemisphere_dict["image"] = img_url_full
        hemisphere_dict["title"] = item_title
    
        hemisphere_image_urls.append(hemisphere_dict)

    browser.back()

    return hemisphere_image_urls

    
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
