from rootpy.plotting import Canvas
from rootpy.plotting import Pad
def retreiveCanvasParameters(state):
    doRatio = state['doRatio']
    #doRatio  = 1
    canvaswidth = 750
    canvasheight= 800
    canvasParameters = {}
    canvasParameters['canvaswidth']  = [750,750]
    canvasParameters['canvasheight'] = [canvasheight,int((1-0.2*(1-doRatio))*canvasheight)]
    canvasParameters['leftmargin']   = [0.0, 0.0 ]
    canvasParameters['rightmargin']  = [0.0, 0.0 ]
    canvasParameters['topmargin']    = [1.0, 1.0 ] 
    canvasParameters['bottommargin'] = [0.0, 0.4 ]
    return canvasParameters

def createCanvas(canvasParameters,state):
    """
    Create Canvas for the plot.
    """
    doRatio = state['doRatio']
    canvasParameters = retreiveCanvasParameters(state)
    plotwidth        = canvasParameters['canvaswidth'][doRatio]
    plotheight       = canvasParameters['canvasheight'][doRatio]
    canvas = Canvas(width = plotwidth,height = plotheight )

    return canvas


def createHistogramPad(canvasParameters,state):
    """
    Create Histogram Pad. 
    """
    doRatio = state['ratiooverwrite']
    top    = canvasParameters['topmargin'][doRatio]
    bottom = canvasParameters['bottommargin'][doRatio]
    left   = canvasParameters['leftmargin'][doRatio]
    right  = 1 - canvasParameters['rightmargin'][doRatio]

    histpad = Pad(left,bottom,right, top,color="white",bordersize =1)
    if not doRatio:
        histpad.SetBottomMargin(0.15)

    histpad.SetFrameBorderMode(0)

    histpad.SetLogy()
    #histpad.cd()
    histpad.SetFrameBorderSize(2)
    histpad.SetFrameLineWidth(1);


    histpad.Draw()

    return histpad


def createRatioPad(canvasParameters,state):
    """
    Create Ratio Pad, if required.
    """
    doRatio = state['doRatio']
    top    = canvasParameters['bottommargin'][1] - 0.02 
    #plotParameters['topmargin'][doRatio]
    bottom = 0.0
    #plotParameters['bottommargin'][doRatio]
    left   = canvasParameters['leftmargin'][1]
    right  = 1 - canvasParameters['rightmargin'][1]

    ratiopad    = Pad(left,bottom ,right,top,bordersize = 1)
    ratiopad.SetBottomMargin(0.33)
    ratiopad.SetTopMargin(0.03)
    ratiopad.SetFrameLineWidth(1);

    
    ratiopad.Draw()
    

    return ratiopad
