from bs4 import BeautifulSoup, Comment
import requests
from sys import argv
from os import path


def get_soup(url):
    try:
        downloaded_html = requests.get(url)
        if downloaded_html.status_code != 200:
            raise
    except:
        print("\n[-] ERROR: Invalid URL\n")
        exit(0)
    soup = BeautifulSoup(downloaded_html.text, 'html.parser')
    return soup

def get_comments(soup):
    for comments in soup.findAll(text=lambda text: isinstance(text, Comment)):
        print("")
        print(comments.extract())
        print("")

def main():
    if len(argv) != 2:
        print("\n[-] Usage: python {} <URL>\n".format(path.basename(__file__)))
        exit(0)
    url = argv[1]
    soup = get_soup(url)
    get_comments(soup)

main()
