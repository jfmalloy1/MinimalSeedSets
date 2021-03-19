import json
import pandas as pd
from tqdm import tqdm
import os

""" Finds minimal seeds (scope_seeds) and size of OG seed set (scope_compounds)
    Input: filepath to json filepath
    Output: pandas series which can be added to an existing dataframe
"""
def analyze_json(fp):
    data = json.load(open(fp))
    #Get metagenome id 
    id = fp[9:19]
    #Return relevant data
    return pd.Series({"ID": id,
        "Seed Size": len(data["stats"]["scope_compounds"]),
        "MSS Size": len(data["stats"]["scope_seeds"]),
        "MSS Compounds": data["stats"]["scope_seeds"]})

def main():
    # #Test
    # test_series = analyze_json("output/mw3300036539/output.json")
    # df = df.append(test_series, ignore_index=True)
    # print(df)

    #Set up dataframe
    df = pd.DataFrame(columns=["ID", "Seed Size", "MSS Size", "MSS Compounds"])
    #Sorting by molecular weight results
    for dir in tqdm(os.listdir("output")):
        if dir.startswith("mw"):
            test_series = analyze_json("output/" + dir + "/output.json")
            df = df.append(test_series, ignore_index=True)

    print(df)
    df.to_csv("output/MSSresults_mw.csv")

if __name__ == "__main__":
    main()
