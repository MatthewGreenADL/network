import os 

regionname   = "PRE3L"
outputfolder = "output_local/3L_ISR/"
year = "1516"

os.system("python source/plotter_network.py --dataperiods " + year +  " --region " + regionname +  " --output " + outputfolder)
