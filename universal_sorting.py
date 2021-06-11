import pandas as pd
import json
import sys, os
import itertools
from tqdm import tqdm

""" Read in KEGG compounds, sort by molecular weight
    Input: filepath to KEGG cpds & molweights
    Output: dataframe, sorted by molweight (lowest to highest)
"""
def sort_KEGG_cpds_mw(fp):
    df = pd.read_csv(fp)
    df = df.sort_values('Mol_Weight')
    return df

""" Read in KEGG compounds, sort by universality (within metagenomes)
    Input: filepath to KEGG cpds & metagenome occurance count
    Output: dataframe, sorted by universality (highest to lowest)
"""
def sort_KEGG_cpds_universality(fp):
    df = pd.read_csv(fp, names=["C", "Occurance"])
    df = df.sort_values("Occurance", ascending=False)
    return df

""" Sort compounds by molecular weight
    Input: list of compounds to sort, KEGG dataframe of molweight-sorted compounds, metagenome id
    Output: sorted list of compounds, in lightest-to-heaviest order
"""
def sort_mw(cpds, KEGG_mw_df, id):
    sub_df = KEGG_mw_df[KEGG_mw_df["C"].isin(cpds)]
    sub_df["C"].to_csv("data/MW/mw_"+str(id)+".txt", header=None, index=None, mode="a")

""" Sort compounds by universality
    Input: list of compounds to sort, KEGG dataframe of universal-ordered compounds (by metagenome occurance), metagenome id
    Output: sorted list of compounds, in most-to-least universal order
"""
def sort_universality(cpds, KEGG_universal_df, id):
    sub_df = KEGG_universal_df[KEGG_universal_df["C"].isin(cpds)]
    sub_df["C"].to_csv("data/Universality/u_"+str(id)+".txt", header=None, index=None, mode="a")


def main():
    #Set all columns visible
    pd.set_option('display.max_columns', None)
    #Read in random 100 metagenome sample
    df = pd.read_csv("data/Metagenome_Elements.csv")
    #Read in molecular weight and universality orders of KEGG
    KEGG_mw_df = sort_KEGG_cpds_mw("data/chiral_molweight_formula_labels.csv")
    KEGG_universal_df = sort_KEGG_cpds_universality("data/metagenome_occurance.csv")

    #Molecular weight sorting
    df.apply(lambda x: sort_mw(eval(x["compounds"]), KEGG_mw_df, x["Unnamed: 0"]), axis=1)
    #Universality sorting
    df.apply(lambda x: sort_universality(eval(x["compounds"]), KEGG_universal_df, x["Unnamed: 0"]), axis=1)

    #Testing
    # row1 = df.iloc[1]
    # sort_mw(eval(row1["compounds"]), KEGG_mw_df, row1["Unnamed: 0"])
    # sort_universality(eval(row1["compounds"]), KEGG_universal_df, row1["Unnamed: 0"])



if __name__ == "__main__":
    main()
