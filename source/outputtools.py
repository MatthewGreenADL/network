import os 
import math

from rootpy import ROOT
from ROOT  import RooStats
def createOutputFolders(outputfolder,state): 
    Region = state['Region']
    DataPeriods = state['year']
    dataoutputfolder = os.path.join(outputfolder,"Data" + DataPeriods )

    os.system("mkdir -p " +	dataoutputfolder  )
    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region) )
#    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"Loose") )
#    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"Tight") )
 #   os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"Tighter") )
 #   os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"Tenacious") )
##    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"N-1","Loose") )
#    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"N-1","Tight") )
#    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"N-1","Tighter") )
#    os.system("mkdir -p " + os.path.join(dataoutputfolder,Region,"N-1","Tenacious") )


def outputRegionDiagnostics(breakdowns,state):
    #print "Region: " + Region
    Region     = state['Region']
    RegionType = state['regiontype']
#    metwp      = state['metwp']
#    isowp   = state['isowp']
    #Region     = state['region']
    Year       = state['year']
    applynf  = state['applynf']
    usefakes = state['usefakes']
    BLINDED = state['BLINDED']
    if Year =="1516":
        BLINDED = False

    if "VH" in Region:
        BLINDED = True
    #for legend in breakdowns['background']:
    #    print legend + ": " + str(breakdowns['background'][legend]['yield']) + "\pm" + str(breakdowns['background'][legend]['error'])

    #if RegionType.startswith("CR"):
    primarybackgrounds = ""
    if RegionType is "CRVV" : primarybackgrounds = "Diboson"
    if RegionType is "CRTOP": primarybackgrounds = ("t#bar{t}","Single top")
    if RegionType is "ABCD" : primarybackgrounds = "Z+jets"

    primaryyield = 0.0
    primaryerror = 0.0
    otheryield   = 0.0
    othererror   = 0.0


    for background in breakdowns['background']:
        if background == 'total': continue 
        if background == 'Signal': continue
        if background not in primarybackgrounds:
            otheryield += breakdowns['background'][background]['yield']
            othererror += breakdowns['background'][background]['error']**2
        else:
            primaryyield += breakdowns['background'][background]['yield']
            primaryerror += breakdowns['background'][background]['error']**2

    othererror   = math.sqrt(othererror)
    primaryerror = math.sqrt(primaryerror)


#    if bool(usefakes):
    DiagOutput = open('diagnostics/diag_' + Region + '_' + str(Year) + '_.txt','w')
#    else:
    #DiagOutput = open('diag_' + Region + '_' + str(Year) + "_" + metwp + "_" + isowp + '_' + str(usefakes) +  '.txt','w')

    DiagOutput.write("Region\t" +Region +"\n")
    if not BLINDED:
        datayield    =  breakdowns['data']['Data']['yield']
        dataerror    =  breakdowns['data']['Data']['error']
        try:
            A  = (datayield -  otheryield)
            B  = primaryyield 
            dA =  math.sqrt(dataerror**2 +othererror**2)
            dB = primaryerror

            normfactor = A/B
            dNF = math.sqrt((1/(B**2))*(dA**2) + ((A**2)/(B**4))*(dB**2))

        except:
            normfactor = 0.0 
            dNF = 0.0
        DiagOutput.write(Region + " NF\t" + str(normfactor) + "\t" + str(dNF) + "\n")
        if ("RJ" in Region) or Region.startswith("CR"):
            DiagOutput.write("NFs Applied\t False\n")
        else:
            DiagOutput.write("NFs Applied\t" + str(applynf) + "\n")

            
    else:
        DiagOutput.write(Region + " NF\tN/A\tN/A\n")
        DiagOutput.write("NFs Applied\t" + str(applynf) + "\n")
    # ABCDoutput = open('ABCD_' + Region + '_' + metwp + '.txt', 'w')
    # ABCDoutput.write(str(DataEstimate) + " " + str(DataEstimateError) + "\n")
    # ABCDoutput.write( str(zjetsyield) + " " + str(zjetserror) )
    # ABCDoutput.close()

    #print Region + " NF: " + str(normfactor) + "\pm" + str(dNF)
    for legend in breakdowns['background']:
        if legend == 'total': continue
        #purity = (breakdowns['background'][legend]['yield']/ breakdowns['background']['total']['yield'] )
        DiagOutput.write(legend + "\t" + str(breakdowns['background'][legend]['yield']) + "\t" +str(breakdowns['background'][legend]['error'])  + "\n")
        

    try:
        DiagOutput.write("Signal\t" +str(breakdowns['signal']['Signal']['yield']) + "\t" + str(breakdowns['signal']['Signal']['error']) + "\n")
    except:
        DiagOutput.write("Signal\t N/A\t N/A \n")   
    DiagOutput.write("Total\t" + str(breakdowns['background']['total']['yield']) + "\t" +str(breakdowns['background']['total']['error'])  + "\n")
    if not BLINDED:
        DiagOutput.write("Data\t" + str(breakdowns['data']['Data']['yield']) + "\t" +str(breakdowns['data']['Data']['error'])  + "\n")
    else:
        DiagOutput.write("Data\tN/A\tN/A\n")
    #DiagOutput.write(legend + "\t" + str(breakdowns['data']['Data']['yield']) + "\t" +str(breakdowns['data']['Data']['error'])  + "\n")
          
