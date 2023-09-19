'''
    Reddit Destroyer Version 1.0
    Filename:       Reddit-Destroyer.py
    By:             Joseph Haenel
    Date:           09-08-2023
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
    