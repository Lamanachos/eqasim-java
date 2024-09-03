from numpy import mean, median, std
import pandas as pd
file = "python_files\\get_data\\res_drz.csv"
df = pd.read_csv(file, sep=";")
for i in df.columns :
    print(i + " :")
    print(median(df[i]))
    print(mean(df[i]))
    print(std(df[i]))