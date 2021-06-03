import pandas as pd


def get_top_half_goal_contributions(df):
	"""
	get goal contibutions against teams that finished in the top half
	"""
	top_half_df = df[df['opponent_position'] <= 10]
	top_half_df = top_half_df[['player', 'goal_contribution', 'goals', 'assists', 'minutes_played']]

	aggregates = top_half_df.groupby(['player']).agg('sum').sort_values(
		by=['goal_contribution', 'goals', 'assists'], ascending=False)
	aggregates['minutes_per_goal_contibution'] = aggregates.apply(lambda row: row['minutes_played'] / row['goal_contribution'], axis=1)

	return aggregates