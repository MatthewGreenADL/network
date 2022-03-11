import os 
import argparse


years = ["1516"]
regionlist = ["VRnominal","Enominal"]#,"Dnominal"]

outputname = "OR_7"

for year in years:
    for region in regionlist:
        the_string =  '#!/bin/sh\n'
        the_string += '#SBATCH -p batch \n'
        the_string += '#SBATCH -N 1 \n'
        the_string += '#SBATCH -n 1 \n'
        the_string += '#SBATCH --time=01:00:00 \n'
        the_string += '#SBATCH --mem=4GB \n'
        the_string += "python plotter.py --dataperiods " + year + " --region " + region + " --output output_local/"+outputname+"/"
        f= open('/fast/users/a1608402/rootpyPlotter2/cloudjob_' + region + "_" + year + ".sh",'w')
        f.write(the_string)
        f.close()
        print(the_string)
        
        os.system("sbatch " + "/fast/users/a1608402/rootpyPlotter2/cloudjob_" + region + "_" + year + ".sh")

        #os.system("python submission.py --year " + year + " --regions " + regions + " --isowp FCTight --fakes True --output output_local/"+outputname+"_FCTight/")
