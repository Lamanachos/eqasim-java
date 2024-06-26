import matplotlib.pyplot as plt
import attributes as attrib
file = attrib.results_file
f = open(file,"r")
lines = f.readlines()
f.close()
all_dist = lines[7][1:-2].split(", ")
for i in range(len(all_dist)) :
    all_dist[i] = float(all_dist[i])
inside_dist = lines[9][1:-2].split(", ")
for i in range(len(inside_dist)) :
    inside_dist[i] = float(inside_dist[i])
all_hours = lines[11][1:-2].split(", ")
for i in range(len(all_hours)) :
    all_hours[i] = float(all_hours[i])
inside_hours = lines[13][1:-2].split(", ")
for i in range(len(inside_hours)) :
    inside_hours[i] = float(inside_hours[i])
plt.subplot(2,2,1)
plt.plot(all_dist)
plt.title("all_dist")
plt.subplot(2,2,2)
plt.plot(inside_dist)
plt.title("inside_dist")
plt.subplot(2,2,3)
plt.plot(all_hours)
plt.title("all_hours")
plt.subplot(2,2,4)
plt.plot(inside_hours)
plt.title("inside_hours")
plt.show()
