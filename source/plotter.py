#from rootpyPlotter_modules import *
# generic python imports 

import os.path
import sys
import math
import argparse
from decimal import Decimal
import time
from collections import OrderedDict
from itertools import izip
from decimal import Decimal

# rootpy imports 
from rootpy import ROOT
from rootpy.io import root_open
from rootpy.io import Directory
from rootpy.plotting import F1, Hist, HistStack, Canvas, Legend, Pad,Hist2D,Profile
from rootpy.plotting.shapes import Line,Arrow
from rootpy.plotting.utils  import draw
from rootpy import asrootpy
from rootpy.tree import Cut
from rootpy.tree import Tree
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange


# vast majority of functions are in these tool files. 
import rootpyglobals
import plotlabels 
import legendtools
import stacktools 
import canvastools
import outputtools
import drawtools
import variabletools 
import styletools
import plottools
import regiontools


def main():

    styletools.initPlotStyle()

    t0 = time.time()
    
    parser = argparse.ArgumentParser(description='Optional app description')
    
    parser.add_argument('--output'         , '-o'   , type=str, default="rootpyoutput", help='Provide a location for output of Plots')
    parser.add_argument('--region'         , '-r'   , type=str, default ="PRE3L", help='Specify which Region you wish to run over [See regiondefinitions.py]'  )
    parser.add_argument('--ratioplot'      , '-rp'  , type=bool, default=True, help='produce Ratio subplot [None, Ratio, Residual]')
    parser.add_argument('--regionbreakdown', '-c'   , type=bool, default=False, help='Produce a breakdown of the Region [True, False]')
    parser.add_argument('--dataperiods'    , '-p'   , type=str , default='1516', help='Specify which data periods to include. Options: [1516, 17, 18, 15-17, 17-18, 15-18]')
    parser.add_argument('--applynf'        , '-nf'  , type=bool, default=False, help='Apply Normalisation Factors ')
    parser.add_argument('--usefakes'       , '-uf'   , default=True,action='store_false', help='Use Matrix Method Fakes Estimation ')
    args = parser.parse_args()
    
    args.usefakes  = False;
    region         = args.region 
    outputfolder   = args.output
    state = plottools.defineState(args)

    if state['Region'].startswith("SR"):
        state['BLINDED'] = True
    else:
        state['BLINDED'] = False


    sampleLocations = OrderedDict()
    sampleLocations['1516'] = "/data/coepp/THREELEP/OUTPUT/"
    sampleLocations['EW'] = "/home/a1707313/rootpyPlotter/EW_ntuples"
    sampleLocations['17']   = "/fast/users/a1608402/samples/SUSY2_Bkgs_mc16cd/Tight"
    sampleLocations['18']   = "/fast/users/a1608402/samples/SUSY2_Bkgs_mc16e/Tight"

    suffix='_merged_processed_Tight.root'


    samples = OrderedDict([
        ('data1516',{'type':'data','year':'1516','legend':'Data','fillcolor':0,'linecolor':0,'filename':'data1516'+suffix,'location':sampleLocations['1516']}),
        ('triboson1516',{'type':'bkg','year':'1516','legend':'Triboson','fillcolor':kBlue-2,'filename':'triboson'+suffix,'location':sampleLocations['1516']}),
        ('topOther1516',{'type':'bkg'  , 'year':'1516','legend':'Top other','fillcolor':kPink-5,'filename':'topOther'+suffix,'location':sampleLocations['1516']}),
        ('higgs1516'   ,{'type':'bkg'  , 'year':'1516', 'legend':'Higgs'    , 'fillcolor':kYellow-9   , 'filename':'higgs'+suffix,'location':sampleLocations['1516']}),
        #('fakes1516'   ,{'type':'fakes', 'year':'1516', 'legend':'Fakes'    , 'fillcolor':kGray+2   , 'filename':'fakes'+suffix,'location':sampleLocations['1516']}),
        ('diboson1516' ,{'type':'bkg'  , 'year':'1516', 'legend':'Diboson'  , 'fillcolor':kAzure-9      , 'filename':'diboson'+suffix,'location':sampleLocations['1516']}),
        #('signal1516'  ,{'type':'sig'  , 'year':'1516', 'legend':'Signal'   , 'fillcolor':0, 'linecolor': kRed+2, 'filename':signal+bkg_suffix\})
#        ('signal4000',{'type':'sig', 'year':'4000', 'legend':'Signal', 'fillcolor':0, 'linecolor':kRed+2, 'filename':'EW-4000-sample.root', 'location':sampleLocations['4000']})
        ])

    
    regionLabel = "3L_NETWORK"
    regionselection     = Cut("is3Lep&&lept1Pt>25&&lept2Pt>25&&lept3Pt>20&&mll>81.2&&mll<101.2&&met>120&&min_mt<110")    #mll>75&&mll<105") 
