from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        time.sleep(1) # Just so I don't get IP banned
        for _ in range(self.scrolls):
            driver.implicitly_wait(10)
            driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    def Scrape():
        pass
    
    