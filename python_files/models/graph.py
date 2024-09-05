import get_train_test_val as gt
import matplotlib.pyplot as plt
from math import ceil

df_data = gt.get_data()
df_results = gt.get_results()

X = df_data["area"]
Y = df_results["er_idf"]

nb = len(df_data.columns)
liste_col = list(df_data.columns)
for i in range(nb):
    plt.subplot(3, ceil(nb/3),i+1)
    col_name = liste_col[i]
    X = df_data[col_name]
    plt.scatter(X,Y)
    plt.xlabel(col_name)
plt.show()

