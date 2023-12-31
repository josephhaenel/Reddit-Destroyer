# Reddit Thread Scraper

## Prerequisites
- [git](https://git-scm.com/downloads)
- [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
- [firefox](https://www.mozilla.org/en-US/firefox/new/)

## How to use:
1. **Clone the Repository:**
    - `git clone https://github.com/josephhaenel/Reddit-Destroyer.git`
2. **Navigate to the Project Directory:**
    - Open the Anaconda prompt(miniconda3).
    - `cd Reddit-Destroyer`
3. **Set Up the Conda Environment:**
    - Create a new environment from the provided yaml file:
        - `conda env create -f requirement.yaml`
    - Actiate the environment:
        - `conda activate RedditDestroyerEnv`
4. **Navigate to the Project Directory via Command Line or Integrated Terminal:**
    - On Windows: Press Windows + R, type *cmd*, and press Enter
    - On macOS: Press Cmd + Space, type *Terminal*, and press Enter
    - On Linux: Open a terminal from the application menu or use a shortcut, often Ctrl + Alt + T
5. Change and Setup OPENAI API Key
   - Navigate to OPENAI website (Should be something like platform.openai.com)
   - After logging in, their should be a tab to the left which says API Keys, click it.
   - Click "Create New Secret Key"
   - Input any name and click "Create Secret Key"
   - Copy it and navigate to "chatgpt_integration/apiCalls.py" in your local repository.
   - Replace "OPENAI_API_KEY" with your copied api key.
7. **Run The Script:**
    - Replace `<Link>` and `<Output File>` with the link to the reddit thread you want to scrape and file you want the comments to output to, for example,
     'https://www.reddit.com/r/funny/comments/16brnzb/self_aware/'.
        - `python Reddit-Destroyer.py <Link> <Output File>`
    - `<Output File>` is optional and will default to `<redditName>_output.txt`
    - Please Note: The link must *NOT* be a https://*old*.reddit.com/.../...


## Dependencies
- Firefox
- Python v3.11.0
- Selenium v3.141
- BeautifulSoup4 v4.12.2
- Webdriver-Manager v4.0.0

**Do not close the Firefox window until it closes itself**

*Made by **Joseph Haenel** for CS 325 @SIUE*
