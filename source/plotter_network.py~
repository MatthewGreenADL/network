# from rootpyPlotter_modules import *
# generic python imports 

import os.path
import sys
import math
import argparse
from decimal import Decimal
import time
from collections import OrderedDict
#from itertools import izip
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
import stacktools_network 
import canvastools
import outputtools
import drawtools
import variabletools_network
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
#    sampleLocations['1516'] = "/data/coepp/THREELEP/OUTPUT/"
#    sampleLocations['4000'] = "/hpcfs/users/a1707313/atlas/rootpyPlotter/input_local/"
    sampleLocations['4001'] = "/hpcfs/users/a1707313/atlas/3L_ISR_networkCalculations/networkmetrics/clumpingtests/"
    sampleLocations['4000'] = "/hpcfs/users/a1707313/atlas/3L_ISR_networkCalculations/networkmetrics/"
#    sampleLocations['17']   = "/fast/users/a1608402/samples/SUSY2_Bkgs_mc16cd/Tight"
#    sampleLocations['18']   = "/fast/users/a1608402/samples/SUSY2_Bkgs_mc16e/Tight"

#    suffix='_euclidean_nsi_local_soffer_clustering_l_80-0.root'
    suffix='.root'
#    midfix ='_cityblock_nsi_degree_l_100-0'
#    midfix ='_cityblock_nsi_harmonic_closeness_l_100-0'
#    midfix ='_cityblock_nsi_average_neighbors_degree_l_100-0'
#    midfix ='_cityblock_nsi_exponential_closeness_l_100-0'
#    midfix ='_cityblock_nsi_local_clustering_l_100-0'
#    midfix ='_correlation_nsi_harmonic_closeness_l_0-03'
#    midfix ='_correlation_nsi_degree_l_0-03'
#    midfix ='_cosine_nsi_degree_l_0-015'
#    midfix ='_cosine_nsi_degree_l_0-1'
#    midfix ='_cosine_nsi_local_soffer_clustering_l_0-015'
    midfix ='_euclidean_nsi_degree_l_70-0'
