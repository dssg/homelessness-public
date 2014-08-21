"""A module with a few helpful diagnostic tools.

"""
import pandas as pd

def unique_summary(df, subset):
    """Given a dataframe and a subset of columns, print a summary of unique rows

    :param df: The dataframe to inspect.
    :type df: Dataframe.
    :subset df: The subset of columns to consider.
    :type df: array-like.

    """
    total = len(df)
    unique = len(df.drop_duplicates(subset=subset))
    print "Total rows: {}".format(total)
    print "Unique rows: {}".format(unique)
    print "Unaccounted-for rows: {}".format(total-unique)

def null_summary(df):
    """Given a dataframe, print a summary of null values for each column

    :param df: The dataframe to inspect.
    :type df: Dataframe.

    """
    for column in df.columns:
        print column
        print count_nulls(df[column])

def count_nulls(s):
    """Given a series, return a summary of null values for that series

    :param s: The series to inspect.
    :type s: Series.

    """
    count = len(s[pd.isnull(s)])
    percent = 100 * float(len(s[pd.isnull(s)])) / len(s)
    return "**NaNs:** " + str(count) + " / " + str(int(percent)) + "%"

def generate_sankey(df, left, right):
    """Given a dataframe, a left column, and a right column, print the input for `SankeyMATIC <http://sankeymatic.com>`_.

    :param df: The dataframe to use.
    :type df: Dataframe.
    :param left: The left column to use.
    :type left: str.
    :param right: The right column to use.
    :type right: str.

    """
    grouped = df[[left, right]].dropna().groupby([left, right])
    for group, rows in grouped.groups.iteritems():
        print "{} [{}] {}".format(group[0], len(rows), group[1])
