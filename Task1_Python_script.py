import os
import sys
import requests
import re
from bs4 import BeautifulSoup  # Make sure this module is installed

# function to get the html source text of the website article
def get_page():
    # Ask the user to input "Enter the URL of an article: " and collect it in url
    url = input("Enter the URL of an article: ")

    # Call get method in requests object, pass url and collect it in res
    res = requests.get(url)

    # Check if the request was successful
    if res.status_code != 200:
        print('Failed to retrieve the page. Please check the URL and try again.')
        sys.exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')
    return soup, url

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub(r'<(.*?)>', '', text)
    return text

def collect_text(soup, url):
    text = f'url: {url}\n\n'
    # Collect text differently depending on the site structure
    if "crummy.com" in url:
        # For BeautifulSoup documentation, let's get text from <p> and <li> tags as they contain useful info
        elements = soup.find_all(['p', 'li'])
    else:
        # Default to <p> tags
        elements = soup.find_all('p')
        
    for elem in elements:
        text += f"{elem.text}\n\n"
    return text

# function to save file in the current directory
def save_file(text, url):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1] if '/' in url else url
    fname = f'scraped_articles/{name}.txt'
    
    # write a file using with
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    soup, url = get_page()
    text = collect_text(soup, url)
    save_file(text, url)
