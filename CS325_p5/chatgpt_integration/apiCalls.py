"""
This module implements the APICalls class to interface with the OpenAI API for sentiment analysis of comments. 
It requires an OpenAI API key, which should be set in the OPENAI_API_KEY variable.

The APICalls class takes a list of comments and a URL as inputs. It extracts the basename from the URL to name the output file, which will be stored in the 'Data/Sentiments' directory. The class performs sentiment analysis on each comment using the OpenAI API and writes the results to the output file. A 20-second wait is implemented between each API call to avoid rate limits.

Attributes:
    comments (list[str]): A list of comments for sentiment analysis.
    outFile (str): File path to store the analysis results.

Methods:
    analyzeSentiment(comment: str) -> str:
        Analyzes the sentiment of a single comment using the OpenAI API.
        Returns the sentiment ('positive', 'negative', or 'neutral').

    getSentiment():
        Processes each comment for sentiment analysis and writes the results to the output file.

Exceptions:
    ValueError: Raised if the OpenAI API key is not set.
    openai.error.OpenAIError: Raised for errors during API calls.

Usage Example:
    Set the OPENAI_API_KEY with a valid API key.
    Initialize APICalls with comments and a URL, then call `getSentiment` to analyze sentiments.
"""

OPENAI_API_KEY = ''  # Replace with YOUR OWN OpenAI API key

import openai
import time
import os
import re

class APICalls:
    def __init__(self, comments, url):
        """
        Initializes the APICalls class with comments and URL.
        Extracts the basename from the URL to create an output file path.
        Raises ValueError if the OpenAI API key is not set.
        """
        base_name = [part for part in url.split('/') if part][-1].split('?')[0]
        base_name = re.sub(r'[^\w\s-]', '', base_name).strip()
        self.outFile = os.path.join('Data', 'Sentiments', base_name + '_sentiment.txt')
        self.comments = comments

        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set.")
        openai.api_key = OPENAI_API_KEY

    def analyzeSentiment(self, comment):
        """
        Sends a comment to the OpenAI API for sentiment analysis.
        Implements a 20-second delay to avoid API rate limiting.
        Returns the sentiment of the comment.
        """
        time.sleep(20)  # Avoiding rate limiting
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Analyze the sentiment of the following comment, responding with positive, negative, or neutral."},
                          {"role": "user", "content": comment}]
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return None

    def getSentiment(self):
        """
        Iterates over the list of comments, analyzes their sentiment,
        and writes the results to the output file.
        """
        with open(self.outFile, 'w', encoding='utf-8') as sentiment_file:
            for comment in self.comments:
                sentiment = self.analyzeSentiment(comment)
                print(f"Comment: {comment}\nSentiment: {sentiment}\n")
                sentiment_file.write(f"Comment: {comment}\nSentiment: {sentiment}\n\n")
