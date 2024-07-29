import xml.etree.ElementTree as ET
import time as t
import gzip
import attributes as attrib

#split network in nodes and links
true_start = t.time()
print("Parsing network...")
network_file = attrib.network_file
tree = ET.parse(gzip.open(network_file))
#usually takes around 190 seconds
print("Parsing done in",t.time()-true_start,"seconds")
root = tree.getroot()
# links_filename = network_file[:-7] + "_links.xml"
# nodes_filename = network_file[:-7] + "_nodes.xml"
links_filename = attrib.links_file
nodes_filename = attrib.nodes_file
start = t.time()
print("Building links and nodes files...")
lf = open(links_filename,'wb')
lf.write("<?xml version='1.0' encoding='UTF-8'?>\n".encode())
nf = open(nodes_filename,'wb')
nf.write("<?xml version='1.0' encoding='UTF-8'?>\n".encode())
nf.write(ET.tostring(root[1]))
lf.write(ET.tostring(root[2]))
lf.close()
nf.close()
print(f"Total time : {t.time()-true_start}")
