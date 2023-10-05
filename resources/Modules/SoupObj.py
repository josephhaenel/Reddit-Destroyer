from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import time

class SoupObject:

    @staticmethod
    def get_soup_object(url):
                # Initialize the browser driver (Firefox works better than chrome for me)
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