#    midfix ='_euclidean_nsi_degree_l_70-0'
#    midfix ='_mahalanobis_nsi_betweenness_l_1-0'
#    midfix ='_mahalanobis_nsi_exponential_closeness_l_2-5'
#    midfix ='_mahalanobis_nsi_max_neighbors_degree_l_2-5'

    samples = OrderedDict([
#        ('data',{'type':'data','year':'1516','legend':'Data','fillcolor':0,'linecolor':0,'filename':'data'+midfix+'_dataonly'+suffix,'location':sampleLocations['4000']}),

#        ('data',{'type':'data','year':'1516','legend':'Data','fillcolor':0,'linecolor':0,'filename':'data_correlation_nsi_degree_l_0-03_dataonly'+suffix,'location':sampleLocations['4000']}),
#        ('ttbar',{'type':'bkg','year':'1516','legend':'ttbarDilep','fillcolor':kGray+2,'filename':'ttbar'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
#        ('triboson',{'type':'bkg','year':'1516','legend':'Triboson','fillcolor':kBlue-2,'filename':'triboson'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
#        ('topOther',{'type':'bkg', 'year':'1516','legend':'Top other','fillcolor':kPink-5,'filename':'topOther'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
#        ('singleTop',{'type':'bkg', 'year':'1516','legend':'Single top','fillcolor':kOrange-5,'filename':'singleTop'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
#        ('higgs'   ,{'type':'bkg', 'year':'1516', 'legend':'Higgs', 'fillcolor':kYellow-9, 'filename':'higgs'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
#        ('diboson' ,{'type':'bkg', 'year':'1516', 'legend':'Diboson', 'fillcolor':kAzure-9 , 'filename':'diboson'+midfix+'_bgonly_mock4'+suffix,'location':sampleLocations['4000']}),
\
#        ('singleTop' ,{'type':'bkg', 'year':'1516', 'legend':'TopOtherFull (DibosonLittle)', 'fillcolor':0, 'linecolor':kGreen , 'filename':'topOther_DibosonLittleTopOtherOrig_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4001']}),
#        ('diboson' ,{'type':'bkg', 'year':'1516', 'legend':'TopOtherFull (DibosonTiny)', 'fillcolor':0,'linecolor':kAzure , 'filename':'topOther_DibosonTinyTopOtherOrig_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4001']}),
#        ('topOther' ,{'type':'bkg', 'year':'1516', 'legend':'TopOtherFull (DibosonFull)', 'fillcolor':0, 'linecolor':kOrange , 'filename':'topOther_DibosonOrigTopOtherOrig_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4001']}),
#        ('ttbar' ,{'type':'bkg', 'year':'1516', 'legend':'TopOtherBig (DibosonSmall)', 'fillcolor':0, 'linecolor':kPink-5 , 'filename':'topOther_DibosonSmallTopOtherBig_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4001']}),

#        ('diboson' ,{'type':'bkg', 'year':'1516', 'legend':'Toy2 (10000:10000)', 'fillcolor':0,'linecolor':kPink+10 , 'filename':'toydata/euclidean/toydata2_10000__toydata1_10000_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),
#        ('singleTop' ,{'type':'bkg', 'year':'1516', 'legend':'Toy2 (1000:10000)', 'fillcolor':0, 'linecolor':kOrange+8, 'filename':'toydata/euclidean/toydata2_10000__toydata1_1000_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),
#        ('ttbar' ,{'type':'bkg', 'year':'1516', 'legend':'Toy2 (200:10000)', 'fillcolor':0,'linecolor':kRed , 'filename':'toydata/euclidean/toydata2_10000__toydata1_200_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),
#        ('topOther' ,{'type':'bkg', 'year':'1516', 'legend':'Toy1 (10000:10000)', 'fillcolor':0,'linecolor':kAzure+8 , 'filename':'toydata/euclidean/toydata1_10000__toydata1_10000_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),
#        ('triboson' ,{'type':'bkg', 'year':'1516', 'legend':'Toy1 (1000:10000)', 'fillcolor':0, 'linecolor':kBlue , 'filename':'toydata/euclidean/toydata1_1000__toydata1_1000_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),
#        ('higgs' ,{'type':'bkg', 'year':'1516', 'legend':'Toy1 (200:10000)', 'fillcolor':0,'linecolor':kBlue-9 , 'filename':'toydata/euclidean/toydata1_200__toydata1_200_toydata2_10000_euclidean_nsi_betweenness_l_12-0_bgonly.root','location':sampleLocations['4001']}),

        ('triboson' ,{'type':'bkg', 'year':'1516', 'legend':'Toy unweighted (N=20000)', 'fillcolor':0, 'linecolor':kBlue , 'filename':'toydata/neighbourassignment/euclidean/toydata3_20000euclidean_nsi_degree_l_12-0_bgonly.root','location':sampleLocations['4001']}),
        ('higgs' ,{'type':'bkg', 'year':'1516', 'legend':'Random weighted (N=384)', 'fillcolor':0, 'linecolor':kBlue-9 , 'filename':'toydata/neighbourassignment/euclidean/smallsample_6000_weightedeuclidean_nsi_degree_l_12-0_bgonly.root','location':sampleLocations['4001']}),


#        ('diboson' ,{'type':'bkg', 'year':'1516', 'legend':'Diboson', 'fillcolor':kAzure-9 , 'filename':'diboson_DibosonTinyTopOtherOrig_euclidean_nsi_local_soffer_clustering_l_70-0_bgonly.root','location':sampleLocations['4001']}),
#        ('topOther',{'type':'bkg', 'year':'1516','legend':'Top other','fillcolor':kPink-5,'filename':'topOther_DibosonTinyTopOtherOrig_euclidean_nsi_local_soffer_clustering_l_70-0_bgonly.root','location':sampleLocations['4001']}),


#        ('randomdiboson' ,{'type':'bkg', 'year':'1516', 'legend':'Diboson(Random)', 'fillcolor':kAzure-9 , 'filename':'dibosononlychecks/randomdibosononly_nBins3_Nrand100000_euclidean_nsi_degree_l_700-0_bgonly.root','location':sampleLocations['4000']}),
#        ('originaldiboson' ,{'type':'bkg', 'year':'1516', 'legend':'Diboson(Original)', 'fillcolor':kOrange-5 , 'filename':'dibosononlychecks/originaldibosononly_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4000']}),
#        ('diboson' ,{'type':'bkg', 'year':'1516', 'legend':'Diboson', 'fillcolor':kAzure-9 , 'filename':'dibosononlychecks/originaldibosononly_euclidean_nsi_degree_l_70-0_bgonly.root','location':sampleLocations['4000']}),
        #('fakes1516'   ,{'type':'fakes', 'year':'1516', 'legend':'Fakes'    , 'fillcolor':kGray+2   , 'filename':'fakes'+suffix,'location':sampleLocations['1516']}),
#        ('signal'  ,{'type':'sig','year':'1516','legend':'Signal','fillcolor':0,'linecolor': kRed+2, 'filename':'signal'+midfix+'_bgonly_mock'+suffix,'location':sampleLocations['4000']})
        #('signal4000',{'type':'sig', 'year':'4000', 'legend':'Signal', 'fillcolor':0, 'linecolor':kRed+2, 'filename':'EW-4000-sample.root', 'location':sampleLocations['4000']})

#        ('data',{'type':'data','year':'1516','legend':'Data','fillcolor':0,'linecolor':0,'filename':'data'+midfix+'_dataonly'+suffix,'location':sampleLocations['4000']}),
        ])

    
    regionLabel = "3L_NETWORK"
    regionselection     = Cut("") 
