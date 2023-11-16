'''
    Filename:       Scraper.py
    By:             Joseph Haenel
    Date:           09-08-2023
    Dependencies:   Selenium, BeautifulSoup4, Webdriver-Manager, Firefox Browser
    Using Python 3.11.0
    
    This module provides functionality to scrape content from a Reddit thread
    and output the data into a file. The primary class in this module, ScraperClass,
    expects a Reddit URL and an optional output filename. If the output filename 
    is not provided, it will generate one based on the last segment of the URL.
    
    Outputs:
    - A JSON file with structured information about comments including text,
      username, date, and score.
'''

__all__ = ['ScraperClass']  # Public Classes

# Import required modules and dependencies
from module_3.SoupError import SoupObjectError
from module_4.SoupObj import SoupObject
from module_1.getInfo import InfoExtractor
import os
import sys
import json

class ScraperClass:
    def __init__(self, url, output_file=None):
        '''
        Initializes the scraper.
        
        Parameters:
        - url (str): The URL of the Reddit thread to be scraped.
        - output_file (str, optional): The name of the output file. 
                                       If not provided, a filename is generated based on the URL.
        '''
        self.url = url
        if output_file is None:
            # Extract the last segment of the URL, removing any query strings
            base_name = [part for part in self.url.split('/') if part][-1].split('?')[0]
            self.output_file = os.path.join('Data', 'processed', base_name + '_output.txt')
        else:
            self.output_file = os.path.join('Data', 'processed', output_file)

    def scrape(self):
        '''
        Main scraping function. It tries to get the soup object, then extracts
        comments information and writes them to a JSON file.
        '''
        try:
            # Attempt to get the soup object
            soup_obj = SoupObject.get_soup_object(self.url)
        except SoupObjectError as e:
            # Exit if there's an error fetching the soup object
            print(e)
            sys.exit(1)

        results = []

        # Iterate through each comment and extract required information
        for comment in soup_obj.find_all("shreddit-comment"):
            commentData = {
                "Text": InfoExtractor.getCommentText(comment).replace('\n', '').strip(),
                "Username": InfoExtractor.getCommentUsername(comment),
                'Date': InfoExtractor.getCommentDate(comment),
                "Score": InfoExtractor.getCommentLikes(comment)
            }
            results.append(commentData)

        # Write the results to a JSON file
        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
