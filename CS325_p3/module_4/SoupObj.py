from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import time
import os

class SoupObject:
    '''
    The SoupObject class provides functionality to fetch and parse the complete content of a given Reddit thread URL.
    
    The class employs the Selenium WebDriver to load and expand all comments of a Reddit thread by triggering 
    the "more replies" and "View more comments" buttons on the page. After expanding all the comments, 
    it uses BeautifulSoup to parse the page content.
    
    It contains a single static method:
    - get_soup_object(url): Returns a parsed BeautifulSoup object of the provided URL's content.
    '''

    @staticmethod
    def get_soup_object(url):
        '''
        Fetches and parses the complete content of a given Reddit thread URL.

        Parameters:
        - url (str): The URL of the Reddit thread to be scraped.

        Returns:
        - BeautifulSoup object: Parsed content of the provided URL.
        '''
        # Initialize the browser driver (Firefox in this case)
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.get(url)
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
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        driver.execute_script("arguments[0].click();", button)
                        time.sleep(1)  # Allow the new content to load
                    except StaleElementReferenceException:
                        # The button became stale, so move on to the next button
                        continue

                continue

            except:  # No "more replies" buttons found
                try:
                    # Try clicking the "View more comments" button
                    viewMoreCommentsButton = wait.until(
                        EC.presence_of_element_located((By.XPATH, viewMoreCommentsXpath)))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", viewMoreCommentsButton)
                    driver.execute_script("arguments[0].click();", viewMoreCommentsButton)
                    time.sleep(1)  # Allow the new comments to load
                except:  # No "View more comments" button found, scroll down instead
                    driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)

            # Check for changes in scroll height
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:  # If no new content, break the loop
                break

            lastHeight = newHeight  # Update scroll height
        
        # Get base name of reddit thread from URL    
        base_name = [part for part in url.split('/') if part][-1].split('?')[0]
        raw_html_filename = os.path.join("Data", "raw", f"{base_name}_raw.txt")
        # Write the raw html to raw/<RedditThread>_raw.txt
        with open(raw_html_filename, "w", encoding="utf-8") as raw_html_file:
            raw_html_file.write(driver.page_source)
        # Convert the loaded page source into a BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()  # Close the browser
        return soup
