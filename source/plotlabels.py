import ROOT
from calculationtools import calculateNFs
import math 
import rootpyglobals
from ROOT import RooStats

def atlaslabel( input):
    """
    The location of the ATLAS Internal label
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(labelmargin,0.87,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize*1.2)
    plottitle.SetNDC()
    plottitle.Draw()

def energylabel(input):
    """
    The location of the Energy and Luminosity label
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(labelmargin,0.805,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize*1.2)
    plottitle.SetNDC()
    plottitle.Draw()

def SRlabel(input):
    """
    Location of the Region in questions label.
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(labelmargin,0.745,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize)
    plottitle.SetNDC()
    plottitle.Draw()

def METlabel(input):
    """
    Location of the Region in questions label.
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(labelmargin,0.695,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize)
    plottitle.SetNDC()
    plottitle.Draw()

def topleftplotlabel(input):
    """
    Location of some diagnostic information. 
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(labelmargin,0.961,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize)
    plottitle.SetNDC()
    plottitle.Draw()

def toprightplotlabel(input):
    """
    Location of Release and Data year information
    """
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize
    plottitle = ROOT.TLatex(0.74,0.971,input)
    plottitle.SetTextFont(43)
    plottitle.SetTextSize(defaultlabelsize)
    plottitle.SetNDC()
    plottitle.Draw()


def drawXandYlabels(backgrounds,data,xlabel,ylabel,state,histpad,ratiopad):
    """
    Function governing the drawing of the x and y labels. With options for if or if there is not a ratiopad.
    """
    print "xlabel: " + xlabel
    print "ylabel: " + ylabel

    histpad.cd()
    doRatio = state['doRatio']
    labelmargin      = rootpyglobals.labelmargin
    defaultlabelsize = rootpyglobals.defaultlabelsize

    backgrounds.yaxis.SetTitle(ylabel)
    backgrounds.yaxis.SetTitleSize(30)
    backgrounds.yaxis.SetTitleFont(43)
    backgrounds.yaxis.SetTitleOffset(2)
    backgrounds.sum.yaxis.set_label_size(int(defaultlabelsize*20))
    backgrounds.yaxis.SetLabelColor(1)

#    ratiopad.cd()
    
    #    backgrounds.yaxis.SetTitle("Data/SM")
    try:
        data.sum.yaxis.SetTitle("Data/SM") 
        data.sum.yaxis.SetTitleSize(100)
        data.sum.yaxis.SetTitleFont(43)
        data.sum.yaxis.SetTitleOffset(2) 
        data.sum.yaxis.CenterTitle()
    except:
        pass
    backgrounds.yaxis.SetTitleOffset(2)
    backgrounds.sum.yaxis.set_label_size(int(defaultlabelsize*20))
    

    try:
        data.sum.xaxis.SetTitleSize(40)
        data.sum.xaxis.SetTitleFont(43)
        data.sum.xaxis.SetTitle(xlabel)
        data.sum.xaxis.SetTitleOffset(2)
        
        data.sum.xaxis.set_label_size(int(defaultlabelsize*20))
        data.sum.yaxis.set_label_size(int(defaultlabelsize*20))
    except:
        pass






def drawXandEfflabels(stack,datastack,xlabel,ylabel,defaultlabelsize,ratiopad,histpad,doRatio,labelmargin):
    """
    Function governing the drawing of the x and y labels. With options for if or if there is not a ratiopad.
    """
#    histpad.cd()
    stack.sum.yaxis.SetTitle("#epsilon_{SR/RJ2LA}")
    stack.sum.yaxis.SetTitleOffset(2)
    stack.sum.yaxis.set_label_size(int(defaultlabelsize*1.5))

    #if doRatio:
    #    #ratiopad.cd()
    #    datastack.xaxis.SetTitle(xlabel)
    #    datastack.yaxis.SetTitle("Data/SM")
    ##    datastack.yaxis.CenterTitle()
     #   datastack.xaxis.SetTitleOffset(3.4)
    #    datastack.yaxis.SetTitleOffset(2)
    #    datastack.xaxis.set_label_size(int(defaultlabelsize*1.5))
    #    datastack.yaxis.set_label_size(int(defaultlabelsize*1.5))
    #    #histpad.cd()
    #else:
 #       histpad.cd()
    stack.sum.xaxis.SetTitle(xlabel)
    stack.sum.xaxis.SetTitleOffset(1.5)
    stack.sum.xaxis.set_label_size(int(defaultlabelsize*1.5))
  #  histpad.cd()


def drawPlotInformation(state):
        """
        Draw all non-legend relevant information 
        """
        #doRatio = state['doRatio']
        DataPeriods = state['year']
#        donminus1 = state['donminus1']
#        metwp = state['metwp']
#        isowp = state['isowp']
        atlasStatus = rootpyglobals.atlasStatus
        RegionLabel = state['regionlabel']
        # labelmargin      = rootpyglobals.labelmargin
        # defaultlabelsize = rootpyglobals.defaultlabelsize
        # atlasStatus = rootpyglobals.atlasStatus

        atlaslabel('#it{#bf{ATLAS}} ' + atlasStatus)
        if(DataPeriods == '1516'):
            energylabel("13TeV, 36.2 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data1516}')
        elif(DataPeriods== '17'):
            energylabel("13TeV, 43.9 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data17}') 
        elif(DataPeriods== '18'):
            energylabel("13TeV, 59.9 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data18}') 
        elif(DataPeriods=='15-17'):
            energylabel("13TeV, 80.1 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data15-17}') 
        elif(DataPeriods=='15-18'):
            energylabel("13TeV, 139 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data15-18}') 
        elif(DataPeriods=='17-18'):
            energylabel("13TeV, 80.1 fb^{-1}")
            toprightplotlabel('#lower[0.4]{Rel21:Data17-18}')
        #        if donminus1:
        #            SRlabel( RegionLabel + " N-1")
        #        else:
        SRlabel( RegionLabel )
        #        METlabel( "MET: " + metwp + " ISO: " + isowp  )
        






def drawTopLeftInformation(breakdowns,state):
    """
    Draw the top left diagnostic information seciton of the plot. 
    """
    from ROOT  import RooStats
    Year  = state['year']
    applynf= state['applynf']
    BLINDED   = state['BLINDED']

    Region     = state['Region']
    RegionType = state['regiontype']
#    print "Region: " + Region 
#    print "RegionType: " + RegionType 

    if RegionType.startswith("CR"):
        if RegionType is "CRVV" : primarybackgrounds = "Diboson"
        if RegionType is "CRTOP": primarybackgrounds = ("t#bar{t}","Single top")

        datayield =  breakdowns['data']['Data']['yield']
        dataerror =  breakdowns['data']['Data']['error']
        primaryyield = 0.0
        primaryerror = 0.0
        otheryield   = 0.0
        othererror   = 0.0

#        print "BREAKDOWNS" + str(breakdowns['background'])
        for background in breakdowns['background']:
            if background == 'total': continue 
            if background not in primarybackgrounds:
                otheryield += breakdowns['background'][background]['yield']
                othererror += breakdowns['background'][background]['error']**2
            else:
                primaryyield += breakdowns['background'][background]['yield']
                primaryerror += breakdowns['background'][background]['error']**2

        othererror   = math.sqrt(othererror)
        primaryerror = math.sqrt(primaryerror)

        A  = (datayield -  otheryield)
        B  = primaryyield 
        dA = math.sqrt(dataerror**2 +othererror**2)
        dB = primaryerror

        normfactor = A/B
        dNF = math.sqrt((1/(B**2))*(dA**2) + ((A**2)/(B**4))*(dB**2))

        #print legend + " NF: " + str(nf)
        topleftplotlabel("NF: " + str(round(normfactor,3)) + "\pm" + str(round(dNF,3))) 
    elif RegionType is "ABCD" and not Region.startswith("SR2L_ISR") and 0 : 
        
        primarybackgrounds = ("Z+jets")
        if BLINDED: return
        
        primaryyield = 0.0
        primaryerror = 0.0
        otheryield   = 0.0
        othererror   = 0.0
        zjetsyield = 0.0
        zjetserror = 0.0

            

        zjetsyield += breakdowns['background']['Z+jets']['yield']
        zjetserror += breakdowns['background']['Z+jets']['error']**2

        for other in breakdowns['background']:
            print "key: " + other 
            
#            if "Z" in other: continue
            if other == "Z+jets": continue
            if other == "total": continue
            otheryield += breakdowns['background'][other]['yield']
            othererror += breakdowns['background'][other]['error']**2

        othererror = math.sqrt(othererror)
        if BLINDED: 
            topleftplotlabel("Z+jets MC: " + str(round(zjetsyield,2)) + "\pm" + str(round(zjetsyield,2)))
            return

        datayield = breakdowns['data']['Data']['yield']
        dataerror =  breakdowns['data']['Data']['error']
        dataEstimate = datayield - otheryield 
        dataEstimateError = math.sqrt(dataerror**2 + othererror**2)


    elif not state['BLINDED']:
        datayield = breakdowns['data']['Data']['yield']
        mcyield   = breakdowns['background']['total']['yield']
        try:
            topleftplotlabel("Data/MC: " + str(round(datayield/mcyield,2)))
        except ZeroDivisionError:
            topleftplotlabel("Data/MC: MC = 0  " )
    elif Region.startswith("SR") and ("Signal" in breakdowns['signal']):
        print "In plotlabels"
        signalyield = breakdowns['signal']['Signal']['yield']
        mcyield   = breakdowns['background']['total']['yield']

        Significance_Relative_Systematics = float(breakdowns['background']['total']['error'])/float(breakdowns['background']['total']['yield'])
        observed = float(breakdowns['signal']['Signal']['yield']) + float(breakdowns['background']['total']['yield'])
        expected = float(breakdowns['background']['total']['yield'])        
        topleftplotlabel("S/sqrt(B)[STAT]: " + str(round(float(breakdowns['signal']['Signal']['yield'])/math.sqrt(float(breakdowns['background']['total']['yield'])),2))   )
#        topleftplotlabel("#sigma(S/B)[STAT]: " + str(round(ROOT.RooStats.NumberCountingUtils.BinomialObsZ(observed,expected, Significance_Relative_Systematics),2)))



        


def getYlabel(units,nbins,xmin,xmax):
    """
    Generate the label required for the y axis. In this way we can specify two to three native options.
    These options are eV meaning GeV or MeV, "1" which is a counting style of bin like njets or 
    We can chose radians, or "none" /"" which is or scale variables. 
    """
    if 'eV' in units:
        binning = str(round((xmax - xmin)/nbins,0)).split('.')[0]
        ylabel = "Events/" + binning + units
    elif "1" in units:
        binning = ""
        units = ""
        ylabel = "Events"
    elif 'rad' in units:
        binning = str(round((xmax - xmin)/nbins,2))
        ylabel = "Events/" + binning + units
    elif units == '':
        binning = str(round((xmax - xmin)/nbins,2))
        ylabel = "Events/" + binning + units
    return ylabel


def RegionYrange(Region):
    """
    Different regions and selections have different y axis ranges due to the different types of events present. 
    This function deals with this. 
    """
    if "CR" in Region:
        if "CRWZ" in Region:
            yminimum = 1e-1
            ymaximum = 1e8
        elif "CRZZ" in Region:
            yminimum = 1e-1
            ymaximum = 1e8
        elif "CRTOP" in Region:
            yminimum = 1e-1
            ymaximum = 1e8
        elif "CRZ" in Region:
            yminimum = 1e-1
            ymaximum = 1e8
        else:
            yminimum = 1e-1
            ymaximum = 1e4
    elif "VR" in Region:
        yminimum = 1e-1
        ymaximum = 1e6
    elif "SR" in Region:
        yminimum = 1e-1
        ymaximum = 1e2
    else:
        yminimum = 1e-1
        ymaximum = 1e8
    
    
    return yminimum,ymaximum 
