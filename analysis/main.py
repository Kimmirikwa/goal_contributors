import pandas as pd

import utils

BIG_6 = ['Man City', 'Man Utd', 'Liverpool', 'Chelsea', 'Spurs', 'Arsenal']


def aggregate_goal_involvements(df, filename):
	goal_involvement_aggregates = utils.aggregate_goal_involvements(df)
	goal_involvement_aggregates.to_csv(
		"output/goal_involvements/{}.csv".format(filename), index=False)


if __name__ == "__main__":
	data = pd.read_csv("../data/Premier League_scorers.csv")
	data.fillna(0, inplace=True)

	# goal_contibution = goals + assists
	data['goal_involvement(goals + assists)'] = data['goals'] + data['assists']

	# minutes as int
	data['minutes_played'] = data.apply(lambda row: int(row['minutes_played'][:-1]), axis=1)

	# add games played column
	# the values should be 1 but will be summed per player to get the total count
	data['games_played'] = 1

	# overall scorers and assiter aggregates
	aggregate_goal_involvements(data, "against_all_teams")

	# scorers or assisters against top 10 teams
	aggregate_goal_involvements(data[data['opponent_position'] <= 10], "against_top_10")

	# scorers or assisters against bottom 10 teams
	aggregate_goal_involvements(data[data['opponent_position'] >= 11], "against_bottom_10")

	# scorers or assisters against top 4 teams
	aggregate_goal_involvements(data[data['opponent_position'] <= 4], "against_top_4")

	# scorers or assisters against relegated teams
	aggregate_goal_involvements(data[data['opponent_position'] >= 18], "against_relegated")

	# scorers or assisiters against 'the big 6'
	aggregate_goal_involvements(data[data.opponent.isin(BIG_6)], "against_traditional_big_6")

