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


def get_stats_function(stats):
	functions = {
		'scorers': utils.get_scorers_df,
		'all_goals': utils.get_goal_types
	}

	return functions[stats]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process leauge top scorers')
	parser.add_argument('--league_link_name', default='premier', help='the name to use to get the league link')
	parser.add_argument('--stats', default='all_goals', help="the statistics to get")
	args = parser.parse_args()
	soup = utils.get_soup(home_url)

	league_link = home_url + utils.get_league_link(soup, args.league_link_name)
	league_soup = utils.get_soup(league_link)

	league_table = utils.get_league_table(league_soup)

	stats_url = home_url + league_soup.find('a', title="View stats")['href']
	stats_soup = utils.get_soup(stats_url)
	scorers_uris = utils.get_player_scorers_uris(stats_soup)

	players_scorers_urls = utils.get_players_stats_urls(scorers_uris)
	players_all_goals_urls = utils.get_all_goals_urls(players_scorers_urls)

	stats_function = get_stats_function(args.stats)
	league_name = LEAGUE_TABLES[args.league_link_name]
	df = stats_function(players_all_goals_urls, LEAGUE_TABLES[args.league_link_name])
	df.to_csv("data/{}_{}.csv".format(league_name, args.stats), index=False)
