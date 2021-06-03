import pandas as pd

import utils


if __name__ == "__main__":
	data = pd.read_csv("../data/premier_scorers.csv")
	data.fillna(0, inplace=True)

	# goal_contibution = goals + assists
	data['goal_contribution'] = data['goals'] + data['assists']

	# minutes as int
	data['minutes_played'] = data.apply(lambda row: int(row['minutes_played'][:-1]), axis=1)

	contibutors_against_top_10_teams = utils.aggregate_goal_contributions(
		data[data['opponent_position'] <= 10])
	contibutors_against_top_10_teams.to_csv("output/contibutors_against_top_10_teams.csv", index=False)
