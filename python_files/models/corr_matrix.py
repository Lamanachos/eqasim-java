import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import attributes as attrib

def matrix(only_data = True):
    df = pd.read_csv(attrib.data_file,sep=";")
    df.drop(columns = ["insee"],inplace=True)
    df.drop(columns = ["density"],inplace=True)
    new_df = pd.DataFrame()
    col_div = "area"
    skip = ["density","cars_per_person","ms_walk_bs","coeff_join"]

    for col in df.columns :
        if (col != col_div) and (col not in skip) and (col_div != None):
            temp = df[col]/df[col_div]
            new_df[col] = temp
        else :
            new_df[col] = df[col]
    if not only_data :
        temp_df = pd.read_csv(attrib.results_file,sep=";")
        temp_df.drop(columns = ["insee"],inplace=True)
        for col in temp_df.columns :
            new_df[col] = temp_df[col]
    print(new_df)
    matrix = new_df.corr()

    # plotting correlation matrix
    sns.heatmap(matrix, cmap="coolwarm", annot=True)
    plt.show()

matrix(False)