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

		columns = ['player', 'team', 'team_position', 'opponent', 'opponent_position', 'goals', 'assists']
		try:
			tbody = stats_table.find('tbody')
			rows = tbody.findAll('tr')
			data = []
			for row in rows:
				cells = row.findAll('td')
				if len(cells) < 13:
					continue
				team = cells[6].find('a').text.strip()
				opponent = cells[6].find('a').text.strip()
				data.append([player_stats_url['player'], team, league_table.index(team) + 1, opponent, league_table.index(team) + 1, cells[9].text, cells[10].text])
		except Exception as e:
			continue


		df = pd.concat([df, pd.DataFrame(data, columns=columns)])

	return df
