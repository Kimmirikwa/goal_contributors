import re
import requests

import pandas as pd
from bs4 import BeautifulSoup


home_url = "https://www.transfermarkt.com"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


def get_soup(url):
	"""
	parses the soup object from the downloaded content
	"""
	page = requests.get(url, headers=headers)

	return BeautifulSoup(page.content, 'html.parser')


def get_league_link(soup, league):
	print("Getting the link for {}".format(league))
	h2_tags = soup.findAll('h2')
	epl_link = None
	for header in h2_tags:
		link = header.find('a')['href']
		if league in link:
			return link


def get_league_table(league_soup):
	print("Getting the league table")
	tables = league_soup.findAll('table')
	epl_table = None

	for table in tables:
		thead = table.find('thead')
		if not thead:
			continue
		ths = thead.findAll('th')
		if ths[-1].text == 'Pts':
			epl_table = table
			break

	tbody = epl_table.find('tbody')
	team_rows = tbody.findAll('tr')

	return [team_row.findAll('td')[2].text.strip() for team_row in team_rows]


def get_stats_uris(stats_soup):
	print("Getting the league stats")
	li_tags = stats_soup.findAll('li', {'class': 'page'})
	stats_uris = [li_tag.find('a')['href'] for li_tag in li_tags]
	return stats_uris


def get_players_stats_urls(stats_uris):
	print("Getting the player stats url")
	players_stats_urls = []
	for stats_uri in stats_uris:
		stats_url = home_url + stats_uri
		stats_soup = get_soup(stats_url)

		tables = stats_soup.findAll('table')
		scorers_table = None

		for table in tables:
			thead = table.find('thead')
			if not thead:
				continue
			ths = thead.findAll('th')
			if len(ths) == 7:
				scorers_table = table
				break

		tbody = scorers_table.find('tbody')
		scorer_rows = tbody.findAll('tr', {"class": re.compile(r'(odd)|(even)')})
		for scorer_row in scorer_rows:
			player = scorer_row.find('td', {'class': 'hauptlink'})
			player_url = home_url + player.find('a')['href']
			player_soup = get_soup(player_url)
			player_stats_url = player_soup.find('a', text='View full stats')['href']
			players_stats_urls.append({
				'player': player.text.strip(),
				'url': player_stats_url
				})
	return players_stats_urls


def get_all_goals_urls(players_scorers_urls):
	return [{
		'player': url['player'],
		'url': url['url'].replace("leistungsdaten", "alletore")
		} for url in players_scorers_urls]


def get_scorers_df(players_stats_urls, league_name, league_table):
	print("Getting the scorers stats")
	df = pd.DataFrame()
	for player_stats_url in players_stats_urls:
		url = home_url + player_stats_url['url']
		print(url)
		stats_soup = get_soup(url)
		table_divs = stats_soup.findAll('div', {'class': 'box'})
		stats_table = None
		for table_div in table_divs:
			league = table_div.find('div').text
			if league_name not in league:
				continue
			stats_table = table_div.find('table')
			break

		columns = ['match_day', 'date', 'venue', 'player', 'team', 'opponent', 'opponent_position', 'result', 'goals', 'assists', 'minutes_played']
		try:
			tbody = stats_table.find('tbody')
			rows = tbody.findAll('tr')
			data = []
			for row in rows:
				cells = row.findAll('td')
				if len(cells) < 13:
					continue
				team = cells[3].find('img', alt=True)['alt']
				opponent = cells[6].find('a').text.strip()
				data.append(
					[cells[0].text.strip(), cells[1].text.strip(), cells[2].text.strip(), player_stats_url['player'], team, opponent, league_table.index(opponent) + 1, cells[7].text.strip(), cells[9].text.strip(), cells[10].text.strip(), cells[14].text.strip()])
		except Exception as e:
			continue


		df = pd.concat([df, pd.DataFrame(data, columns=columns)])

	return df


def get_goal_types(urls, league):
	df = pd.DataFrame()
	columns = ['league', 'player', 'team_venue_goal_number', 'opponent_position', 'final_score', 'minute', 'current_score', 'goal_type']
	for url in urls:
		goals_soup = get_soup(home_url + url['url'])
		tables = goals_soup.findAll('table')
		goals_table = None

		for table in tables:
			thead = table.find('thead')
			if not thead:
				continue
			ths = thead.findAll('th')
			if ths[-1].text == 'Type of goal':
				goals_table = table
				break

		season_row = goals_table.find("td", text="Season 20/21").parent
		rows = season_row.find_all_next("tr")
		opponent = None
		venue = None
		goal_number = None
		data = []
		for row in rows:
			try:
				cells = row.findAll("td")
				if row.parent != season_row.parent:
					break
				if not cells:
					continue
				if len(cells) == 4:
					if current_league != league:
						continue
					goal_number += 1
				elif cells[0].find('img')['title'].strip() == league:
					opponent_and_position = cells[6].text.split()
					opponent = " ".join(opponent_and_position[:-1])
					opponent_position = opponent_and_position[-1]
					for char in "(.)":
						opponent_position = re.sub("\\{}".format(char), '', opponent_position)
					venue = cells[2].text.strip()
					goal_number = 1
					final_score = cells[7].text.strip()
				else:
					current_league = cells[0].find('img')['title'].strip()
					continue
			except Exception as e:
				continue
			data.append([
					league, url['player'], "{}_{}_{}".format(opponent, venue, goal_number), opponent_position, final_score, cells[-3].text.strip(), cells[-2].text.strip(), cells[-1].text.strip()])
		df = pd.concat([df, pd.DataFrame(data, columns=columns)])

	return df


# df = get_goal_types([{"player": "Harry Kane", "url": "/harry-kane/alletore/spieler/132098"}], "Premier League")
# print(df.head())

