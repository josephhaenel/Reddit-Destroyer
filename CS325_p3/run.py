'''
    Reddit Destroyer Version 1.0
    Filename:       run.py
    By:             Joseph Haenel
    Date:           09-08-2023
    
    This script provides functionality to scrape a specific Reddit thread.
    The script expects two terminal arguments: the URL of the Reddit thread 
    and the name of an output file where the scraped data will be stored.
    The actual scraping is done by the ScraperClass from the module_2 package.
    
    Inputs:
    - URL of the Reddit thread (required)
    - Output filename (optional)

    Outputs:
    - A file containing the scraped data from the specified Reddit thread.
'''

from module_2.Scraper import ScraperClass
import argparse
from getComments.getComments import GetComments
from chatgpt_integration.apiCalls import APICalls
import os
import sys

def getTerminalArgs() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Path to the .txt file with the Reddit Threads to be scraped', type=str, required=True)
    args = parser.parse_args()
    
    return args.dir

if __name__ == '__main__':
    # Get terminal arguments
    dir = getTerminalArgs()

    if not os.path.isfile(dir):
        print(f"Error: The file {dir} does not exist.")
        sys.exit(1)
    # Open the directory and read in the url's from the .txt file
    with open(dir, 'r') as urlFile:
        # Store the urls in the urls list (Assuming 1 URL per line)
        urls = [line.strip() for line in urlFile.readlines()]

        
    # Iterate over the urls list
    for url in urls:
        # Initialize the scraper with the provided arguments
        scraper = ScraperClass(url)
        # Perform the scraping operation
        scraper.scrape()
        # Call function to get <n> comments from out_file
        get_comments = GetComments()
        comments = get_comments.getCommentsText(url=url, limit=50)
        # Pass comments to API Call
        apiCalls = APICalls(comments, url)
        apiCalls.getSentiment()