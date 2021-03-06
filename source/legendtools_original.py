from rootpy.plotting import Legend
import rootpyglobals
from ROOT import TColor
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange

def drawDataLegend(breakdowns,state):
        

        defaultlabelsize = rootpyglobals.defaultlabelsize

        datalegend_entries=2 #figure out how to remove this magic number                                                                                                                                                       
        datamargin      = 0.10
        datarightmargin = 0.00
        datatopmargin   = 0.05
        dataentryheight = 0.045
        dataentrysep    = 0.06
        datalegend = Legend(datalegend_entries, leftmargin  = 0.26,
                                      topmargin   = datatopmargin           ,
                                      rightmargin = datarightmargin         ,
                                      entryheight = dataentryheight       ,
                                      entrysep    = dataentrysep            ,
                                      margin      = datamargin              ,
                                      textfont    = 43                  ,
                                      textsize    = defaultlabelsize,
                                      header      = None)
        datalegend.SetLineColor(0)


        BLINDED = state['BLINDED']
        plotData = state['plotData']

	
        backgroundbreakdown = breakdowns['background']
        backgroundhistogram = backgroundbreakdown['total']['histogram']
        backgroundyield     = backgroundbreakdown['total']['yield']
        backgrounderror     = backgroundbreakdown['total']['error']

        if plotData and (not BLINDED): 
            databreakdown       = breakdowns['data']
            datahistogram       = databreakdown['Data']['histogram']
            datayield           = databreakdown['Data']['yield']
            dataerror           = databreakdown['Data']['error']

            datahistogram.SetMarkerStyle('circle')
            datahistogram.SetMarkerSize(2) 
            datahistogram.SetLineWidth(3)
            datalegend.AddEntry(datahistogram,label = "Data [" + str(round(datayield,0)) +"]",style ="E1P")
        #errorband = inputstack.sum.Clone()
        backgroundhistogram.SetLineColor(1)
        backgroundhistogram.SetLineWidth(2)
        backgroundhistogram.SetFillStyle(3344)
        backgroundhistogram.SetFillColor(922)
#	if Region.startswith("SR"):
	datalegend.AddEntry(backgroundhistogram, label = "SM   [" + str(round(float(backgroundyield),1)) + "]" ,style = "LF")
	#else:
        #    datalegend.AddEntry(backgroundhistogram, label = "SM [" + str(round(float(backgroundyield),1)) + "]",style = "LF")

        datalegend.Draw("SAME")



def drawBackgroundLegend(breakdowns,state):
    backgroundbreakdown = breakdowns['background']
    signalbreakdown     = breakdowns['signal']

    if "3L" in state['Region']:
        legend_entries= 4
    else:
        legend_entries= 6

    margin      = 0.30
    rightmargin = 0.07
    topmargin   = 0.05
    entryheight = 0.045
    entrysep    = 0.06
    defaultlabelsize = rootpyglobals.defaultlabelsize
    LegendExtraInformation = state['LegendExtraInformation']

    legend = Legend(legend_entries, leftmargin  = 0.49,
                                      topmargin   = topmargin           ,
                                      rightmargin = rightmargin         ,
                                      entryheight = entryheight       ,
                                      entrysep    = entrysep            ,
                                      margin      = margin              ,
                                      textfont    = 43                  ,
                                      textsize    = defaultlabelsize,
                                      header      = None                )

#    legend.SetLineColor()

    totalyield,totalerror = backgroundbreakdown['total']['yield'], backgroundbreakdown['total']['error']

    for background in backgroundbreakdown:
        if background == "total":continue
	
        histogram      = backgroundbreakdown[background]['histogram']
        backgroundyield = backgroundbreakdown[background]['yield']
        backgrounderror = backgroundbreakdown[background]['error']
        information = ""
	if (backgroundyield < 0.0):
            colorwrapper = "#color[16]{"
	else:
            colorwrapper = "#color[1]{"
        if LegendExtraInformation == "Relative" and totalyield != 0:
            information += " [" + colorwrapper + str(round(100*backgroundyield/totalyield,1)) +"}%]"
        elif LegendExtraInformation == "Absolute":
            information += " [" + colorwrapper + str(round(backgroundyield,1)) + "}]"

        legend.AddEntry(histogram,label = background + information ,style="F")

    for signal in signalbreakdown:
        histogram   = signalbreakdown[signal]['histogram']
        signalyield = signalbreakdown[signal]['yield']
        signalerror = signalbreakdown[signal]['error']
#	signallatex = "\tilde{\chi}^{0}_{2}/\tilde{\chi}^{\pm}_{1},\tilde{\chi}^{0}_{1}=(200,100)\mathrm{GeV}"
	signallatex = signal
#	print signal 
        legend.AddEntry(signalbreakdown[signal]['histogram'],
                        label =signallatex + " (" + str(round(signalyield,1)) +")",
                        style="L")



    # for LegendGroup in backgroundstacks:
    #     if LegendGroup is 'Data': continue
    #     if LegendGroup is 'Signal': continue 
    #     backgroundyield,backgrounderror = backgroundstacks[LegendGroup].sum.integral(error=True,overflow=True)
    #     if LegendExtraInformation == "Relative" and totalyield!=0:
    #         relativeyield = str(round(100*backgroundyield/totalyield,1))
    #         legend.AddEntry(backgroundstacks[LegendGroup].sum,label=LegendGroup + " [" + relativeyield + "%]",style="F" )
    #     elif LegendExtraInformation == "Absolute":
    #         legend.AddEntry(backgroundstacks[LegendGroup].sum,label =LegendGroup + " (" + str(round(backgroundyield,1)) +")",style="F")
    #     else:
    #         legend.AddEntry(backgroundstacks[LegendGroup].sum,label =LegendGroup ,style="F")

#    for LegendGroup in backgroundstacks:
#        if LegendGroup is 'Signal':
#            backgroundyield,backgrounderror = backgroundstacks[LegendGroup].sum.integral(error=True,overflow=True)
#            legend.AddEntry(backgroundstacks[LegendGroup].sum,label =LegendGroup + " (" + str(round(backgroundyield,1)) +")",style="L")

    legend.Draw("SAME");
