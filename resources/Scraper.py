'''
    Filename:       Scraper.py
    By:             Joseph Haenel
    Date:           09-08-2023
    Dependencies:   Selenium, BeautifulSoup4, Webdriver-Manager, Firefox Browser
    Using Python 3.11.0
'''

__all__ = ['ScraperClass']  # Public Classes

# Import required modules and dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import time
import os
import sys
import json

# Custom exception to handle scenarios where BeautifulSoup object retrieval fails.
class SoupObjectError(Exception):
    def __init__(self, message="Soup Object could not be retrieved"):
        super().__init__(message)

# Main scraper class
class ScraperClass:
    def __init__(self, url, output_file = None):
        self.url = url
        if output_file is None:
            base_name = [part for part in self.url.split('/') if part][-1].split('?')[0]  # Remove any query string
            self.output_file = os.path.join('outputs', base_name + '_output.txt')
        else:
            self.output_file = os.path.join('outputs', output_file)

    # Function to get BeautifulSoup object after loading page and expanding all/most comments
    def get_soup_object(self):
        # Initialize the browser driver (Firefox works better than chrome for me)
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.get(self.url)
        time.sleep(1)  # Allow the page to load

        # Capture the initial scroll height of the page
        lastHeight = driver.execute_script("return document.body.scrollHeight")

        # Continuous loop to expand all comments until no more are found
        while True:
            wait = WebDriverWait(driver, 10)
            moreRepliesXpath = "//button[.//span[contains(., 'more replies')]]"
            viewMoreCommentsXpath = "//button[.//span[contains(., 'View more comments')]]"

            try:
                # Click all visible "more replies" buttons
                moreRepliesButtons = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, moreRepliesXpath)))

                for button in moreRepliesButtons:
                    try:
                        # Scroll the button into view and click it
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", button)
                        driver.execute_script("arguments[0].click();", button)
                        time.sleep(1)  # Allow the new content to load
                    except StaleElementReferenceException:
                        # The button became stale, probably because the page structure changed. Continue to the next button.
                        continue

                # No exceptions, implies we clicked all visible "more replies" buttons, so move to the next iteration.
                continue

            except: # No more "more replies" buttons found
                try:
                    # Try clicking the "View more comments" button to load more comments
                    viewMoreCommentsButton = wait.until(
                        EC.presence_of_element_located((By.XPATH, viewMoreCommentsXpath)))
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", viewMoreCommentsButton)
                    driver.execute_script(
                        "arguments[0].click();", viewMoreCommentsButton)
                    time.sleep(1)  # Allow the new comments to load
                except:  # If no "View more comments" button is found, simply scroll down
                    driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                    
            # Check scroll height again
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:  # No new content, break
                break

            lastHeight = newHeight # Update scroll height

        # Create a beautifulsoup object for parsing
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit() # Close the browser
        return soup

    # Extract the text of a comment
    def getCommentText(self, comment):
        commentText = comment.find(id="-post-rtjson-content")
        if commentText is None:
            return ''
        elif isinstance(commentText, str):
            return commentText.strip()
        else:
            return commentText.get_text().strip()

    # Extract the number of likes of a comment
    def getCommentLikes(self, comment):
        commentLikes = comment.get('score')
        if not commentLikes:
            return 0
        return int(commentLikes) if commentLikes else 0

    # Extract the username of the person who posted the comment
    def getCommentUsername(self, comment):
        commentUsername = comment.find(
            'a', class_="font-bold text-neutral-content-strong text-12 hover:underline")
        return commentUsername.get_text(strip=True) if commentUsername else None

    # Extract the date when the comment was posted
    def getCommentDate(self, comment):
        commentDate = comment.find('time')
        return commentDate['title'] if commentDate and 'title' in commentDate.attrs else None

    # Main scraping function
    def scrape(self):
        try:
            soup_obj = self.get_soup_object()
        except SoupObjectError as e:
            print(e)
            sys.exit(1)

        results = []

        for comment in soup_obj.find_all("shreddit-comment"):
            commentData = {
                "Text": self.getCommentText(comment).replace('\n', '').strip(),
                "Username": self.getCommentUsername(comment),
                'Date': self.getCommentDate(comment),
                "Score": self.getCommentLikes(comment)
            }
            results.append(commentData)

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
