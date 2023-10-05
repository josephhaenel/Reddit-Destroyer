'''
    Filename:       Scraper.py
    By:             Joseph Haenel
    Date:           09-08-2023
    Dependencies:   Selenium, BeautifulSoup4, Webdriver-Manager, Firefox Browser
    Using Python 3.11.0
'''

__all__ = ['ScraperClass']  # Public Classes

# Import required modules and dependencies
from .SoupError import SoupObjectError
from .SoupObj import SoupObject
from .getInfo import InfoExtractor
import os
import sys
import json

# Main scraper class
class ScraperClass:
    def __init__(self, url, output_file = None):
        self.url = url
        if output_file is None:
            base_name = [part for part in self.url.split('/') if part][-1].split('?')[0]  # Remove any query string
            self.output_file = os.path.join('outputs', base_name + '_output.txt')
        else:
            self.output_file = os.path.join('outputs', output_file)

    # Main scraping function
    def scrape(self):
        try:
            soup_obj = SoupObject.get_soup_object(self.url)
        except SoupObjectError as e:
            print(e)
            sys.exit(1)

        results = []

        for comment in soup_obj.find_all("shreddit-comment"):
            commentData = {
                "Text": InfoExtractor.getCommentText(comment).replace('\n', '').strip(),
                "Username": InfoExtractor.getCommentUsername(comment),
                'Date': InfoExtractor.getCommentDate(comment),
                "Score": InfoExtractor.getCommentLikes(comment)
            }
            results.append(commentData)

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
