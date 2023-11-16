'''
    Reddit Destroyer Version 2.0
    Filename:       run.py
    By:             Joseph Haenel
    Date:           11-16-2023
    
    This script is designed to scrape content from multiple Reddit threads.
    It reads URLs from a specified text file and performs scraping on each URL.
    The scraping functionality is implemented by ScraperClass from module_2.
    Additionally, it integrates features to analyze comments using 
    GetComments and APICalls from respective modules.

    Inputs:
    - Path to the .txt file containing URLs of Reddit threads (required)

    Outputs:
    - Files containing scraped data from each specified Reddit thread.
      Additional analysis on the comments may be performed and outputted.
'''
import argparse
import os
import sys

from module_2.Scraper import ScraperClass
from getComments.getComments import GetComments
from chatgpt_integration.apiCalls import APICalls


def getTerminalArgs() -> str:
    """
    Parses the command line arguments to get the path of the .txt file
    containing the Reddit thread URLs.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Path to the .txt file with the Reddit Threads to be scraped', type=str, required=True)
    args = parser.parse_args()
    
    return args.dir

if __name__ == '__main__':
    # Get the file path from terminal arguments
    dir = getTerminalArgs()

    # Check if the specified file exists
    if not os.path.isfile(dir):
        print(f"Error: The file {dir} does not exist.")
        sys.exit(1)

    # Read URLs from the specified file
    with open(dir, 'r') as urlFile:
        urls = [line.strip() for line in urlFile.readlines()]  # Assuming one URL per line

    # Process each URL
    for url in urls:
        scraper = ScraperClass(url)  # Initialize the scraper
        scraper.scrape()  # Perform the scraping operation

        # Get and analyze comments
        get_comments = GetComments()
        comments = get_comments.getCommentsText(url=url, limit=50)  # Retrieve comments
        apiCalls = APICalls(comments, url)  # Perform API calls for further analysis
        apiCalls.getSentiment()  # Analyze sentiment of the comments
