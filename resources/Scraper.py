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
import json

class SoupObjectError(Exception):
    def __init__(self, message = "Soup Object could not be retrieved"):
        super().__init__(message)

class ScraperClass:
    
    def __init__(self, url, outputFile = 'output.txt'):
        self.url = url
        self.outputFile = outputFile
        
    def getSoupObject(self):
        '''Returns a BeautifulSoup object for a given url'''
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(1)  # Just so I don't get IP banned and to let page load
        last_height = driver.execute_script('return document.body.scrollHeight')
        
        max_attempts = 10  # Maximum number of times to attempt scrolling
        attempts = 0

        while attempts < max_attempts:
            # Send multiple PAGE_DOWN key events
            for _ in range(3):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)  # Smaller sleep between key events

            try:
                view_more_comments = driver.find_element(By.XPATH, "//*[@id=\"comment-tree\"]/faceplate-partial/div[1]/button")
                expand_comment_section = driver.find_element(By.XPATH, "//*[@id=\"comment-tree\"]/shreddit-comment[2]/div[3]/faceplate-partial")
                expand_comment_section_more = driver.find_element(By.XPATH, "//*[@id=\"comment-tree\"]/shreddit-comment[2]/div[3]/shreddit-comment/div[3]/faceplate-partial")
                expand_comment_section_more.click()
                view_more_comments.click()
                expand_comment_section.click()
            except NoSuchElementException:
                pass  # View more comments button not found yet

            time.sleep(1)  # Wait for page to load

            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                attempts += 1  # Increment attempts if height hasn't changed
            else:
                last_height = new_height  # Reset attempts if height has changed
                attempts = 0

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup
    
    def getCommentText(self, comment):
        commentText = comment.find(id="-post-rtjson-content")
        if not commentText:
            raise Exception(f"Could not get commentText: {commentText}")
        return commentText.get_text()

            
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
            json.dump(results, file, indent=4)
    