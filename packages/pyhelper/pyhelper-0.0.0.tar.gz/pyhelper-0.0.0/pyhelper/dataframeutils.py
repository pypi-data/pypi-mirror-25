# coding=utf-8

import pandas as pd


def df_len(df):
    return 0 if df is None else len(df)


def df_merge(df1, df2):
    """
    根据索引将df2中的新数据行追加到df1
    :param df1:
    :param df2:
    :return:
    """
    return pd.concat([df1, df2[~df2.index.isin(df1.index)]])
