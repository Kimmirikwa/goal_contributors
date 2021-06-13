import pandas as pd
import numpy as np


def aggregate_goal_involvements(df):
	"""
	aggregate goal contibutors
	"""
	df = df[['player', 'goal_involvement(goals + assists)', 'goals', 'assists', 'minutes_played', 'games_played']]

	aggregates = df.groupby(['player']).agg('sum').sort_values(
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

	return aggregates


def aggregate_goals_types(df):
	df = df[['player', 'goal_type']]
	df['number_goals'] = 1

	aggregates = df.groupby(['player', 'goal_type']).agg('sum')
	aggregates.reset_index(inplace=True)
	aggregates = pd.pivot_table(aggregates, index=['player'], columns=['goal_type'], values='number_goals', aggfunc=np.sum)
	aggregates.fillna(0, inplace=True)

	return aggregates
