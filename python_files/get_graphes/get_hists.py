from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
import attributes as attrib

drz_df = attrib.get_results()
#drz_df = attrib.get_data()
divide_by = None
all_in = False
nb_graphs = len(drz_df.columns)
ind = 1
for col in drz_df.columns :
    if col != "insee" : 
        if not all_in :
            plt.subplot(3,int(ceil(nb_graphs/3)),ind)
            plt.title(col)
        if divide_by != None :
            temp = drz_df[col]/drz_df[divide_by]
        else :
            temp = drz_df[col]
        plt.hist(temp,bins=30)
        ind += 1
plt.show()
