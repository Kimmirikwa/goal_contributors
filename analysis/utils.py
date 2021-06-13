import pandas as pd
import numpy as np

VENUE_GOALS = {
	'A': 'away_goals',
	'H': 'home_goals'
}


def aggregate_goal_involvements(df):
	"""
	aggregate goal contibutors
	"""
	df_to_aggregate = df[['player', 'goal_involvement(goals + assists)', 'goals', 'assists', 'minutes_played', 'games_played']]

	aggregates = df_to_aggregate.groupby(['player']).agg('sum').sort_values(
		by=['goal_involvement(goals + assists)', 'goals', 'assists'], ascending=False)
	# avoid division by zero
	# we are also only intrested in players that scored or assisted
	aggregates = aggregates[aggregates['goal_involvement(goals + assists)'] > 0]
	aggregates['minutes_per_goal_involvement'] = aggregates['minutes_played'] / aggregates['goal_involvement(goals + assists)']
	aggregates['games_per_goal_involvement'] = aggregates['games_played'] / aggregates['goal_involvement(goals + assists)']
	aggregates['minutes_per_goal'] = aggregates['minutes_played'] / aggregates['goals']
	aggregates['games_per_assist'] = aggregates['games_played'] / aggregates['assists']
	aggregates = aggregates.round(1)
	aggregates.reset_index(inplace=True)

	venue_goals_aggregates = get_goals_by_venue(df[['player', 'venue', 'goals']])

	aggregates = pd.merge(aggregates, venue_goals_aggregates, left_on='player', right_on='player')

	return aggregates


def get_goals_by_venue(df_for_venues):
	df_for_venues['venue'] = df_for_venues.apply(lambda row: VENUE_GOALS[row['venue']], axis=1)
	venue_goals_aggregates = pd.pivot_table(
		df_for_venues, index=['player'], columns=['venue'], values='goals', aggfunc=np.sum)
	return venue_goals_aggregates


def aggregate_goals_types(df):
	df = df[['player', 'goal_type']]
	df['number_goals'] = 1

	aggregates = df.groupby(['player', 'goal_type']).agg('sum')
	aggregates.reset_index(inplace=True)
	aggregates = pd.pivot_table(aggregates, index=['player'], columns=['goal_type'], values='number_goals', aggfunc=np.sum)
	aggregates.fillna(0, inplace=True)

	return aggregates
