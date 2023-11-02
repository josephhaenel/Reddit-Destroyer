import os
import json

class GetComments:
    def __init__(self, base_dir='Data', sub_dir='processed'):
        self.base_dir = base_dir
        self.sub_dir = sub_dir

    def getCommentsText(self, file=None, url=None, limit=50):  # limit parameter with default value of 50
        if file is None and url is not None:
            base_name = [part for part in url.split('/') if part][-1].split('?')[0]
            in_file = os.path.join(self.base_dir, self.sub_dir, base_name + '_output.txt')
        elif file is not None:
            in_file = os.path.join(self.base_dir, self.sub_dir, file)
        else:
            raise ValueError("Either file or url must be provided")

        comments_text = []
        try:
            with open(in_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Parse the JSON data from the file
                # Limit the number of comments processed to the limit parameter
                for entry in data[:limit]:  # Slice the data to only include up to `limit` entries
                    comments_text.append(entry['Text'])  # Extract the "Text" field
        except FileNotFoundError:
            print(f"The file {in_file} was not found.")
        except json.JSONDecodeError:
            print(f"There was an error decoding the JSON data from the file {in_file}.")

        return comments_text
