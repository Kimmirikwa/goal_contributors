import pandas as pd


def get_top_half_goal_contributions(df):
	top_half_df = df[df['opponent_position'] <= 10]
	top_half_df = top_half_df[['player', 'goal_contribution', 'goals', 'assists']]

	return top_half_df.groupby(['player']).agg('sum').sort_values(
		by=['goal_contribution', 'goals', 'assists'], ascending=False)