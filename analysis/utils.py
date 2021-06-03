import pandas as pd


def aggregate_goal_contributions(df):
	"""
	aggregate goal contibutors
	"""
	df = df[['player', 'goal_contribution', 'goals', 'assists', 'minutes_played']]

	aggregates = df.groupby(['player']).agg('sum').sort_values(
		by=['goal_contribution', 'goals', 'assists'], ascending=False)
	aggregates['minutes_per_goal_contibution'] = aggregates['minutes_played'] / aggregates['goal_contribution']
	aggregates = aggregates.round(1)

	return aggregates.reset_index()
