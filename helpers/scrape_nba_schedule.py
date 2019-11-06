from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 1000)

def run():
    # Take month and year as inputs
    season_year = 2020
    month = "november"

    today = datetime.date(datetime.now())
    yesterday = today - timedelta(days=1)
    today_one_week = today + timedelta(days=7)

    cutoff_time_est = dt.time(22, 0, 0)


    # URL page we will scraping
    url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(season_year, month)

    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

    # The first column (date) is a different class than the rest of the columns.
    # So break up headers into two separate lists below.
    date_col = headers[:1]
    headers = headers[1:]

    # Get data and avoid the first header row
    rows = soup.findAll('tr')[1:]
    games = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    dates = [[th.getText() for th in rows[i].findAll('th')]
                for i in range(len(rows))]

    games = pd.DataFrame(games, columns = headers)
    dates = pd.DataFrame(dates, columns = date_col)

    # Merge dates with rest of data on index to get full month schedule
    full_month_schedule = dates.merge(games, left_index=True, right_index=True)

    # Clean column names and only keep relevant columns
    full_month_schedule.rename(columns={'Date':'date_est_str',
                              'Start (ET)':'start_time_est_str',
                              'Visitor/Neutral':'visitor_team',
                              'Home/Neutral':'home_team'},
                               inplace=True)
    full_month_schedule = full_month_schedule[['date_est_str', 'start_time_est_str', 'visitor_team', 'home_team']]

    # Extract date and time from string columns
    full_month_schedule['date_est'] = pd.to_datetime(full_month_schedule['date_est_str'])
    full_month_schedule['start_time_est']=full_month_schedule.start_time_est_str.str[:-1]
    full_month_schedule['start_time_est'] = pd.to_datetime(full_month_schedule['start_time_est'], format= '%H:%M').dt.time
    full_month_schedule['start_time_est'] = full_month_schedule['start_time_est'].apply(lambda x: (dt.datetime.combine(dt.datetime(1,1,1), x,) + dt.timedelta(hours=12)).time())

    # Keep only the next week of data. Since dates are based on EST, we need to include yesterday as well.
    next_week_schedule = full_month_schedule.loc[full_month_schedule['date_est'] <= today_one_week]
    next_week_schedule = next_week_schedule.loc[next_week_schedule['date_est'] >= yesterday]

    # Remove games that are on Friday and Saturday night (I am not planing on coming to the office on the weekend to watch)
    next_week_schedule['day_of_week'] = next_week_schedule['date_est'].dt.dayofweek
    next_week_schedule = next_week_schedule[(next_week_schedule['day_of_week'] != 4) & (next_week_schedule['day_of_week'] != 5)]

    # Only keep games that start after a set cutoff time
    next_week_schedule = next_week_schedule[(next_week_schedule['start_time_est'] >= cutoff_time_est)]
    next_week_schedule = next_week_schedule[['date_est', 'start_time_est', 'visitor_team', 'home_team']]

    # Generate IST columns
    next_week_schedule['date_time_est'] = next_week_schedule.apply(lambda r : pd.datetime.combine(r['date_est'],r['start_time_est']),1)
    next_week_schedule['hours_add'] = 9.5
    next_week_schedule['hours_add'] = pd.to_timedelta(next_week_schedule['hours_add'],'h')
    next_week_schedule['date_time_ist'] = next_week_schedule['date_time_est'] + next_week_schedule['hours_add']
    next_week_schedule['date_ist'] = [d.date() for d in next_week_schedule['date_time_ist']]
    next_week_schedule['time_ist'] = [d.time() for d in next_week_schedule['date_time_ist']]

    return next_week_schedule

output = run()

print(output)

'''
Need to still do the following:
- Loop to generate two months of games before filtering
'''
