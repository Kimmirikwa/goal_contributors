import pandas as pd

import utils


if __name__ == "__main__":
	data = pd.read_csv("../data/premier_scorers.csv")
	data.fillna(0, inplace=True)

	# goal_contibution = goals + assists
	data['goal_contribution'] = data.apply(lambda row: row['goals'] + row['assists'], axis=1)
	print(data.head())

	# minutes as int
	data['minutes_played'] = data.apply(lambda row: int(row['minutes_played'][:-1]), axis=1)

	top_half = utils.get_top_half_goal_contributions(data)
	print(top_half.head(10))