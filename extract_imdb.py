import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setting up headless browsing (optional)
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# URL of the website to scrape
driver.get("https://www.imdb.com/chart/top")

# Initialize lists
title = []
year = []
duration = []
class_age = []
rating = []

# Get page content
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

def extract ():
    # Scrape titles
    for b in soup.find_all(attrs={'class': 'ipc-title-link-wrapper'}):
        name = b.find(attrs={'class': 'ipc-title__text'})
        if name:
            title.append(name.text)
        else:
            title.append("N/A")

    # Scrape years
    for c in soup.find_all(attrs={'class': 'cli-title-metadata'}):
        name2 = c.find_all('span')
        if len(name2) > 0:
            year.append(name2[0].text)
        else:
            year.append("N/A")

    # Scrape durations
    for d in soup.find_all(attrs={'class': 'cli-title-metadata'}):
        name3 = d.find_all('span')
        if len(name3) > 1:
            duration.append(name3[1].text)
        else:
            duration.append("N/A")

    # Scrape class_age
    for e in soup.find_all(attrs={'class': 'sc-ab348ad5-7 cqgETV cli-title-metadata'}):
        name4 = e.find_all('span')
        if len(name4) >= 3:
            class_age.append(name4[2].text)
        else:
            class_age.append("N/A")

    # Scrape ratings
    for f in soup.find_all(attrs={'class': 'cli-ratings-container'}):
        name5 = f.find_all('span')
        if len(name5) > 1:
            rating.append(name5[1].text)
        else:
            rating.append("N/A")

    # Ensure all lists are of the same length
    max_length = max(len(title), len(year), len(duration), len(class_age), len(rating))

    # Pad lists to match the maximum length
    while len(title) < max_length:
        title.append("N/A")
    while len(year) < max_length:
        year.append("N/A")
    while len(duration) < max_length:
        duration.append("N/A")
    while len(class_age) < max_length:
        class_age.append("N/A")
    while len(rating) < max_length:
        rating.append("N/A")

    # Create DataFrame
    df = pd.DataFrame({
        'title': title, 
        'year': year, 
        'duration': duration,
        'class_age': class_age,
        'rating': rating
    })
    #Remove row if whole column contain N/A sebab dio data lain tok termasuk nga mov list mari mano au
    df = df[(df.year != "N/A") & (df.duration != "N/A") & (df.class_age != "N/A") & (df.rating != "N/A")]
    # Close the browser
    driver.quit()
    return df

# RUN
if __name__ == "__main__":
    print(extract())
#print(df)