def defineState(args):
    import regiontools
    from collections import OrderedDict
    Region = args.region
    
    RegionDictionary   = regiontools.retreiveRegionInformation(Region)
    state              = OrderedDict()
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
    state['BLINDED']     = BLINDED
    state['plotData']    = plotData
    state['doRatio']     = args.ratioplot
#    state['systematics'] = args.systematics
    state['LegendExtraInformation'] = "Absolute" #Relative
    state['colorscheme'] = "RJ"
    state['ratiooverwrite'] = 1;

    if RegionType == "ABCD": args.applynf = False

    if "CR" in RegionType:args.applynf = False

    return state


