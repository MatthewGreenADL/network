from rootpy.plotting.shapes import Line,Arrow
from rootpy.plotting import F1, Hist, HistStack, Canvas, Legend, Pad
import rootpyglobals
from regiondefinitions import retreiveRegionInformation
from collections import OrderedDict
from rootpy import ROOT
from ROOT import TLatex
import math
from ROOT import TColor
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from ROOT  import RooStats


def defineState(args):
    Region = args.region
    RegionDictionary = retreiveRegionInformation(Region)
    state                = OrderedDict()
    RegionLabel        = RegionDictionary['regionlabel']
    Cutlist            = RegionDictionary['cutlist']
    Cutnames           = RegionDictionary['cutnames']
    RegionType         = RegionDictionary['regiontype']


    state['Region'] = args.region 
    if Region.startswith("SR"): 
        BLINDED = True
        plotData = 0 
        doRatio  = 0
        args.ratioplot = 0
    else:
        BLINDED = False
        plotData = 1

    if Region.startswith("SR") and args.dataperiods == "1516":
        BLINDED  = False
        plotData = 1 
        
    if "VH" in Region:
        BLINDED = True
        plotData = 0 

    state['BLINDED'] = BLINDED 
    state['Region']      = args.region
    state['regiontype']  = RegionDictionary['regiontype']
    state['regionlabel'] = RegionDictionary['regionlabel']
    state['year']        = args.dataperiods
    state['applynf']     = args.applynf
    state['usefakes']    = args.usefakes
    state['donminus1']   = args.nminus1
    state['BLINDED']     = BLINDED 
    state['plotData']    = plotData
    state['doRatio']     = args.ratioplot 
    state['systematics'] = args.systematics
    state['LegendExtraInformation'] = "Absolute" #Relative
    state['colorscheme'] = "RJ"
    state['ratiooverwrite'] = 1;

    if RegionType == "ABCD": args.applynf = False
        
    if "CR" in RegionType:args.applynf = False
#    print str(args.usefakes)
    return state 




def getTreeNames(sample,samples,rootfiles):
    """
    Inputs: sample  - specific sample to retreive tree of 
            samples - dictionary of all samples 
            rootfiles - rootfiles of all samples 
    Output: a root tree 
    """

    filename = samples[sample]['filename']
    rootfile  = rootfiles[sample]
    #print "INSIDEFilename" + Filename
#    if("data15" in filename):
#        try:
#            tree = rootfile.data1516
#        except:
#            try: 
#                tree = rootfile.Get("data15-16")
#            except:
#                pass
#            exit()
    if("data15" in filename):
        tree = rootfile.Get("data1516")
    elif("data17" in filename):
        tree = rootfile.data17
    elif("data18" in filename):
        tree = rootfile.data18
    elif("fakes" in filename):
        tree = rootfile.MM_CENTRAL
#    elif("fakes17" in Filename):
#        tree = rootfile.MM_CENTRAL
#    elif("fakes18" in Filename):
#        tree = rootfile.MM_CENTRAL
    elif("higgs" in filename):
        tree = rootfile.higgs_NoSys
    elif("singleTop" in filename):
        tree = rootfile.singleTop_NoSys
    elif("topOther" in filename):
        tree = rootfile.topOther_NoSys
    elif("triboson" in filename):
        tree = rootfile.triboson_NoSys
    elif("Vgamma" in filename):
        tree = rootfile.Vgamma_NoSys
    elif("Wjets" in filename):
        tree = rootfile.Wjets_NoSys
    elif("Zjets" in filename):
        tree = rootfile.Zjets_NoSys
    elif("DY" in filename):
        tree = rootfile.lowMassDY_NoSys
    elif("diboson" in filename):
        tree = rootfile.diboson_NoSys
    elif("ttbarDilep_410472" in filename):
        tree = rootfile.ttbarDilep_410472_NoSys
    elif("ttbar" in filename):
        tree = rootfile.ttbar_NoSys
    elif("C1N2_WZ_200p0_100p0_3L" in filename):
        tree = rootfile.Get("C1N2_WZ_200p0_100p0_3L_NoSys")
    return tree



def createSampleStack(samples):
    """
    input: samples dictionary - contains all sample information 
    output: a ROOT stack for data, signal, background and fakes 
    """
    from collections import OrderedDict
    stack     = OrderedDict()
    for Type in ['data','bkg','fakes', 'sig']:
        stack[Type] = OrderedDict()
