'''
    Reddit Destroyer Version 0.0.1
    By Joseph Haenel
'''

import time
from resources.Scraper import ScraperClass
import os
import argparse

def getTerminalArgs() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(help='The url of the Reddit Thread to be scraoed' , dest='url' , type=str)
    args = parser.parse_args()
    
    return args.url

if __name__ == '__main__':
    scraper = ScraperClass(getTerminalArgs())
    scraper.scrape()
    