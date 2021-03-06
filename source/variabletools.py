from collections import OrderedDict

def getVariables(region):
    """
    Input region 
    Output variable information dictionary according to your choice 
    """

    
    defaultvariables = OrderedDict([
      ('lept1Pt'                        ,{'latex':"p_{T}^{l1}"  ,'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
      ('lept2Pt'                        ,{'latex':"p_{T}^{l2}"  ,'units':'GeV','nbins':20,'xmin':0,'xmax':400}),
      ('lept3Pt'                        ,{'latex':"p_{T}^{l3}"  ,'units':'GeV','nbins':15,'xmin':0,'xmax':350}),
      ('lept1Phi'                       ,{'latex':"\phi^{l1}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
      ('lept2Phi'                       ,{'latex':"\phi^{l2}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
      ('lept3Phi'                       ,{'latex':"\phi^{l3}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
#      ('NjS'                        ,{'latex':"n^{S}_{J}"           ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),
#      ('NjISR'                        ,{'latex':"n^{ISR}_{J}"           ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),
      ('mll'                          ,{'latex':"m_{ll}"        ,'units':'GeV','nbins':40,'xmin':75,'xmax':110}),
      ('ptll'                          ,{'latex':"p_{T}^{ll}"        ,'units':'GeV','nbins':40,'xmin':0,'xmax':400}),
      ('mTW'                       ,{'latex':"m_{T}^{W}"        ,'units':'GeV','nbins':25,'xmin':0,'xmax':250}),
      ('met'     ,{'latex':"E_{T}^{miss}"  ,'units':'GeV','nbins':10,'xmin':50,'xmax':350}),
      ('min_mt',{'latex':"m_{T}^{min}"  ,'units':'GeV','nbins':25,'xmin':0,'xmax':110}),
      ('eventWeight',{'latex':"Event weight"  ,'units':'','nbins':25,'xmin':-0.3,'xmax':3}),
    ])
    
    jetvariables = OrderedDict([
      ('nJets'                        ,{'latex':"n^{20}_{J}"           ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),
      ('nBtagJets',{'latex':"n^{20,77}_{b}"        ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),  
      ('jet1Pt'                        ,{'latex':"p_{T}^{jet,lead}"   ,'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
      ('jet2Pt'                        ,{'latex':"p_{T}^{jet,sublead}",'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
      #      ('jet1Phi'                        ,{'latex':"\phi^{jet,lead}"   ,'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
    ])

    variables = OrderedDict()
    
    if ("my_custom_region" in region):
        variables.update(defaultvariables)
    else:
        variables.update(defaultvariables)
    return variables
    