#    regionselection_4000     = Cut("lep1pt>25&&lep2pt>25&&lep3pt>20&&mll>75&&mll<105")
    cutnames    = ["blank"]
    regionType  = "VR"


    regionInformation = {} 
    regionInformation['region']      = region
    regionInformation['regionlabel'] = regionLabel
    regionInformation['regiontype']  = regionType

    
    weight="weight"
    
    
    #    LuminosityDictionary =  luminosity() 
    
    
    WeightDictionary     = {'data':weight, 'bkg':weight,'fakes':weight, 'sig':weight}
    
    trees     = OrderedDict()
    rootfiles = OrderedDict()
    for sample in samples:
        year              = samples[sample]['year']
        filename          = samples[sample]['filename']
        filelocation      = samples[sample]['location']
        rootfiles[sample] = root_open(os.path.join(filelocation,filename))
        trees[sample]     = stacktools.getTreeNames(sample,samples,rootfiles)


    variables = variabletools.getVariables(region)

    outputyields = True    
    for variable in variables:
        print variable

        units     = variables[variable]['units']
        nbins     = int(variables[variable]['nbins'])
        xmin      = float(variables[variable]['xmin'])
        xmax      = float(variables[variable]['xmax'])
        xlabel    = variables[variable]['latex']
        ylabel    = plotlabels.getYlabel(units,nbins,xmin,xmax)
        

        canvas    = canvastools.createCanvas(state)
        histpad   = canvastools.createHistogramPad(state)
        ratiopad  = canvastools.createRatioPad(state)
        
        
        histpad.cd()

        stack     = stacktools.createSampleStack(samples)

        for sample in samples:
            type = samples[sample]['type']
            legendEntry = samples[sample]['legend']
            if "Data" not in legendEntry and "Signal" not in legendEntry: 
                selection = Cut("36.2e3*trigMatch_2LTrigOR*weight") * regionselection        # apply weight to bkg samples - where does this weight come from? 
#            elif "Signal" in legendEntry: 
#                selection = regionselection_4000    # no 'is3Lep', lept1Pt, lept2Pt, lept3Pt in EW-4000-signal.root. Also only plot variables in common in variabletools.py e.g. mll, met
            else:
                selection = regionselection # regionselection is choosing 3L, cut on leptpts, choosing mll in region for Z mass (defining the VR) 
                
            temphist   =  trees[sample].Draw(variable, hist= Hist(nbins,xmin,xmax),selection = selection )     # trees is ordereddict of the Trees in each sample 
            temphist   =  temphist.merge_bins([(0,1),  (nbins,nbins+1)  ])
            temphistentry,temphisterror = temphist.integral(overflow=True,error=True)    # integral over all entries with overflow bin included? How is error calculated? 
            if outputyields == True:
                print sample + ": " + str(round(temphistentry,2)) + "\pm" + str(round(temphisterror,2))
            styletools.setSampleStyle(temphist,sample,samples)
            stack[type][legendEntry].Add(temphist.Clone()) 

        processedstacks, breakdowns = stacktools.processStack(stack,state)
        backgrounds         = processedstacks['background']
        data                = processedstacks['data']
        signals             = processedstacks['signal']
        
        info = []
        
        for hist in backgrounds:
            info.append([hist,hist.integral(overflow=True) ])


        del backgrounds
        backgrounds = HistStack()
        for histogram,entries in sorted(info, key=lambda tup: tup[1]):
            backgrounds.Add(histogram.Clone())


        histpad.cd()


        yminimum,ymaximum = 1e-2,1e5
        #yminimum, ymaximum = plotlabels.RegionYrange(Region)
        
        backgrounds.SetMinimum(yminimum)
        backgrounds.SetMaximum(ymaximum)
                
        # draw all the backgrounds - stacked 
        backgrounds.Draw()

        # make the statistical error band and draw it 
        errorband = backgrounds.sum.Clone()
        errorband.SetMarkerSize(0)
        errorband.SetLineColor("black")
        errorband.SetFillStyle(3344)
        errorband.SetFillColor("black")
        errorband.Draw("E2P SAME")
        
        #draw the total yield over the top 
        backgrounds.sum.SetFillStyle(0)
        backgrounds.sum.SetLineColor("black")
        backgrounds.sum.SetLineWidth(2)
        backgrounds.sum.SetMarkerSize(0)
        backgrounds.sum.Draw("HIST SAME")
        
        
        labelmargin      = rootpyglobals.labelmargin
        defaultlabelsize = rootpyglobals.defaultlabelsize

        backgrounds.sum.yaxis.SetTitle(ylabel)
        backgrounds.sum.yaxis.SetTitleOffset(2)
        backgrounds.sum.yaxis.SetTitleSize(30)

        plotlabels.drawXandYlabels(backgrounds,data,xlabel,ylabel,state,histpad,ratiopad)
        
        for signal in signals:
            signal.Draw("Hist SAME X0")


        if not state['BLINDED']:     # draw data if unblinded 
            data.sum.SetMarkerStyle('circle')
            data.sum.SetMarkerSize(2)
            data.sum.SetLineColor('black')
            data.sum.SetLineWidth(2)
            data.sum.Draw("SAME EP")

        ratiopad.cd()
        ratioplot = drawtools.drawRatioPlot(data,backgrounds,state)
        ratioplot.yaxis.SetTitle("Data/SM")
        ratioplot.yaxis.CenterTitle()
        ratioplot.xaxis.SetTitle(xlabel)
                
        ROOT.gPad.RedrawAxis()
        
        histpad.cd()

        plotlabels.drawPlotInformation(state)
        plotlabels.drawTopLeftInformation(breakdowns,state)
        legendtools.drawDataLegend(breakdowns,state)
        legendtools.drawBackgroundLegend(breakdowns,state)
        
        os.system("mkdir -p " + outputfolder + "/Data" + year )
        os.system("mkdir -p " + outputfolder + "/Data" + year + "/" + region)
        outputtools.outputRegionDiagnostics(breakdowns,state)

        filenamevariable = variable.replace("/","_").replace("_1000","")
        canvas.Print(outputfolder + "/Data" + year +  "/" + region + "/"+ filenamevariable+ "_" + region + ".png")
#        canvas.Print(outputfolder + "/Data" + year + "/" + region + "/"+ filenamevariable+ "_" + region + ".pdf")
        outputyields = False       # only see output yields for first variable 




if __name__ == "__main__":
    main() 

