# Reddit Thread Scraper

## Prerequisites
- [git](https://git-scm.com/downloads)
- [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
## How to use:
1. **Clone the repository:**
    - `git clone https://github.com/josephhaenel/Reddit-Destroyer.git`
2. **Navigate to the Project Directory:**
    - Open the Anaconda prompt(miniconda3).
    - `cd Reddit-Destroyer`
3. **Set Up the Conda Environment:**
    - Create a new environment from the provided yaml file:
        - `conda create --name RedditDestroyerEnv --file requirements.yaml`
    - Actiate the environment:
        - `conda activate RedditDestroyerEnv`
4. **Navigate to the Project Directory via Command Line or Integrated Terminal:**
    - On Windows: Press Windows + R, type *cmd*, and press Enter
    - On macOS: Press Cmd + Space, type *Terminal*, and press Enter
    - On Linux: Open a terminal from the application menu or use a shortcut, often Ctrl + Alt + T
5. **Run The Script:**
    - Replace `<Link>` with the link to the reddit thread you want to scrape, for example,
     'https://www.reddit.com/r/funny/comments/16brnzb/self_aware/'.
        - `python3 Reddit-Destroyer.py <Link>`

## Dependencies
- Python v3.11.4
- Selenium v3.141
- BeautifulSoup4 v4.12.2
- Webdriver-manager v4.0.0

*Made by **Joseph Haenel** for CS 325 @SIUE*