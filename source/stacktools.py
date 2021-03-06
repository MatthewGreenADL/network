from collections import OrderedDict
from rootpy.plotting import  Hist, HistStack, Canvas
import math 

def getTreeNames(sample,samples,rootfiles):
    """
    Inputs: sample  - specific sample to retreive tree of
            samples - dictionary of all samples
            rootfiles - rootfiles of all samples
    Output: a root tree
    """

    filename = samples[sample]['filename']
    rootfile  = rootfiles[sample]
    if("data15" in filename):
        tree = rootfile.Get("data1516")
    elif("data17" in filename):
        tree = rootfile.data17
    elif("data18" in filename):
        tree = rootfile.data18
    elif("fakes" in filename):
        tree = rootfile.MM_CENTRAL
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
    else:
        tree = rootfile.network_tree
    return tree

# tree not assigned for excluded filename 



def createSampleStack(samples):
    """
    input: samples dictionary - contains all sample information
    output: a ROOT stack for data, signal, background and fakes
    """

    stack     = OrderedDict()
    for Type in ['data','bkg','fakes', 'sig']:
        stack[Type] = OrderedDict()

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
