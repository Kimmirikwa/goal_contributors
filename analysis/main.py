import pandas as pd

import utils


if __name__ == "__main__":
	data = pd.read_csv("../data/premier_scorers.csv")

	# goal_contibution = goals + assists
	data['goal_contribution'] = data.apply(lambda row: row['goals'] + row['assists'], axis=1)

	top_half = utils.get_top_half_goal_contributions(data)
	print(top_half.head(10))