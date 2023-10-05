'''
    Reddit Destroyer Version 1.0
    Filename:       Reddit-Destroyer.py
    By:             Joseph Haenel
    Date:           09-08-2023
'''

from resources.Modules.Scraper import ScraperClass
import argparse

def getTerminalArgs() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(help='The url of the Reddit Thread to be scraped' , dest='url' , type=str)
    parser.add_argument(help='The output file', dest='out_file', nargs='?', type=str)
    args = parser.parse_args()
    
    return args.url, args.out_file

if __name__ == '__main__':
    url, out_file = getTerminalArgs()
    scraper = ScraperClass(url, out_file)
    scraper.scrape()
    