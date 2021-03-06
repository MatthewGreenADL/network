from collections import OrderedDict

def getVariables(region):
    """
    Input region 
    Output variable information dictionary according to your choice 
    """

    
    defaultvariables = OrderedDict([
#        ('nsi_betweenness',{'latex':"betweenness^{*,euc}, l=12.0.",'units':'','nbins':21,'xmin':0.,'xmax':50000}), # 0.015
#        ('nsi_average_neighbors_degree',{'latex':"k_{nn,\nu}^{*,city}, l=20.0",'units':'','nbins':20,'xmin':0.5,'xmax':0.73}),
#        ('nsi_',{'latex':"k_{\nu}^{*,city}, l=100.0",'units':'','nbins':25,'xmin':0,'xmax':0.8}),
#        ('nsi_local_clustering',{'latex':"C_{\nu}^{*,city}, l=20.0"  ,'units':'','nbins':20,'xmin':0.6,'xmax':0.97}),
#        ('nsi_local_soffer_clustering',{'latex':"C_{\nu}^{*,euc}, l=70.0"  ,'units':'','nbins':25,'xmin':0.3,'xmax':1.1}),
#        ('nsi_max_neighbors_degree',{'latex':"k_{nnmax,\nu}^{*,city}, l=20.0",'units':'','nbins':22,'xmin':0.79,'xmax':0.865}),
        ('nsi_degree',{'latex':"k_{\nu}^{*,euc}, l=12.0"  ,'units':'','nbins':10,'xmin':0,'xmax':1.0}),

#      ('lept1Pt'                        ,{'latex':"p_{T}^{l1}"  ,'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
#      ('jet1Pt'                        ,{'latex':"p_{T}^{j1}"  ,'units':'GeV','nbins':25,'xmin':0,'xmax':500}),
#      ('lept2Pt'                        ,{'latex':"p_{T}^{l2}"  ,'units':'GeV','nbins':20,'xmin':0,'xmax':400}),
#      ('lept3Pt'                        ,{'latex':"p_{T}^{l3}"  ,'units':'GeV','nbins':15,'xmin':0,'xmax':350}),
      #    ('lept1Phi'                       ,{'latex':"\phi^{l1}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
      #    ('lept2Phi'                       ,{'latex':"\phi^{l2}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
      #    ('lept3Phi'                       ,{'latex':"\phi^{l3}"  ,'units':'rad','nbins':15,'xmin':-3.2,'xmax':3.2}),
      #      ('NjS'                        ,{'latex':"n^{S}_{J}"           ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),
      #      ('NjISR'                        ,{'latex':"n^{ISR}_{J}"           ,'units':'1'   ,'nbins':6,'xmin':0,'xmax':6}),
#      ('mll'                          ,{'latex':"m_{ll}"        ,'units':'GeV','nbins':40,'xmin':0,'xmax':400}),
#      ('ptll'                          ,{'latex':"p_{T}^{ll}"        ,'units':'GeV','nbins':40,'xmin':0,'xmax':400}),
#      ('mTW'                       ,{'latex':"m_{T}^{W}"        ,'units':'GeV','nbins':25,'xmin':0,'xmax':250}),
#      ('met'     ,{'latex':"E_{T}^{miss}"  ,'units':'GeV','nbins':10,'xmin':0,'xmax':250}),
#      ('min_mt',{'latex':"m_{T}^{min}"  ,'units':'GeV','nbins':25,'xmin':0,'xmax':200}),
#        ('braycurtis_nsi_average_neighbors_degree',{'latex':"avg neigh deg"  ,'units':'','nbins':25,'xmin':0,'xmax':0.6})
#        ('nsi_degree',{'latex':"euc degree, l=100"  ,'units':'','nbins':25,'xmin':0,'xmax':1}),
#        ('nsi_average_neighbors_degree',{'latex':"cheb avg neighbors degree, l=60"  ,'units':'','nbins':25,'xmin':0,'xmax':1}),
#        ('nsi_exponential_closeness',{'latex':"CC_{EC,\nu}^{*,euc}, l=12.",'units':'','nbins':20,'xmin':0,'xmax':0.6}),
#        ('nsi_exponential_clustering',{'latex':"C_{EC,\nu}^{*,euc}, l=12.",'units':'','nbins':20,'xmin':0,'xmax':0.6}),
#        ('nsi_harmonic_closeness',{'latex':"CC_{HC,\nu}^{*,city}, l=100.0",'units':'','nbins':25,'xmin':0,'xmax':0.8}),
#        ('nsi_harmonic_closeness',{'latex':"CC_{HC,\nu}^{*,euc}, l=12.",'units':'','nbins':20,'xmin':0,'xmax':1.01}),
#        ('nsi_degree',{'latex':"k_{\nu}^{*,corr}, l=0.03",'units':'','nbins':25,'xmin':0,'xmax':0.95}),
#        ('nsi_degree',{'latex':"k_{\nu}^{*,euc}, l=12.",'units':'','nbins':20,'xmin':0,'xmax':0.95}), # 0.015
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
    
