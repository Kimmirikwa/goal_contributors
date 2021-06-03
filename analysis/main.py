import pandas as pd

import utils


if __name__ == "__main__":
	data = pd.read_csv("../data/premier_scorers.csv")
	data.fillna(0, inplace=True)

	# goal_contibution = goals + assists
	data['goal_involvement(goals + assists)'] = data['goals'] + data['assists']

	# minutes as int
	data['minutes_played'] = data.apply(lambda row: int(row['minutes_played'][:-1]), axis=1)

	# add games played column
	# the values should be 1 but will be summed per player to get the total count
	data['games_played'] = 1

	# overall scorers and assiter aggregates
	goal_contibutor_aggregates = utils.aggregate_goal_involvements(data)
	goal_contibutor_aggregates.to_csv("output/goal_contibutor_aggregates.csv", index=False)

	# scorers or assisters agains top 10 teams
	contributors_against_top_10_teams = utils.aggregate_goal_involvements(
		data[data['opponent_position'] <= 10])
	contributors_against_top_10_teams.to_csv("output/contributors_against_top_10_teams.csv", index=False)

	# scorers or assisters against bottom 10 teams
	contributors_against_bottom_10_teams = utils.aggregate_goal_involvements(
		data[data['opponent_position'] >= 11])
	contributors_against_bottom_10_teams.to_csv("output/contributors_against_bottom_10_teams.csv", index=False)

	# scorers or assisters agains top 4 teams
	contributors_against_top_4_teams = utils.aggregate_goal_involvements(
		data[data['opponent_position'] <= 4])
	contributors_against_top_4_teams.to_csv("output/contributors_against_top_4_teams.csv", index=False)
