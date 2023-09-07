from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

class Scraper:
    
    def __init__(self, url, outputFile = 'output.txt'):
        self.url = url
        self.outputFile = outputFile
        
    def getSoupObject(self):
        '''Returns a BeautifulSoup object for a given url'''
        driver = webdriver.Chrome(executable_path=ChromeDriverManager.install())
        driver.get(self.url)
        time.sleep(1) # Just so I don't get IP banned and to let page load
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True: # Scrolling to load all of the page
            driver.implicitly_wait(10)
            driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
            try:
                view_more_comments = driver.find_element_by_css_selector("span.flex.items-center.gap-xs")
                view_more_comments.click()
            except NoSuchElementException:
                pass # View more comments button not found yet
            time.sleep(1) # Wait for page to load
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup
        
    def Scrape():
        pass
    
    