#    regionselection     = Cut("lept1Pt>25&&lept2Pt>25&&lept3Pt>20") 
#    regionselection     = Cut("is3Lep&&lept1Pt>25&&lept2Pt>25&&lept3Pt>20&&mll>75&&mll<105&&min_mt<110&&met>120") 
#    regionselection_4000     = Cut("lep1pt>25&&lep2pt>25&&lep3pt>20&&mll>75&&mll<105&&met>120")
    cutnames    = ["blank"]
    regionType  = "VR"

    regionInformation = {} 
    regionInformation['region']      = region
    regionInformation['regionlabel'] = regionLabel
    regionInformation['regiontype']  = regionType
    
    eventweight="eventweight"
       
    #    LuminosityDictionary =  luminosity() 
    
    WeightDictionary     = {'data':eventweight, 'bkg':eventweight,'fakes':eventweight, 'sig':eventweight}
    
    trees     = OrderedDict()
    rootfiles = OrderedDict()
    for sample in samples:
        year              = samples[sample]['year']
        filename          = samples[sample]['filename']
        filelocation      = samples[sample]['location']
        rootfiles[sample] = root_open(os.path.join(filelocation,filename))
        trees[sample]     = stacktools_network.getTreeNames(sample,samples,rootfiles)

    variables = variabletools_network.getVariables(region)

    print("region: " + region)
    print("variables are: ")
    for variable in variables:
        print(variable)

    outputyields = True    
    for variable in variables:
        print(variable)

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

        stack     = stacktools_network.createSampleStack(samples)

        for sample in samples:
            type = samples[sample]['type']
            legendEntry = samples[sample]['legend']
            if "Data" not in legendEntry and "Signal" not in legendEntry:
#                selection = Cut("36.2e3*trigMatch_2LTrigOR*eventweight") * regionselection 
                selection = Cut("eventweight") * regionselection 

            if "toy1:200" not in legendEntry:
                selection = Cut("eventweight") * regionselection 
            if "toy1:200" in legendEntry:
                selection = Cut("eventweight") * regionselection 
#                selection = regionselection 
#            elif "Signal" in legendEntry: 
#                selection = regionselection_4000    # no 'is3Lep', lept1Pt, lept2Pt, lept3Pt in EW-4000-signal.root 
#            else:
#                selection = regionselection # regionselection is choosing 3L, cut on leptpts, choosing mll in region for Z mass 
#            else: # data1516
#                selection = Cut("eventweight") * regionselection  #                selection = regionselection
#                selection = Cut("9223./52.")*regionselection # check distribution shapes (change this)
                
            temphist   =  trees[sample].Draw(variable, hist= Hist(nbins,xmin,xmax),selection = selection )     # trees is ordereddict of the Trees in each sample 
            temphist   =  temphist.merge_bins([(0,1),  (nbins,nbins+1)  ])
            temphistentry,temphisterror = temphist.integral(overflow=True,error=True)
            if outputyields == True:
                print(sample + ": " + str(round(temphistentry,2)) + "\pm" + str(round(temphisterror,2)))
            styletools.setSampleStyle(temphist,sample,samples)
            stack[type][legendEntry].Add(temphist.Clone()) 

        processedstacks, breakdowns = stacktools_network.processStack(stack,state)
        backgrounds         = processedstacks['background']
        data                = processedstacks['data']
        signals             = processedstacks['signal']
        
        info = []
        
        for hist in backgrounds:
            info.append([hist,hist.integral(overflow=True) ])
            print("integral ", hist, " ", hist.integral(overflow=True))

