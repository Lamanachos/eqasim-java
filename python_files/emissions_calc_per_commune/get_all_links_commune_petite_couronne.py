import attributes as attrib
import os
import geopandas as gpd

attrib.build_attributes(every_commune=True)
os.system("python python_files\\emissions_calc_per_commune\\get_links_per_commune.py")
