'''
Must insert your own API key
'''
OPENAI_API_KEY = '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'

import openai
import time
import os

class APICalls:
    def __init__(self, comments, url):
        base_name = [part for part in url.split('/') if part][-1].split('?')[0]
        self.outFile = os.path.join('Sentiments', base_name + '_sentiment.txt')
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
        with open(self.outFile, 'w') as sentiment_file:
            for comment in self.comments:
                sentiment = self.analyzeSentiment(comment)
                print(f"Comment: {comment}\nSentiment: {sentiment}\n")
                sentiment_file.write(f"Comment: {comment}\nSentiment: {sentiment}\n\n")


