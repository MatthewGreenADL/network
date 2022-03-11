from rootpy.tree import Cut
#from normalisationfactors import normalisationfactors
#from normalisationfactors import retreiveNormalisationFactors

def retreiveSelection(RegionDictionary,sampleDictionarySubset,LuminosityDictionary,WeightDictionary,state):
    variable     = state['variable']
    Type         = sampleDictionarySubset['type']
    Year         = sampleDictionarySubset['year']
    LegendEntry  = sampleDictionarySubset['legend']
    Luminosity   = LuminosityDictionary[Type][Year]
    Weight       = WeightDictionary[Type]
    donminus1    = state['donminus1']
    Cutlist = RegionDictionary['cutlist']
    total = Cut("1")

    return Cut(Luminosity) * Cut(Weight) * total 




def retreiveRegionInformation(Region,sampleType="MC"):
    cutnames = [] 
    RegionLabel = ""
    cutlist = ""
    RegionType = ""


    if Region == "PRE3L":
        cutlist = [Cut("1"),Cut("is3Lep && lept1Pt>25 && lept2Pt>25 && lept3Pt>20 && mll>75 && mll<105 && mTW>50")]
        cutnames = ["Total","3L-Preselection"]
        RegionLabel = ""
    
    if (RegionLabel == ""):
         RegionLabel = Region

    if cutlist == "":
        print "no cutlist applied"

    if RegionType == "":
        RegionType = 'generic'

    
    RegionDictionary = {}
    RegionDictionary['region']      = Region
    RegionDictionary['regionlabel'] = RegionLabel
    RegionDictionary['cutlist']     = cutlist
    RegionDictionary['cutnames']    = cutnames
    RegionDictionary['regiontype']  = RegionType



    return RegionDictionary
