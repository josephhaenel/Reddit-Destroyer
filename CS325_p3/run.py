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

def getTerminalArgs() -> str:
    '''
    Retrieves the terminal arguments for the Reddit thread URL and output file.
    
    Returns:
    - url (str): URL of the Reddit thread to be scraped.
    - out_file (str, optional): The output file name. 
    
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(help='The url of the Reddit Thread to be scraped', dest='url', type=str)
    parser.add_argument(help='The output file', dest='out_file', nargs='?', type=str)
    args = parser.parse_args()
    
    return args.url, args.out_file

if __name__ == '__main__':
    # Get terminal arguments
    url, out_file = getTerminalArgs()
    # Initialize the scraper with the provided arguments
    scraper = ScraperClass(url, out_file)
    # Perform the scraping operation
    scraper.scrape()
    # Call function to get <n> comments from out_file
    get_comments = GetComments()
    comments = get_comments.getCommentsText(file=out_file, url=url, limit=50)
    # Pass comments to API Call
    apiCalls = APICalls(comments, url)
    apiCalls.getSentiment()
    
    
