import pandas as pd


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
	aggregates = aggregates.round(1)
	aggregates.reset_index(inplace=True)

	return aggregates