#        print samples
        for sample in samples:
            legendEntry = samples[sample]['legend']
            isData = ('Data'  in legendEntry) and ('data' in Type)
            isSignal = ('Signal' in legendEntry) and ('sig' in Type)
            isBackground = ('Data' not in legendEntry) and ('Signal' not in legendEntry) and ("Fakes" not in legendEntry) and('bkg' in Type)
            isFakes = ('Fakes' in legendEntry) and 'fakes' in Type
            if isData: 
                stack[Type][legendEntry] = HistStack()
            elif isSignal:
                stack[Type][legendEntry] = HistStack()
            elif isBackground :
                stack[Type][legendEntry] = HistStack()
            elif isFakes :
                stack[Type][legendEntry] = HistStack()
    return stack


def processStack(stack,state):
    """
    process the output of the draw, which is a stack[Type][Legend] object into data,background,signals + their breakdowns.
    the samples object will contain the histograms, the breakdowns contain histograms, yields and errors seperately. 
    """
    from collections import OrderedDict
    data                = HistStack()
    backgrounds         = HistStack()
    signals             = HistStack()

    backgrounds_zeroed  = HistStack()
    signals_zeroed      = HistStack()
    
    databreakdown       = OrderedDict()
    backgroundbreakdown = OrderedDict()
    signalbreakdown     = OrderedDict()
    breakdowns          = OrderedDict()
    samples             = OrderedDict()
    if state['BLINDED']: oklist = ['bkg','fakes','sig']
    else: oklist = ['data','bkg','fakes','sig']

    for Type in oklist:
        for legend  in stack[Type]:            
            tempyield = stack[Type][legend].sum.Clone().integral(overflow=True,error=True)[0]
            temperror = stack[Type][legend].sum.Clone().integral(overflow=True,error=True)[1]
            
            if Type == 'data':
                data.Add(stack[Type][legend].sum.Clone())
                databreakdown[legend] = {'histogram': stack[Type][legend].sum.Clone() ,'yield': tempyield, 'error': temperror }
            elif (Type == 'bkg') :
                backgrounds.Add(stack[Type][legend].sum.Clone())
                backgroundbreakdown[legend] = {'histogram': stack[Type][legend].sum.Clone() ,'yield': tempyield, 'error': temperror }
            elif (Type == 'fakes'):
                backgrounds.Add(stack[Type][legend].sum.Clone())
                backgroundbreakdown[legend] = {'histogram': stack[Type][legend].sum.Clone() ,'yield': tempyield, 'error': temperror }
            elif Type == 'sig':
                signals.Add(stack[Type][legend].sum.Clone())
                signalbreakdown[legend] = {'histogram': stack[Type][legend].sum.Clone() ,'yield': tempyield, 'error': temperror }
    totalyield = 0.0
    totalerror = 0.0 
    for bkg in backgrounds:
#        if bkg == "total": continue 
        tempyield,temperror = bkg.integral(overflow=True,error=True) 
        if tempyield < 0.0: 
            tempyield = 0.0
        totalyield += tempyield 
        totalerror += temperror**2
    totalerror = math.sqrt(totalerror)
    backgroundbreakdown['total'] = {'histogram': backgrounds.sum.Clone(), 'yield':totalyield,'error':totalerror}


    breakdowns['background'] = backgroundbreakdown
    breakdowns['data']       = databreakdown
    breakdowns['signal']     = signalbreakdown
    samples['background'] = backgrounds
    samples['data'] = data
    samples['signal'] = signals    
    return samples,breakdowns





def drawBackgrounds(stack,Region):
    Hist.SetDefaultSumw2(True)
    from plotlabels import RegionYrange
    
    temphist = stack.sum.Clone()
    yminimum, ymaximum = RegionYrange(Region)

    stack.SetMinimum(yminimum)
    stack.SetMaximum(ymaximum)

    stack.Draw()
#    stack.sum.SetDefaultSumw2(True)
    errorband = stack.sum.Clone()
    errorband.SetMarkerSize(0)
