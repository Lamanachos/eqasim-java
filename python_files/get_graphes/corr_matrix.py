import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import attributes as attrib

def matrix(only_data = True, col_div = None):
    plt.clf()
    if col_div != None :
        new_df = attrib.div_data_by_column(col_div=col_div)
    else : 
        new_df = attrib.get_data()
    if not only_data :
        temp_df = pd.read_csv(attrib.results_file,sep=";")
        temp_df.drop(columns = ["insee"],inplace=True)
        for col in temp_df.columns :
            new_df[col] = temp_df[col]
    new_df.drop(columns=["insee"],inplace=True)
    matrix = new_df.corr()
    # plotting correlation matrix
    sns.heatmap(matrix, cmap="coolwarm", annot=True)
    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    figure.tight_layout()
    if col_div == None :
        plt.savefig("python_files\\get_graphes\\mat_corr.png",dpi = 300)
    else : 
        plt.savefig("python_files\\get_graphes\\mat_corr_div_"+col_div+".png",dpi = 300)

matrix(False, col_div=None)