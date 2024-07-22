from math import ceil
import matplotlib.pyplot as plt
import pandas as pd

data_drz_file = "python_files\\get_data\\data_drz.csv"
data_drz_df = pd.read_csv(data_drz_file,sep=";")
nb_graphs = len(data_drz_df.columns)-1
for i in range(nb_graphs) :
    if data_drz_df.columns[i] != "insee" : 
        plt.subplot(2,int(ceil(nb_graphs/2)),i+1)
        temp = data_drz_df[data_drz_df.columns[i]]
        plt.hist(temp,bins=20)
        plt.title(data_drz_df.columns[i])
plt.show()
