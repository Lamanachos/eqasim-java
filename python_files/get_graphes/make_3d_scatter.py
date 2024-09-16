from math import ceil, floor
import attributes as attrib
import matplotlib.pyplot as plt
import numpy as np

def make_3d_scatter(xyz_names = ["er_idf","att_idf","car_ms_idf_nb"]):
    df_results = attrib.get_results()

    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 

    X = df_results[xyz_names[0]]
    Y = df_results[xyz_names[1]]
    Z = df_results[xyz_names[2]]
    fig = plt.figure()
    axes = fig.add_subplot(projection='3d')
    axes.scatter(X,Y,Z,s=5,marker = "o")
    axes.set_xlabel(xyz_names[0],fontsize = 8)
    axes.set_ylabel(xyz_names[1],fontsize = 8)
    axes.set_zlabel(xyz_names[2],fontsize = 8)
    axes.set_xticks(np.arange(floor(min(X)),ceil(max(X)),round((max(X)-min(X))/10,1)))
    axes.set_yticks(np.arange(floor(min(Y)),ceil(max(Y)),round((max(Y)-min(Y))/10,1)))
    axes.set_zticks(np.arange(floor(min(Z)),ceil(max(Z)),round((max(Z)-min(Z))/10,1)))
    elevation_angle = 20
    azimuthal_angle = 140
    axes.view_init(elevation_angle, azimuthal_angle)
    #figure = plt.gcf()
    #figure.set_size_inches(11.7,8.3)
    #plt.savefig(attrib.graphes_folder+"\\graph_3d",dpi = 300)
    plt.show()

make_3d_scatter()