#    errorband.SetLineWidth(2)
    errorband.SetLineColor("black")
    #    errorband.SetFillStyle(3344)
    
    errorband.SetFillStyle(3444)
    errorband.SetFillColor("black")
    errorband.DrawClone("E2P SAME")


    stack.sum.SetFillStyle(0)
    stack.sum.SetLineColor("black")
    stack.sum.SetLineWidth(2)
    stack.sum.SetMarkerSize(0)
    
    stack.sum.DrawClone("HIST SAME")




def drawEfficiency(stack,stack_den):
    temphist = stack.sum.Clone()

    #temphist = stack.sum.Clone()
    stack.sum.Divide(stack_den.sum)
    stack.sum.SetLineColor("black")
    stack.sum.SetLineWidth(4)
    stack.sum.Draw("EP SAME")
    

def drawSignals(signals):
    for signal in signals:
        signal.Draw("Hist SAME X0")

def drawsignalobjects(backgroundstacks):
    for LegendEntry in backgroundstacks:
        if 'Signal' in LegendEntry:
            backgroundstacks[LegendEntry].sum.Draw("Hist SAME X0")


def drawData(datastack,Region,state):
    BLINDED = state['BLINDED']
    if not BLINDED:
        datastack.sum.SetMarkerStyle('circle')
        datastack.sum.SetMarkerSize(2) 
        datastack.sum.SetLineColor('black')
        datastack.sum.SetLineWidth(2)
        datastack.sum.Draw("SAME EP")

def drawDataDiagnostics(datastack,Region,state):
    BLINDED = state['BLINDED']
    if not BLINDED:
        datastack.sum.SetMarkerStyle('circle')
        datastack.sum.SetMarkerSize(2)
        datastack.sum.SetLineWidth(2)
        datastack.sum.Draw("SAME EP")


#def drawRatio(histRatio,stack,Region,BLINDED,nbins,xmin,xmax):
    #histRatio = datastack.sum.Clone()
    #histRatio.merge_bins([(0, 1), (-2, -1)])

#    tempDataStack = histRatio.sum.Clone()
#    ratioMinimum=0.001
#    ratioMaximum=2
#    if stack.sum.integral(overflow=True) != 0:
#        average = tempDataStack.integral(overflow=True)/stack.sum.integral(overflow=True)
#    else:   
#        average = 0.0
#    histRatio.SetMinimum(ratioMinimum)
#    histRatio.SetMaximum(ratioMaximum)
#    histRatio.yaxis.divisions = 5
#    histRatio.Divide(stack.sum)##
#
#    if not BLINDED: 
#        histRatio.Draw("PE0")
#    
#    line = Line(float(xmin)+1e-2*float(xmax),1.,float(xmax)-1e-2*float(xmax),1.);
#    line.SetLineWidth(4);
#    line.SetLineColor("red");
#    line.Draw()#
#
#    line2 = Line(float(xmin),average,float(xmax),average)
#    line2.SetLineStyle("dashed")
#    line2.SetLineWidth(4)
#    line2.SetLineColor("blue")
#    if stack.sum.integral(overflow=True) != 0:
#        line2.Draw()
#
#    if not BLINDED:
#        histRatio.Draw("SAME E0P")#
#
#    MCerrorband = stack.sum.Clone()
#    MCerrorband.SetLineWidth(10)
#    MCerrorband.SetFillStyle(3244)
#    MCerrorband.SetFillColor(922)
##
#
#    for i in range(1,int(hist.GetNbinsX())+1):
#        if stack.sum.GetBinContent(i) != 0:
#            xcoord = stack.sum.GetBinCenter(i)
#
#            if tempDataStack.GetBinContent(i)/stack.sum.GetBinContent(i) >= 2:
#                xcoord = stack.sum.GetBinCenter(i)
#                arrow = Arrow(xcoord,1.67,xcoord,1.87,0.015,"|>")
#                arrow.SetAngle(50)
#                arrow.SetLineWidth(6)
#                arrow.SetLineColor(2)
#                arrow.SetFillColor(2)
#                arrow.Draw()
#            elif tempDataStack.GetBinContent(i)/stack.sum.GetBinContent(i) <= -2:
#                xcoord = stack.sum.GetBinCenter(i)
#                arrow = Arrow(xcoord,0.33,xcoord,0.13,0.015,"|>")
#                arrow.SetAngle(50)
#                arrow.SetLineWidth(6)
#                arrow.SetLineColor(2)
#                arrow.SetFillColor(2)
#                arrow.Draw();
#            else:
#                ycoord = tempDataStack.GetBinContent(i)/stack.sum.GetBinContent(i)
#                num  = (tempDataStack.GetBinContent(i) - stack.sum.GetBinContent(i))  
#                den  = math.sqrt(tempDataStack.GetBinError(i)**2 + stack.sum.GetBinError(i)**2)
#                sigma = num/den 
#                binwidth = stack.sum.GetBinWidth(i)
#                sigmatext = TLatex(xcoord-0.35*binwidth,0.3 ,str(round(sigma,1)))
###                sigmatext.
#                sigmatext.SetTextColor(2)#

