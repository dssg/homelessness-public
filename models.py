"""A module with commonly- and uncommonly-used Weka classifiers.

To be used primarily with :mod:`pipeline`.

"""

random_forest_small = 'trees.RandomForest -I 5'
random_forest = 'trees.RandomForest'
random_forest_large = 'trees.RandomForest -I 100'

decision_tree = 'trees.J48'
decision_tree_pruned = 'trees.J48 -M 50'

logistic_small = 'functions.Logistic -M 10'
logistic = 'functions.Logistic'

