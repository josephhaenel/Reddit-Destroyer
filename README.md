# Reddit Thread Scraper

## Prerequisites
- [Git](https://git-scm.com/downloads)
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
- [Firefox](https://www.mozilla.org/en-US/firefox/new/)

## How to Use
1. **Clone the Repository:**
   - Run `git clone https://github.com/josephhaenel/Reddit-Destroyer.git`

2. **Navigate to the Project Directory:**
   - Open the Anaconda Prompt (Miniconda3).
   - Enter `cd Reddit-Destroyer`

3. **Set Up the Conda Environment:**
   - Create a new environment from the provided YAML file:
     - `conda env create -f requirement.yaml`
   - Activate the environment:
     - `conda activate RedditDestroyerEnv`

4. **Navigate to the Project Directory via Command Line or Integrated Terminal:**
   - On Windows: Press `Windows + R`, type `cmd`, and press `Enter`
   - On macOS: Press `Cmd + Space`, type `Terminal`, and press `Enter`
   - On Linux: Open a terminal from the application menu or use the shortcut, often `Ctrl + Alt + T`

5. **Change and Setup OPENAI API Key**
   - Navigate to the OPENAI website (should be something like platform.openai.com)
   - After logging in, there should be a tab to the left that says API Keys; click it.
   - Click "Create New Secret Key"
   - Input any name and click "Create Secret Key"
   - Copy it and navigate to "chatgpt_integration/apiCalls.py" in your local repository.
   - Replace `"OPENAI_API_KEY"` with your copied API key.

6. **Run the Script:**
   - `python run.py --dir "<Input File>"`
   - Replace `<Input File>` with the path to the .txt file containing Reddit URLs you wish to scrape. For example, `C:\Users\joseph\Desktop\CS 325 Projects\Reddit-Destroyer\CS325_p3\input.txt`
   - Note: The .txt file should contain one URL per line.
   - Also, replace the OpenAI API key with your own.
   - Important: The URLs must *not* be from `https://old.reddit.com/.../...`
   - If a sign-in window pops up in the top right of the Firefox window, close it to allow the script to continue, as it interferes with the process.

7. **Generating Sentiment Graphs:**
   - To generate sentiment graphs from the collected data, you can use the "getGraphs.py" script. Simply run the following command:
     - `python getGraphs.py`
   - The script will generate and store the graphs in the "Data/Plots" directory.

## Dependencies
- Firefox
- Python v3.11.0
- Selenium v3.141
- BeautifulSoup4 v4.12.2
- Webdriver-Manager v4.0.0

**Note: Do not close the Firefox window until it closes by itself.**
*The script's name stopped working due to a Reddit update, but it's not required for the project.*

*Created by **Joseph Haenel** for CS 325 at SIUE*
