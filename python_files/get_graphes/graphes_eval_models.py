import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("python_files\\get_graphes\\eval_models.csv",sep=";")
models = data["model"]

fig = plt.figure()
axes = fig.add_subplot()
X1 = data["rmse_all"]
Y1 = data["r2_all"]
axes.scatter(X1,Y1,color = "blue",marker = "o",label = "Entraînement et évaluation sur toutes les sorties")

X2 = data["rmse_idf"]
Y2 = data["r2_idf"]
axes.scatter(X2,Y2,color = "red",marker = "x",label = "Entraînement et évaluation sur les sorties au niveau de l'Île-de-France")
axes.set_xlabel("RMSE",fontsize = 15)
axes.set_ylabel("R2", fontsize = 15)

for i, txt in enumerate(models):
    if txt != "svr_rbf" :
        axes.text(X1[i]+0.005,Y1[i]+0.005,txt,fontsize = 10)
        axes.text(X2[i]+0.005,Y2[i]+0.005,txt,fontsize = 10)
    else :
        axes.text(X1[i]-0.03,Y1[i]+0.005,txt,fontsize = 10)
        axes.text(X2[i]+0.005,Y2[i]+0.005,txt,fontsize = 10)
axes.set_title("R2 et RMSE des différents modèles entraînés et évalués sur différentes sorties")
figure = plt.gcf()
figure.set_size_inches(11.7,8.3)
plt.legend()
plt.savefig("python_files\\get_graphes\\graphes\\models_eval_all")