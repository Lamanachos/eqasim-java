import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import attributes as attrib

df = pd.read_csv(attrib.data_file,sep=";")
df.drop(columns = ["insee"],inplace=True)
df.drop(columns = ["density"],inplace=True)
new_df = pd.DataFrame()
col_div = "area"
skip = ["density","cars_per_person","ms_walk_bs","coeff_join"]

for col in df.columns :
    if (col != col_div) and (col not in skip) :
        temp = df[col]/df[col_div]
        new_df[col] = temp
    else :
        new_df[col] = df[col]
matrix = new_df.corr()

# plotting correlation matrix
sns.heatmap(matrix, cmap="Greens", annot=True)
plt.show()