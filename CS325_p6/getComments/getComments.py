"""
This module defines the GetComments class which is responsible for extracting comment data from JSON files.
The class is initialized with a base directory and a sub-directory where the JSON files are expected to be found.
It provides a method `getCommentsText` that can retrieve comments either from a specified file within the directories
or from a JSON file named after the last part of a given URL, limited to a specified number of comments.

Attributes:
    baseDir (str): The base directory where the JSON files are stored.
    subDir (str): The subdirectory within baseDir where processed JSON files are located.

Methods:
    getCommentsText(file=None, url=None, limit=50):
        Retrieves and returns the text of comments from a JSON file. The JSON file can be specified directly
        by its filename or indirectly via a URL. Only the first `limit` comments are retrieved.

Exceptions:
    FileNotFoundError: Raised when the specified JSON file does not exist in the given path.
    json.JSONDecodeError: Raised when the JSON file content could not be decoded.
"""
import os
import json
import re

class GetComments:
    def __init__(self, baseDir='Data', subDir='processed'):
        self.baseDir = baseDir
        self.subDir = subDir

    def getCommentsText(self, file=None, url=None, limit=50):  # limit parameter with default value of 50
        if file is None and url is not None:
            baseName = [part for part in url.split('/') if part][-1].split('?')[0]
            baseName = re.sub(r'[^\w\s-]', '', baseName).strip()
            inFile = os.path.join(self.baseDir, self.subDir, baseName + '_output.txt')
            
        elif file is not None:
            inFile = os.path.join(self.baseDir, self.subDir, file)
        else:
            raise ValueError("Either file or url must be provided")

        comments_text = []
        try:
            with open(inFile, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse the JSON data from the file
                # Limit the number of comments processed to the limit parameter
                for entry in data[:limit]:  # Slice the data to only include up to `limit` entries
                    comments_text.append(entry['Text'])  # Extract the text field
        except FileNotFoundError:
            print(f"The file {inFile} was not found.")
        except json.JSONDecodeError:
            print(f"There was an error decoding the JSON data from the file {inFile}.")

        return comments_text