#                if ycoord != 0:
#                    sigmatext.Draw()

#        mcerror = 0.0
#        content = stack.sum.GetBinContent(i)
#        error = stack.sum.GetBinError(i)
#        if content != 0 :
#            mcerror = (content+error)/content - 1.0 
#        MCerrorband.SetBinContent(i,1)
#        MCerrorband.SetBinError(i,mcerror)
#        
#    MCerrorband.Draw("E2PSAME")
#    return histRatio



def drawRatioPlot(numerator,denominator,state):

    defaultlabelsize = rootpyglobals.defaultlabelsize
    BLINDED = state['BLINDED']
    if not BLINDED:
        tempDataStack = numerator.sum.Clone()
    else: 
        tempDataStack = denominator.sum.Clone()

    tempDataStack.SetLineColor('black')
    
    nbins = tempDataStack.GetNbinsX()
    
    dx = (tempDataStack.GetBinCenter(int(2))- tempDataStack.GetBinCenter(int(1)))/2
    xmin = tempDataStack.GetBinCenter(int(1)) -dx
    xmax = tempDataStack.GetBinCenter(int(nbins)) +dx
    
    ratioMinimum=0.001
    ratioMaximum=2
    if denominator.sum.integral(overflow=True) != 0:
        average = tempDataStack.integral(overflow=True)/denominator.sum.integral(overflow=True)
    else:   
        average = 0.0

    tempDataStack.SetMinimum(ratioMinimum)
    tempDataStack.SetMaximum(ratioMaximum)
    tempDataStack.yaxis.divisions = 5
    tempDataStack.Divide(denominator.sum)

    if not BLINDED: 
        tempDataStack.Draw("PE0")
    else:
        tempDataStack.Draw("HIST P")

    if not BLINDED:
        tempDataStack.Draw("SAME E0P")
    else:
        tempDataStack.Draw("SAME HIST P")

    MCerrorband = denominator.sum.Clone()
    MCerrorband.SetLineWidth(5)
    MCerrorband.SetLineColor("black")
    MCerrorband.SetFillStyle(3344)
    MCerrorband.SetFillColor(922)

    sigma = denominator.sum.Clone()
    sigma.SetMarkerStyle('circle')
    sigma.SetMarkerColor(kRed)
    sigma.SetMarkerSize(2)


    if not BLINDED:
        for i in range(1,int(nbins)+1):
            if denominator.sum.GetBinContent(i) != 0:
                
                xcoord = denominator.sum.GetBinCenter(i)##

                if tempDataStack.GetBinContent(i)/denominator.sum.GetBinContent(i) >= 2:
    #                xcoord = stack.sum.GetBinCenter(i)
                    arrow = Arrow(xcoord,1.67,xcoord,1.87,0.015,"|>")
                    arrow.SetAngle(50)
                    arrow.SetLineWidth(6)
                    arrow.SetLineColor(2)
                    arrow.SetFillColor(2)
                    arrow.Draw()
                elif tempDataStack.GetBinContent(i)/denominator.sum.GetBinContent(i) <= -2:
    #                xcoord = stack.sum.GetBinCenter(i)
                    arrow = Arrow(xcoord,0.33,xcoord,0.13,0.015,"|>")
                    arrow.SetAngle(50)
                    arrow.SetLineWidth(6)
                    arrow.SetLineColor(2)
                    arrow.SetFillColor(2)
                    arrow.Draw();
                ycoord = tempDataStack.GetBinContent(i)/denominator.sum.GetBinContent(i)
                num  = (tempDataStack.GetBinContent(i) - denominator.sum.GetBinContent(i))  
                den  = math.sqrt(tempDataStack.GetBinError(i)**2 + denominator.sum.GetBinError(i)**2)
