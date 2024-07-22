import attributes as attrib
import os 
import sys, getopt
import time as t
def main(argv):
    start_time = t.time()
    basecase_on = True
    sc_name = attrib.scenario_name
    ins = attrib.insee
    try:
        opts, args = getopt.getopt(argv,"b:s:i:f:",["basecase_or_not=","scenario_name=","insee=","sc_folder="])
    except getopt.GetoptError:
        print ('test.py -b <run also basecase or not (True or False)> -s <scenario_name> -i <insee of the drz>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-b", "--basecase_or_not"):
            basecase_on = bool(arg)
        if opt in ("-s", "--sc_name"):
            sc_name = arg
        if opt in ("-i", "--insee"):
            ins = int(arg)
        if opt in ("-f", "--folder"):
            sc_fold = arg
    attrib.build_attributes(False,sc_name,sc_folder=sc_fold,insee_par=ins)
    #os.system("python split_network.py")
    os.system("python split_emissions.py")
    #os.system("python convert_espg.py "+str(ins))
    os.system("python get_links_per_commune.py")
    os.system("python calculate_emissions.py")
    os.system("python MS_ATT.py")
    if basecase_on :
        attrib.build_attributes(True,sc_name,sc_folder=sc_fold,insee_par=ins)
        os.system("python calculate_emissions.py")
        os.system("python MS_ATT.py")
    attrib.build_attributes(False,sc_name,sc_folder=sc_fold,insee_par=ins)
    #os.system("python Traitement_sorties\\emissions_calc_per_commune\\get_evolutions.py")
    print("Done :",sc_name,",",ins)
    print("Total time :",t.time()-start_time)

if __name__ == "__main__":
   main(sys.argv[1:])

