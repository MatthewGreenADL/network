#from calculationtools import calculateNFs
BLINDEDLIST = ("SR2L_LOW", "SR2L_INT", "SR2L_HIGH","SR2L_ISR","SR3L_LOW","SR3L_INT","SR3L_HIGH","SR3L_ISR")
VVCRlist =("CR2L-VV","CR2L_ISR-VV","CR3L-VV","CR3L_ISR-VV")
TOPCRlist = ("CR2L-TOP","CR2L_ISR-TOP")
CRlist = VVCRlist + TOPCRlist
ABCDlist = ("A","B","D","VRC","VRD")
SRlist = ("SR2L_LOW", "SR2L_INT", "SR2L_HIGH","SR2L_ISR","SR3L_LOW","SR3L_INT","SR3L_HIGH","SR3L_ISR")

def produceTitle(Region,backgroundstacks):
    cutflowstring = "Samples:"
    for LegendEntry in backgroundstacks:

        if LegendEntry == 'Data': continue
        if LegendEntry == 'Signal' : continue 
        print "Legend Entry: " + LegendEntry
        #if ( Region.startswith("SR")): continue
        cutflowstring += "& $" + LegendEntry + "$"
        
    cutflowstring += "&Total&CR Purity& CR NF& Signal & S/B &Data& Data/MC \\\ \\hline "
    #cutflowstring += "\\\ \\hline" 
    return cutflowstring

def produceBackgroundYields(RegionDictionary,backgroundstacks,stack,datastack):

    Region = RegionDictionary['region']
    RegionType = RegionDictionary['regiontype']
    yieldstring = Region 

    primaryyield = 0.0 
    #primarybackground = []
    #for LegendEntry in backgroundstacks:
    if RegionType == "CRVV":
        primarybackground =("Diboson","VV")
    elif RegionType == "CRTOP":
        primarybackground = ("Top","singleTop")
    else: 
        primarybackground = []
    totalyield, totalerror = stack.sum.integral(error=True,overflow=True)

    for LegendEntry in backgroundstacks:
        if LegendEntry == "Data": continue
        if Region.startswith("SR") and LegendEntry == "Data": continue
        
        backgroundyield,backgrounderror = backgroundstacks[LegendEntry].sum.integral(error=True,overflow=True)
        if LegendEntry in primarybackground:
            primaryyield += backgroundyield 
        if LegendEntry == "Signal":
            signalyield = backgroundyield
            signalerror = backgrounderror
            continue
        yieldstring += "&$" + str(round(backgroundyield,2)) + "\pm" + str(round(backgrounderror,2)) + "$"
    yieldstring += "&$" + str(round(totalyield,2)) +"\pm" + str(round(totalerror)) + "$"
    if ("CRVV" or "CRTOP") in RegionType:
        yieldstring += "&$" + str(round(primaryyield/totalyield,2)) +"$"
        NormalisationFactor,NFerror = calculateNFs(backgroundstacks,datastack,RegionDictionary)
        yieldstring += "&$" + str(round(NormalisationFactor,3)) +"\pm" + str(round(NFerror,3)) + "$"
    else:
        yieldstring += "& - & - "

    if "Signal" in backgroundstacks:
        yieldstring += "& $" + str(round(signalyield,2)) + "\pm" + str(round(signalerror,2)) + "$" 
        yieldstring += "& $" + str(round(signalyield/totalyield,2)) +"$"
    else:
        yieldstring += "& -"
        yieldstring += "& -"

    return yieldstring


def produceDataYields(Region,datastack,stack):
    if Region.startswith("SR"):
        yieldstring = "& - & - \\\ \\hline "
    else:
        datayield, dataerror   = datastack.sum.integral(error=True,overflow=True)
        totalyield, totalerror = stack.sum.integral(error=True,overflow=True)
        yieldstring = "&$" + str(round(datayield,0)) + "$&$" + str(round(datayield/totalyield,2)) + "$ \\\ \\hline"
    return yieldstring


def produceExtraInformation(RegionDictionary,backgroundstacks):
    primaryyield = 0.0 
    #primarybackground = []


    return yieldstring 


def produceRegionBreakdown(backgroundstacks,stack,datastack,RegionDictionary):
    Region = RegionDictionary['region']
    titlestring =  produceTitle(Region,backgroundstacks)
    yieldstring =  produceBackgroundYields(RegionDictionary,backgroundstacks,stack,datastack)
    #yieldstring += produceExtraInformation(Region,backgroundstacks,VVCRlist,TOPCRlist)
    yieldstring += produceDataYields(Region,datastack,stack)

    return titlestring,yieldstring


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

            print "SAMPLE: " + LegendGroup
            print "Yield+ Background: " + str(backgroundyield) + "+/-" + str(backgrounderror)
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
        print "TOTAL: " + LegendGroup
        print "Yield+ Background: " + str(DataEstimate) + "+/-" + str(DataEstimateError)
        return DataEstimate, DataEstimateError

    return NF, NFerror


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
