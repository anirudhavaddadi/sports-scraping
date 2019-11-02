from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# NBA season we will be pulling in
year = 2020
month = "november"

# URL page we will scraping
url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year, month)

# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html)

# use findALL() to get the column headers
soup.findAll('tr', limit=2)
# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

# The first column (date) is a different class than the rest of the columns.
# So break up headers into two separate lists below.
date_col = headers[0:0]
headers = headers[1:]
print(date_col)
print(headers)

# Get data and avoid the first header row
rows = soup.findAll('tr')[1:]
games = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
dates = [[td.getText() for td in rows[i].findAll('left')]
            for i in range(len(rows))]

print(games)
games = pd.DataFrame(games, columns = headers)
dates = pd.DataFrame(games, columns = date_col)
games.head(10)
dates.head(10)
