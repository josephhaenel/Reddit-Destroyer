'''
    Filename:       Scraper.py
    By:             Joseph Haenel
    Date:           09-08-2023
    Dependencies:   Selenium, BeautifulSoup4, Webdriver-Manager
    Using Python 3.11.4
'''
__all__ = ['Scraper', 'scrape'] # Public Functions/Variables

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import sys

class SoupObjectError(Exception):
    def __init__(self, message = "Soup Object could not be retrieved"):
        super().__init__(message)

class Scraper:
    
    def __init__(self, url, outputFile = 'output.txt'):
        self.url = url
        self.outputFile = outputFile
        
    def getSoupObject(self):
        '''Returns a BeautifulSoup object for a given url'''
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(1) # Just so I don't get IP banned and to let page load
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True: # Scrolling to load all of the page
            driver.implicitly_wait(10)
            driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
            try:
                view_more_comments = driver.find_element_by_css_selector("span.flex.items-center.gap-xs")
                expand_comment_section = driver.find_element_by_css_selector("svg[icon-name='join-outline']") # FIXME: Might have an issue
                view_more_comments.click()
                expand_comment_section.click()
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
    
    def getCommentText(self, comment):
        commentText = comment.get("post-rtjson-content")
        if not commentText:
            raise Exception(f"Could not get commentText: {commentText}")
        return commentText
            
    def scrape(self):
        try:
            soupObj = self.getSoupObject()
        except SoupObjectError as e:
            print(e)
            sys.exit(1) # Exit the program with an error code 1
        
        results = []

        for index, comment in enumerate(soupObj.find_all("shreddit-comment")):
            commentData = {
                "Text": self.getCommentText(comment),
            #     "Author": self.getCommentAuthor(comment),
            #     'Date': self.getCommentDate(comment),
            #     "Score": self.getCommentScore(comment)
            }
            results.append(commentData)

        with open(self.outputFile, 'w') as file:
            file.write(results)
    