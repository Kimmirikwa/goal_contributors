import re
import requests
import argparse

from bs4 import BeautifulSoup
import pandas as pd

import utils


home_url = "https://www.transfermarkt.com"

LEAGUE_TABLES = {
	"premier": "Premier League",
	"laliga": "LaLiga",
	"serie": "Serie A",
	"bundesliga": "Bundesliga"
}

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process leauge top scorers')
	parser.add_argument('--league_link_name', default='laliga', help='the name to use to get the league link')
	args = parser.parse_args()
	soup = utils.get_soup(home_url)

	league_link = home_url + utils.get_league_link(soup, args.league_link_name)
	league_soup = utils.get_soup(league_link)

	league_table = utils.get_league_table(league_soup)

	stats_url = home_url + league_soup.find('a', title="View stats")['href']
	stats_soup = utils.get_soup(stats_url)
	stats_uris = utils.get_stats_uris(stats_soup)

	players_stats_urls = utils.get_players_stats_urls(stats_uris)

	df = utils.get_scorers_df(players_stats_urls, LEAGUE_TABLES[args.league_link_name], league_table)

	df.fillna(0, inplace=True)
	df.to_csv("data/{}_scorers.csv".format(args.league_link_name), index=False)
