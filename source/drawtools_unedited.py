from rootpy.plotting.shapes import Line,Arrow
from rootpy.plotting import F1, Hist, HistStack, Canvas, Legend, Pad
import rootpyglobals
#from regiondefinitions import retreiveRegionInformation
from collections import OrderedDict
from rootpy import ROOT
from ROOT import TLatex
import math
from ROOT import TColor
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from ROOT  import RooStats


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






