from rootpy.plotting import Canvas,Pad

def getCanvasParameters(state):
    """
    Input: state dictionary - needs to know if you want to plot the ratio plot underneath
    Output: all the parameters which give us a nice framed canvas
    """
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

def createCanvas(state):
    """
    Input: state - do we want a ratioplot?
    Output: a canvas with plotheight and plotwidth
    """

    doRatio = state['doRatio']
    canvasParameters = getCanvasParameters(state)
    plotwidth        = canvasParameters['canvaswidth'][doRatio]
    plotheight       = canvasParameters['canvasheight'][doRatio]

    canvas = Canvas(width = plotwidth,height = plotheight )

    return canvas

def createHistogramPad(state):
    """
    Input: state - needs to know if we want to plot a ratio plot underneath
    Output: the main histogram pad - where the stacks go.
    """

    doRatio = state['ratiooverwrite']
    canvasParameters = getCanvasParameters(state)
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


def createRatioPad(state):
    """
    Input: state - needs to know if we want to plot a ratio plot underneath
    Output: the ratio pad - where the Data/MC goes.
    """

    doRatio = state['doRatio']
    canvasParameters = getCanvasParameters(state)
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
