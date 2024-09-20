from numpy import mean, median, std
import pandas as pd
file = "python_files\\get_data\\res_drz.csv"
df = pd.read_csv(file, sep=";")
nb = 0
tot = 0
for i in df.columns :
    if i != "insee":
        nb += 1
        print(i + " :")
        print("median :",median(df[i]))
        print("mean :",mean(df[i]))
        tot += mean(df[i])
        print("std :",std(df[i]))
print("MEAN MEAN :",tot/nb)