#            if 'DibosonTiny ' in legendEntry:
#                hist.SetFillColorAlpha(kAzure,0.35)
#            if 'DibosonFull ' in legendEntry:
#                hist.SetFillColorAlpha(kOrange,0.35)
#            if 'DibosonSmall ' in legendEntry:
#                hist.SetFillColorAlpha(kOrange,0.35)
#            if 'DibosonLittle ' in legendEntry:
#                hist.SetFillColorAlpha(kPink-5,0.35)
#            if 'TOY2 (toy1:200, toy2:10000)'

        del backgrounds
        backgrounds = HistStack()
        for histogram,entries in sorted(info, key=lambda tup: tup[1]):
            backgrounds.Add(histogram.Clone())


        histpad.cd()


#        yminimum,ymaximum = 1e-2,1e8
        yminimum,ymaximum = 50,1e6
        #yminimum, ymaximum = plotlabels.RegionYrange(Region)
        
        backgrounds.SetMinimum(yminimum)
        backgrounds.SetMaximum(ymaximum)
                
        # draw all the backgrounds - stacked 
        backgrounds.Draw('nostack') # .Draw()

        # make the statistical error band and draw it 
#        errorband = backgrounds.sum.Clone()
#        errorband.SetMarkerSize(0)
#        errorband.SetLineColor("black")
#        errorband.SetFillStyle(3344)
#        errorband.SetFillColor("black")
#        errorband.Draw("E2P SAME")
        
        #draw the total yield over the top 
#        backgrounds.sum.SetFillStyle(0)
#        backgrounds.sum.SetLineColor("kBlack")
#        backgrounds.sum.SetLineWidth(2)
#        backgrounds.sum.SetMarkerSize(0)
#        backgrounds.sum.Draw("HIST SAME")
        
        
        labelmargin      = rootpyglobals.labelmargin
        defaultlabelsize = rootpyglobals.defaultlabelsize

#        backgrounds.sum.yaxis.SetTitle(ylabel)
#        backgrounds.sum.yaxis.SetTitleOffset(2)
#        backgrounds.sum.yaxis.SetTitleSize(30)

        plotlabels.drawXandYlabels(backgrounds,data,xlabel,ylabel,state,histpad,ratiopad)       #  plotlabels.drawXandYlabels(backgrounds,data,xlabel,ylabel,state,histpad,ratiopad)
        
        for signal in signals:
            signal.Draw("Hist SAME X0")


#        if state['BLINDED']:     # draw data if unblinded # if not state['BLINDED'] (removed 'not') # turn this block on 
#            data.sum.SetMarkerStyle('circle')
#            data.sum.SetMarkerSize(2)
#            data.sum.SetLineColor('black')
#            data.sum.SetLineWidth(2)
#            data.sum.Draw("SAME EP")

#        for sample in samples:
#            legendEntry = samples[sample]['legend']
#            if("Toy1 (200:20000)" in legendEntry):
#                rationumerator = sample
#            if("Toy1 (10000:10000)" in legendEntry):
#                ratiodenominator = sample
        rationumerator = backgrounds[1]
        ratiodenominator = backgrounds[0]


        ratiopad.cd() # turn this block on 
        ratioplot = drawtools.drawRatioPlot(rationumerator,ratiodenominator,state) #(backgrounds,backgrounds,state) # (data,backgrounds,state)
        ratioplot.yaxis.CenterTitle()
        ratioplot.xaxis.SetTitle(xlabel)

#        ratioplot.yaxis.SetTitle("Data/SM")
#        ratioplot.yaxis.CenterTitle()
#        ratioplot.xaxis.SetTitle(xlabel)
                
        ROOT.gPad.RedrawAxis()
        
        histpad.cd()

        plotlabels.drawPlotInformation(state)
#        plotlabels.drawTopLeftInformation(breakdowns,state) # turn on 
#        legendtools.drawDataLegend(breakdowns,state) # turn on
        legendtools.drawBackgroundLegend(breakdowns,state)
        
#        os.system("mkdir -p " + outputfolder + "/3L_ISR/")
#        os.system("mkdir -p " + outputfolder + "/3L_ISR/")
#        outputtools.outputRegionDiagnostics(breakdowns,state) # turn on 

        filenamevariable = variable.replace("/","_")
        canvas.Print(outputfolder + "NeighAssign_euc12_" + filenamevariable + region + ".png") 
#        canvas.Print(outputfolder + "/Data" + year + "/" + region + "/"+ filenamevariable+ "_" + region + ".pdf")
        outputyields = False       # only see output yields for first variable 

if __name__ == "__main__":
    main() 

