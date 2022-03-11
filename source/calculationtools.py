import math
def calculateNFs(backgroundstacks,datastack,RegionDictionary):

    Region = RegionDictionary['region']
    RegionLabel = RegionDictionary['regionlabel']
    RegionType  = RegionDictionary['regiontype']

    datavalue = 0.0
    DataEstimate = 0.0
    DataEstimateError = 0.0

    datavalue,dataerror = datastack.sum.integral(error=True, overflow=True)

    DataEstimate = datavalue 
    DataEstimateError = dataerror**2 

    MCyield = 0.0
    MCerror = 0.0
    if RegionType == "CRVV":
        primarybackground = ("Diboson", "VV")
    elif RegionType == "CRTOP":
        primarybackground = ("t#bar{t}","Single top")
    elif RegionType == "ABCD":
        primarybackground = "Z+jets"

    for LegendGroup in backgroundstacks:
        if LegendGroup == 'Data': continue
        if LegendGroup == 'Signal' : continue 
        backgroundyield,backgrounderror = backgroundstacks[LegendGroup].sum.integral(error=True,overflow=True)
        if LegendGroup not in primarybackground:

#            print "SAMPLE: " + LegendGroup
#            print "Yield+ Background: " + str(backgroundyield) + "+/-" + str(backgrounderror)
            DataEstimate      -= backgroundyield 
            DataEstimateError += backgrounderror**2 
        elif LegendGroup in primarybackground:
            MCyield += backgroundyield 
            MCerror += backgrounderror**2 

        

    
    DataEstimateError = math.sqrt(DataEstimateError)
    MCerror           = math.sqrt(MCerror)
    if MCyield != 0.0:
        NF = DataEstimate/MCyield
        A  = DataEstimate
        B  = MCyield 
        dA = DataEstimateError
        dB = MCerror 
        NFerror = math.sqrt((1/B/B)*dA*dA + (A*A/B/B/B/B)*dB*dB)
    else:   
        NF = 0.0
        NFerror = 0.0

    if RegionType == "ABCD":
 #       print "TOTAL: " + LegendGroup
 #       print "Yield+ Background: " + str(DataEstimate) + "+/-" + str(DataEstimateError)
        return DataEstimate, DataEstimateError
    
    return NF, NFerror
        
def SetNegativeYieldsToZero2(stack,nbins):
    for hist in stack:
        for i in range(1,int(nbins)+1):
            if hist.GetBinContent(i) < 0.0:
                print "negative bin content set to 0.0"
                hist.SetBinContent(i,0.0) 


def SetNegativeYieldsToZero(stack):
    """
    take stack, loop through each histogram, loop through each bin in that histogram, if negative set it to zero. 
    store in a temporary stack, and return that stack. 
    """
    from rootpy.plotting import F1, Hist, HistStack, Canvas, Legend, Pad
    temphiststack = HistStack()
    for hist in stack:
        for i in range(1,int(hist.GetNbinsX())+1):
            if hist.GetBinContent(i) < 0.0:
                hist.SetBinContent(i,0.0)
        temphiststack.Add(hist.Clone())
    return temphiststack
#    stack = temphiststack




        

"""
step one, loop through each background, 
if VV then add it to the list, 
if not VV then add to 'Other', 
record name of background. 

do this twice. Once for ee and once for mumu


Sample     ee       mum
--------------------------
total 
VV
non VV 
--------------------------
Data 
--------------------------
"""