#                try:
#                    sigma = num/den 
#                except:
#                    sigma = 0.0

                binwidth = denominator.sum.GetBinWidth(i)
                inputsigma = round(ROOT.RooStats.NumberCountingUtils.BinomialObsZ(numerator.sum.GetBinContent(i),denominator.sum.GetBinContent(i), (denominator.sum.GetBinError(i)+numerator.sum.GetBinError(i))/denominator.sum.GetBinContent(i) ),1)
                if "-" in str(inputsigma):
                    inputsigma = str(round(inputsigma,1))
                else:
                    inputsigma = "+" + str(round(inputsigma,1))
#                print "sigma::BionominalObsZ:: " + str(inputsigma)

#                print str(binwidth)
                sigmatext = TLatex(xcoord-0.30*binwidth,0.07 ,inputsigma)
                sigmatext.SetTextColor(16)
                sigmatext.SetTextSize(0.025)
#                sigmatext.SetNDC()                
                if "inf" not in inputsigma:
                    if abs(float(inputsigma)) > 1.0:
                        sigmatext.Draw("SAME")
                

    for i in range(1,int(nbins)+1):
        if (denominator.sum.GetBinContent(i) != 0.0):
            mcerror = 0.0
            content = denominator.sum.GetBinContent(i)
            error = denominator.sum.GetBinError(i)
            if content != 0 :
                mcerror = (content+error)/content - 1.0 
            MCerrorband.SetBinContent(i,1)
#            if state['Region'].startswith("SR"):
#                MCerrorband.SetBinError(i,math.sqrt(mcerror**2+(0.2*content)**2))
#            else:
            MCerrorband.SetBinError(i,mcerror)
   
    MCerrorband.Draw("E2P SAME")
    line = Line(float(xmin)+1e-2*float(xmax),1.,float(xmax)-1e-2*float(xmax),1.);
    line.SetLineWidth(3);
    line.SetLineColor("red");
    line.Draw()

    line2 = Line(float(xmin),average,float(xmax),average)
    line2.SetLineStyle("dashed")
    line2.SetLineWidth(3)
    line2.SetLineColor("blue")
    if denominator.sum.integral(overflow=True) != 0:
        line2.Draw()



    if not BLINDED:
        tempDataStack.Draw("SAME E0P")
    else:
        tempDataStack.Draw("SAME HIST P")

    tempDataStack.yaxis.SetTitle("Data/SM")
    tempDataStack.yaxis.SetTitleSize(40)
    tempDataStack.yaxis.SetTitleFont(43)


    if not BLINDED:
        for i in range(1,int(nbins)+1):
            if denominator.sum.GetBinContent(i) != 0:
                xcoord = denominator.sum.GetBinCenter(i)

                if tempDataStack.GetBinContent(i)/denominator.sum.GetBinContent(i) >= 2:
    #                xcoord = stack.sum.GetBinCenter(i)
                    arrow = Arrow(xcoord,1.67,xcoord,1.87,0.015,"|>")
                    arrow.SetAngle(50)
                    arrow.SetLineWidth(6)
                    arrow.SetLineColor(2)
                    arrow.SetFillColor(2)
                    arrow.Draw()
                elif tempDataStack.GetBinContent(i)/denominator.sum.GetBinContent(i) <= -2:
    #                xcoord = stack.sum.GetBinCenter(i)
                    arrow = Arrow(xcoord,0.33,xcoord,0.13,0.015,"|>")
                    arrow.SetAngle(50)
                    arrow.SetLineWidth(6)
                    arrow.SetLineColor(2)
                    arrow.SetFillColor(2)
                    arrow.Draw();


    #sigma.Draw("PSAME")
#    tempDataStack.yaxis.SetTitle("Data/SM")
#    tempDataStack.yaxis.CenterTitle()
    tempDataStack.yaxis.SetTitleSize(30)
    tempDataStack.yaxis.SetTitleFont(43)
    tempDataStack.yaxis.SetTitleOffset(2)
#    tempDataStack.xaxis.SetTitle(xlabel)
    tempDataStack.xaxis.SetTitleSize(30)
    tempDataStack.xaxis.SetTitleFont(43)
    tempDataStack.xaxis.SetTitleOffset(3.4)
    
    tempDataStack.xaxis.set_label_size(0.025*3)
    tempDataStack.yaxis.set_label_size(0.025*3)


    return tempDataStack
