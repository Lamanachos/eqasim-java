import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("python_files\\get_graphes\\eval_models.csv",sep=";")
models = data["model"]

fig = plt.figure()
axes = fig.add_subplot()
X1 = data["rmse_all"]
Y1 = data["mae_all"]
axes.scatter(X1,Y1,color = "blue",marker = "o",label = "Entraînement et évaluation sur toutes les sorties")

X2 = data["rmse_idf"]
Y2 = data["mae_idf"]
axes.scatter(X2,Y2,color = "red",marker = "x",label = "Entraînement et évaluation sur les sorties au niveau de l'IDF")
axes.set_xlabel("RMSE")
axes.set_ylabel("MAE")

for i, txt in enumerate(models):
    axes.text(X1[i]+0.005,Y1[i]+0.005,txt,fontsize = 10)
    axes.text(X2[i]+0.005,Y2[i]+0.005,txt,fontsize = 10)
axes.set_title("MAE et RMSE des différents modèles entraînés et évalués sur différentes sorties")
plt.legend()
plt.show()