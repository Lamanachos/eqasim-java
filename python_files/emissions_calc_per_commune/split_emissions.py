import os
import xml.etree.ElementTree as ET
import time as t
import gzip
import attributes as attrib
import multiprocessing as mp

if __name__ == "__main__":
    true_start = t.time()
    
    events_to_keep = attrib.events_to_keep
    emissions_file = attrib.emissions_file
    emissions_split_folder_output = attrib.emissions_split_folder_output
    if not os.path.exists(emissions_split_folder_output):
        os.makedirs(emissions_split_folder_output)
    print("Parsing and writing emissions...")
    unzip_file = gzip.open(emissions_file)
    tree = ET.iterparse(unzip_file)
    count = 0
    row_count = 0
    nb_break = attrib.nb_break
    start = t.time()
    inputs = []
    count = 0
    file_count = 0
    childs = []
    temp_emissions_file = emissions_split_folder_output + "\\" + str(file_count) + ".xml.gz"
    f = gzip.open(temp_emissions_file,'wb')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".encode())
    f.write("<events version='1.0'>\n".encode())
    for event,elem in tree:
        if elem.attrib["type"] in events_to_keep:
            childs.append(elem)
            f.write(ET.tostring(elem))
            count += 1
        if count == nb_break :
            count = 0
            f.write("</events>".encode())
            f.close()
            file_count += 1
            print(f"File {file_count} built in {t.time()-start} seconds")
            start = t.time()
            temp_emissions_file = emissions_split_folder_output + "\\" + str(file_count) + ".xml.gz"
            f = gzip.open(temp_emissions_file,'wb')
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".encode())
            f.write("<events version='1.0'>\n".encode())
    f.write("</events>".encode())
    f.close()
    print("Parsing and writing done in ",t.time()-true_start," seconds")
    print(f"Total time : {t.time()-true_start}")