#    for legend in breakdowns['background')
        

    for legend in breakdowns['background']:
        if legend == 'total': continue
        
        try:
            purity = (breakdowns['background'][legend]['yield']/ breakdowns['background']['total']['yield'] )
        except ZeroDivisionError:
            purity = 0.0
    
        DiagOutput.write(legend + " Purity\t" + str(purity) + "\t" + str(0.0) + "\n")
        #print 

    
   # try:    
   #     DiagOutput.write("s/b\t" + str(breakdowns['signal']['Signal']['yield']/breakdowns['background']['total']['yield'])  + "\t" + str(0.0) +"\n")
   #     DiagOutput.write("s/sqrt(b)\t" + str(breakdowns['signal']['Signal']['yield']/math.sqrt(breakdowns['background']['total']['yield']))+ "\t" + str(0.0) + "\n")
   #     DiagOutput.write("s/sqrt(s+b)\t" + str(breakdowns['signal']['Signal']['yield']/math.sqrt(breakdowns['signal']['Signal']['yield']+breakdowns['background']['total']['yield']))+ "\t" + str(0.0) + "\n")
#        Significane_Relative 
#        print "end of try"

   #     Significance_Relative= float(breakdowns['background']['total']['error'])/float(breakdowns['background']['total']['yield'] )
   #     observed = float(breakdowns['signal']['Signal']['yield']) + float(breakdowns['background']['total']['yield'])
   #     observed_error = math.sqrt(breakdowns['signal']['Signal']['error']**2 + breakdowns['background']['total']['yield']**2)
   #     expected = float(breakdowns['background']['total']['yield'])
   #     expectederror = breakdowns['background']['total']['error']
   #     relativeerror = float(breakdowns['background']['total']['error'])/float(breakdowns['background']['total']['yield'] )
   #     DiagOutput.write("sig\t" + str(round(ROOT.RooStats.NumberCountingUtils.BinomialObsZ(observed,expected, relativeerror),2))+"\n"  )
#        print "end of try"
   #     Significance_Relative_Systematics = float(breakdowns['background']['total']['error'])/float(breakdowns['background']['total']['yield']) + 0.2 
   #     DiagOutput.write("sigsys\t" + str(round(ROOT.RooStats.NumberCountingUtils.BinomialObsZ(observed,expected, Significance_Relative_Systematics),2))  )
   #     print "end of try"
   # except ValueError:
   #     DiagOutput.write("s/b\tN/A\tN/A\n")
   #     DiagOutput.write("s/sqrt(b)\tN/A\tN/A\n")
   #     DiagOutput.write("s/sqrt(s+b)\tN/A\tN/A\n")
   #     DiagOutput.write("sig\tN/A\tN/A\n")
   #     DiagOutput.write("sigsys\tN/A\tN/A\n")

    DiagOutput.close()




def outputLogPlots(canvas,histpad, dataoutputfolder, variable,backgrounds,RegionDictionary,state):
#    metwp = state['metwp']
    systematics = state['systematics']
    donminus1 = state['donminus1']
    Region = RegionDictionary['region']
    
    filenamevariable = variable.replace("/","_").replace("_1000","")
    
    if donminus1:
        canvas.Print(dataoutputfolder + "/" + Region + "/N-1//log_"+ filenamevariable+ "_" + Region + "_"+systematics+".png")
    else:
        canvas.Print(dataoutputfolder + "/" + Region + "/log_"+ filenamevariable+ "_" + Region + "_"+systematics+".png")
        canvas.Print(dataoutputfolder + "/" + Region + "/log_"+ filenamevariable+ "_" + Region + "_"+systematics+".pdf")
#        canvas.Print(dataoutputfolder + "/" + Region + "/" + metwp + "/log_"+ filenamevariable+ "_" + Region + "_"+systematics+".eps")

def outputLinPlots(canvas,histpad, dataoutputfolder, variable,backgrounds,RegionDictionary,state):
#    metwp = state['metwp']
    systematics = state['systematics']
    donminus1 = state['donminus1']
    Region = RegionDictionary['region']

    filenamevariable = variable.replace("/","_").replace("_1000","")
    
    histpad.SetLogy(0)
    backgrounds.SetMinimum(0.0)
#    backgrounds.SetMaximum(3*backgrounds.sum.GetMaximum())
    backgrounds.SetMaximum(100)

    #backgrounds.SetMaximum(10)
#    canvas.Print(dataoutputfolder + "/" + Region + "/"  + metwp + "/lin_"+ filenamevariable+ "_" + Region  + "_" +systematics+".png")
    canvas.Print(dataoutputfolder + "/" + Region + "/lin_"+ filenamevariable+ "_" + Region  + "_" +systematics+".pdf")




