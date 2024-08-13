import pandas as pd
import numpy as np
from scipy.stats import pointbiserialr
from math import sqrt
import seaborn as sns
import matplotlib.pyplot as plt
import random as rd

def getMerit(subset, df_data,df_res):#code pas de moi trouvé sur internet
    k = len(subset)
    rcf_all = []
    for feature in subset:
        for res_name in df_res.columns :
            coeff = pointbiserialr( df_data[feature], df_res[res_name] )
            rcf_all.append( abs( coeff.correlation ) )
    rcf = np.mean( rcf_all )
    corr = df_data[subset].corr()
    corr.values[np.tril_indices_from(corr.values)] = np.nan
    corr = abs(corr)
    rff = corr.unstack().mean()

    return (k * rcf) / sqrt(k + k * (k-1) * rff)
        
def get_best_subset(features,nb,df_data,df_res,liste=[]):
    """Obtenir le meilleur subset de caractéristiques pour une df donnée, méthode relieF.
    label : nom de l'entrée df correspondant au label
    nb : taille du subset (la complexité augmente vite donc éviter nb >= 5)
    df : la dataframe
    liste : ne  pas toucher c'est un argument utilisé par la récursion"""
    t_liste = len(liste)
    t_feat = len(features)
    if t_liste == t_feat:
        temp = []
        for j in range(len(liste)) :
            if liste[j] == 1:
                temp.append(features[j])
        return temp,getMerit(temp,df_data,df_res)
    else :
        nb_1 = liste.count(1)
        if nb_1<nb:
            temp1 = liste.copy()
            temp1.append(1)
            res1,m1 = get_best_subset(features,nb,df_data,df_res,temp1)
            if nb-t_feat+t_liste < nb_1 : #le nombre de feat possible restante est assez grand pour qu'on puisse atteindre nb uns en mettant au moins un 0
                temp0 = liste.copy()
                temp0.append(0)
                res0,m0 = get_best_subset(features,nb,df_data,df_res,temp0)
                if m0 > m1:
                    return res0,m0
                else :
                    return res1,m1
            else :
                return res1,m1
        else :
            temp0 = liste.copy()
            temp0.append(0)
            res0,m0 = get_best_subset(features,nb,df_data,df_res,temp0)
            return res0,m0