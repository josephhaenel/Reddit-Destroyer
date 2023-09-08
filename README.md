# Reddit Thread Scraper

## How to use:
1. Install [git](https://git-scm.com/downloads)
2. Install [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
3. Open the Anaconda prompt(miniconda3), and cd into the project directory ~/Reddit-Destroyer `cd Reddit-Destroyer`
4. Create a new environment from the yaml file `conda create --name RedditDestroyerEnv --file requirements.yaml`
5. Actiate the environment `conda activate RedditDestroyerEnv`
6. Clone the repository `git clone https://github.com/josephhaenel/Reddit-Destroyer.git`
7. From your command line or integrated terminal, cd into the directory ~/Reddit-Destroyer `cd Reddit-Destroyer`
    - On Windows: Press Windows + R, type *cmd*, and press Enter
    - On macOS: Press Cmd + Space, type *Terminal*, and press Enter
    - On Linux: Open a terminal from the application menu or use a shortcut, often Ctrl + Alt + T
8. Run the script: Type into the terminal `python3 Reddit-Destroyer.py <Link>` and press enter, where Link is a link to a reddit thread, ex: 'https://www.reddit.com/r/funny/comments/16brnzb/self_aware/'

## Dependencies
- Python v3.11.4
- Selenium v3.141
- BeautifulSoup4 v4.12.2
- Webdriver-manager v4.0.0

*Made by **Joseph Haenel** for CS 325 @SIUE*