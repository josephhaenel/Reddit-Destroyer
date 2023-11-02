"""
This module contains the APICalls class that interfaces with the OpenAI API to analyze the sentiment of a list of comments. 

Note:
    An OpenAI API key must be provided by setting the OPENAI_API_KEY variable. Replace '#####' with your actual API key.

The class initializes with a list of comments and a URL. It extracts the basename from the URL to create an output file in the 'Data/Sentiments' directory. This output file is used to store the sentiment analysis results.

It uses the OpenAI API to determine the sentiment of each comment and writes the results to the specified output file. To avoid hitting the OpenAI API rate limit, it waits 20 seconds between each API call.

Attributes:
    comments (list): A list of comments to be analyzed.
    outFile (str): The file path where sentiment analysis results will be stored.

Methods:
    analyzeSentiment(comment):
        Sends a single comment to the OpenAI API for sentiment analysis.
        Returns the sentiment of the comment as determined by the API ('positive', 'negative', or 'neutral').

    getSentiment():
        Iterates over all comments and writes their analyzed sentiments to the output file.

Exceptions:
    ValueError: Raised when the OpenAI API key is not set.
    openai.error.OpenAIError: Raised when an error occurs during the API call.

Usage:
    Ensure that OPENAI_API_KEY is set with your valid API key.
    Initialize the APICalls class with a list of comments and a URL, and call the `getSentiment` method to perform sentiment analysis on the comments.
"""
OPENAI_API_KEY = 'YOUR_API_KEY_HERE'

import openai
import time
import os

class APICalls:
    def __init__(self, comments, url):
        base_name = [part for part in url.split('/') if part][-1].split('?')[0]
        self.outFile = os.path.join('Data','Sentiments', base_name + '_sentiment.txt')
        self.comments = comments
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set.")
        openai.api_key = OPENAI_API_KEY

    def analyzeSentiment(self, comment):
        time.sleep(20) # Avoidng Rate Limiting
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
        with open(self.outFile, 'w', encoding='utf-8') as sentiment_file:
            for comment in self.comments:
                sentiment = self.analyzeSentiment(comment)
                print(f"Comment: {comment}\nSentiment: {sentiment}\n")
                sentiment_file.write(f"Comment: {comment}\nSentiment: {sentiment}\n\n")


