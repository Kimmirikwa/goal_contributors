import pandas as pd

import utils

BIG_6 = ['Man City', 'Man Utd', 'Liverpool', 'Chelsea', 'Spurs', 'Arsenal']


def aggregate_attack_stats(goal_involvements_df, goal_types_df, filename):
	goal_involvement_aggregates = utils.aggregate_goal_involvements(goal_involvements_df)
	goal_types_aggregates = utils.aggregate_goals_types(goal_types_df)
	attack_aggregates = pd.merge(goal_involvement_aggregates, goal_types_aggregates, left_on='player', right_on='player')
	attack_aggregates.to_csv(
		"output/goal_involvements/{}.csv".format(filename), index=False)


if __name__ == "__main__":
	goal_involvements_df = pd.read_csv("../data/Premier League_scorers.csv")
	goal_involvements_df.fillna(0, inplace=True)

	# goal_contibution = goals + assists
	goal_involvements_df['goal_involvement(goals + assists)'] = goal_involvements_df['goals'] + goal_involvements_df['assists']

	# minutes as int
	goal_involvements_df['minutes_played'] = goal_involvements_df.apply(lambda row: int(row['minutes_played'][:-1]), axis=1)

	# add games played column
	# the values should be 1 but will be summed per player to get the total count
	goal_involvements_df['games_played'] = 1

	# goal types dataframe
	goal_types_df = pd.read_csv("../data/Premier League_all_goals.csv")
	goal_types_df['opponent'] = goal_types_df.apply(lambda row: row['team_venue_goal_number'].split("_")[0], axis=1)

	# overall scorers and assiter aggregates
	aggregate_attack_stats(goal_involvements_df, goal_types_df, "against_all_teams")

	# scorers or assisters against top 10 teams
	aggregate_attack_stats(
		goal_involvements_df[goal_involvements_df['opponent_position'] <= 10], goal_types_df[goal_types_df['opponent_final_position'] <= 10], "against_top_10")

	# scorers or assisters against bottom 10 teams
	aggregate_attack_stats(
		goal_involvements_df[goal_involvements_df['opponent_position'] >= 11], goal_types_df[goal_types_df['opponent_final_position'] >= 11], "against_bottom_10")

	# scorers or assisters against top 4 teams
	aggregate_attack_stats(
		goal_involvements_df[goal_involvements_df['opponent_position'] <= 4], goal_types_df[goal_types_df['opponent_final_position'] <= 4], "against_top_4")

	# scorers or assisters against relegated teams
	aggregate_attack_stats(
		goal_involvements_df[goal_involvements_df['opponent_position'] >= 18], goal_types_df[goal_types_df['opponent_final_position'] >= 18], "against_relegated")

	# scorers or assisiters against 'the big 6'
	aggregate_attack_stats(
		goal_involvements_df[goal_involvements_df.opponent.isin(BIG_6)], goal_types_df[goal_types_df.opponent.isin(BIG_6)], "against_traditional_big_6")

