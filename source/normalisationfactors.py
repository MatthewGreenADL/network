

def retreiveNormalisationFactors(nf,sampleDictionarySubset,state):

    Region      = state['Region']
    RegionType  = state['regiontype']
    LegendEntry = sampleDictionarySubset['legend']
    Year        = sampleDictionarySubset['year']
    applynf     = state['applynf']
    metwp       = state['metwp']
    nminus1 = state['donminus1']
    isowp   = state['isowp']

    #print nf
    if "2L_ISR" in Region: 
        controlregion = "2L_ISR"
    elif "2L"   in Region: 
        controlregion = "2L"
    elif "3L_ISR" in Region:
        controlregion = "3L_ISR"
    elif "3L" in Region:
        controlregion = "3L"

    nf = {}
    # 3L nfs

            

    nf['3L']     = {'Diboson'   :{'1516':{'yield':1.085,'error':0.107},'17':{'yield':0.996,'error':0.085},'18':{'yield':0.945,'error':0.072}}}
    nf['3L_ISR'] = {'Diboson'   :{'1516':{'yield':0.999,'error':0.097},'17':{'yield':0.912,'error':0.098},'18':{'yield':0.956,'error':0.084}}}

        # 2L nfs
    
    nf['2L'] = {'t#bar{t}' : {'1516':{'yield':1.00,'error':0.135},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}},                     'Single top': {'1516':{'yield':1.00,'error':0.135},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}},
                'Diboson'   : {'1516':{'yield':1.00,'error':0.118},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}}
            }
    if Region.startswith("SR2L_LOW"):# and not nminus1:
        nf['2L'].update({'Z+jets'   : {'1516':{'yield':5.09/15.4,'error':0.118},'17':{'yield':0.741,'error':0.087},'18':{'yield':1.0002,'error':0.087}}})
            
    nf['2L_ISR'] = {'t#bar{t}' : {'1516':{'yield':1.00,'error':0.082},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}},
                    'Single top': {'1516':{'yield':1.00,'error':0.082},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}},
                    'Diboson'   : {'1516':{'yield':1.00,'error':0.827},'17':{'yield':1.00,'error':0.087},'18':{'yield':1.00,'error':0.087}}
                }
    if Region.startswith("SR2L_ISR"):# and not nminus1:
        nf['2L_ISR'].update({'Z+jets'   : {'1516':{'yield':0.9/4.8,'error':0.118},'17':{'yield':0.741,'error':0.087},'18':{'yield':1.0002,'error':0.087}}})
                
 

#    print nf

    #print "Region" + Region 
    #print controlregion 
    try:
    #    print "INFO::Background: " + LegendEntry
            
        nf_scale = nf[controlregion][LegendEntry][Year]['yield']
        nf_error = nf[controlregion][LegendEntry][Year]['error']     
    except:
     #   print "exception raised"
        nf_scale = 1.0
        nf_error = 0.0

    if "CR" in Region:
      #  print "INFO::Control Region"
        nf_scale = 1.0  
        nf_error = 0.0

#    if RegionType is "ABCD":
#        print "INFO::ABCD REGION"
#        nf_scale = 1.0
#        nf_error = 0.0



    if "RJ" in Region:
        #print "INFO::RJ IN NAME"
        nf_scale = 1.0
        nf_error = 0.0

    if applynf == False:
        print "INFO::APPLY NF FALSE"
        nf_scale = 1.0
        nf_error = 0.0

    
    
    #print "END"
    
    #print "INFO::" + LegendEntry + " NF:" + str(nf_scale) + "\pm" + str(nf_error)
    return nf_scale,nf_error








def normalisationfactors(state):
    """
    normalisation factors stored in here.
    """
    from collections import OrderedDict
    nf = OrderedDict()
    metwp  = state['metwp']
    Region = state['Region']
    Year   = state['year']
    

    regionList = ["CR2L-VV","CR2L-TOP","CR2L_ISR-VV","CR2L_ISR-TOP","CR3L-VV","CR3L_ISR-VV"]

    tempDict = {}
    tempDict = {'1516':{},'17':{},'18':{}}
    try:
#        print 'INFO::DiagnosticFile:diag_' + Region + '_' + Year + "_" +metwp + '.txt'
        for controlregion in regionList:
            try:
                with open('diag_' + controlregion + "_" + Year +"_" + metwp + '.txt') as f:
                    for line in f:
                        (key,value,error) = line.split("\t")
                        tempDict[Year][key] = {'yield':value,'error':error.strip('\n')}

                    """         for name in tempDict:
                                if 'NF' in name:
                                    nfDict[name] = {'yield':value,'error':error.strip('\n')}
                    """
            except:
                pass
#                print "INFO::DiagnosticFile:Not created yet"

        if metwp == "Loose":
                            
            nf['2L']     = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   :{'1516':tempDict[Year]['CR2L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['2L_ISR'] = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   : {'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}

            nf['3L']     = {'Diboson'   :{'1516':tempDict[Year]['CR3L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
        elif metwp == "Tight":
            nf['2L']     = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   :{'1516':tempDict[Year]['CR2L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['2L_ISR'] = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   : {'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}

            nf['3L']     = {'Diboson'   :{'1516':tempDict[Year]['CR3L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
        elif metwp == "Tighter":
            nf['2L']     = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   :{'1516':tempDict[Year]['CR2L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['2L_ISR'] = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   : {'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}

            nf['3L']     = {'Diboson'   :{'1516':tempDict[Year]['CR3L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
        elif metwp == "Tenacious":
            nf['2L']     = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L-TOP NF'],'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   :{'1516':tempDict[Year]['CR2L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['2L_ISR'] = {'t#bar{t}' : {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Single top': {'1516':tempDict[Year]['CR2L_ISR-TOP NF']  ,'17':tempDict[Year]['CR2L-TOP NF']},
                            'Diboson'   : {'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}

            nf['3L']     = {'Diboson'   :{'1516':tempDict[Year]['CR3L-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':tempDict[Year]['CR2L_ISR-VV NF'],'17':tempDict[Year]['CR2L-TOP NF']}}

        #print nf
    except:
# OrderedDict([('2L', {'Diboson': 
#                     {'1516': {'yield': '1.01279262902', 'error': '0.127822910279'}, '17': 1.0},
#                      'Single top': {'1516': {'yield': '1.02424809325', 'error': '0.164747003894'}, '17': 1.0},
#                       't#tbar{t}': {'1516': {'yield': '1.02424809325', 'error': '0.164747003894'}, '17': 1.0}}),
#              ('2L_ISR', {'Diboson': {'1516': {'yield': '0.800586519334', 'error': '0.168810976833'}, '17': 1.0},
#                          'Single top': {'1516': {'yield': '0.91332804476', 'error': '0.0904384939606'}, '17': 1.0},
#                          't#tbar{t}': {'1516': {'yield': '0.91332804476', 'error': '0.0904384939606'}, '17': 1.0}}),
#              ('3L', {'Diboson': {'1516': {'yield': '0.908531621212', 'error': '0.114279068735'}, '17': 1.0}}),
#              ('3L_ISR', {'Diboson': {'1516': {'yield': '0.800586519334', 'error': '0.168810976833'}, '17': 1.0}})])



        if metwp == "Loose":
            nf['2L']     = {'t#tbar{t}' : {'1516':1.024,'17':1.0},
                            'Single top': {'1516':1.024,'17':1.0},
                            'Diboson'   :{'1516':1.013,'17':1.0}}
            nf['2L_ISR'] = {'t#tbar{t}' : {'1516':0.913  ,'17':1.0},
                            'Single top': {'1516':0.913  ,'17':1.0},
                            'Diboson'   : {'1516':0.801,'17':1.0}}

            nf['3L']     = {'Diboson'   :{'1516':1.135,'17':1.0}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':1.008,'17':1.0}}
        elif metwp == "Tight":
            nf['2L']     = {'t#tbar{t}' : {'1516':0.991,'17':1.0},
                            'Single top': {'1516':0.991,'17':1.0},
                            'Diboson'   :{'1516':0.989,'17':1.0}}
            nf['2L_ISR'] = {'t#tbar{t}' : {'1516':0.864  ,'17':1.0},
                            'Single top': {'1516':0.864  ,'17':1.0},
                            'Diboson'   : {'1516':0.856,'17':1.0}}

            nf['3L']     = {'Diboson'   :{'1516':1.1,'17':1.0}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':0.946,'17':1.0}}
        elif metwp == "Tighter":
            nf['2L']     = {'t#tbar{t}' : {'1516':1.084,'17':1.0},
                            'Single top': {'1516':1.084,'17':1.0},
                            'Diboson'   :{'1516':1.015,'17':1.0}}
            nf['2L_ISR'] = {'t#tbar{t}' : {'1516':0.887  ,'17':1.0},
                            'Single top': {'1516':0.887  ,'17':1.0},
                            'Diboson'   : {'1516':0.851,'17':1.0}}

            nf['3L']     = {'Diboson'   :{'1516':1.1,'17':1.0}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':0.946,'17':1.0}}
        elif metwp == "Tenacious":
            nf['2L']     = {'t#tbar{t}' : {'1516':1.058,'17':1.0},
                            'Single top': {'1516':1.058,'17':1.0},
                            'Diboson'   :{'1516':0.988,'17':1.0}}
            nf['2L_ISR'] = {'t#tbar{t}' : {'1516':0.864  ,'17':1.0},
                            'Single top': {'1516':0.864  ,'17':1.0},
                            'Diboson'   : {'1516':0.916,'17':1.0}}

            nf['3L']     = {'Diboson'   :{'1516':1.1,'17':1.0}}
            nf['3L_ISR'] = {'Diboson'   :{'1516':0.946,'17':1.0}}
    return nf




#        elif metwp == "Tighter":
#            nf['2L']     = {'t#bar{t}' : {'1516':{'yield':1.411,'error':0.137},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':1.411,'error':0.137},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.909,'error':0.119},'17':1.0,'18':1.0}
#
#                       }
#            nf['2L_ISR'] = {'t#bar{t}' : {'1516':{'yield':0.975,'error':0.083},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':0.975,'error':0.083},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.798,'error':0.17},'17':1.0,'18':1.0}
#                            }
#        elif metwp == "Tenacious":
#            nf['2L']     = {'t#bar{t}' : {'1516':{'yield':1.215,'error':0.135},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':1.215,'error':0.135},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.869,'error':0.119},'17':1.0,'18':1.0}
#                            }
#            nf['2L_ISR'] = {'t#bar{t}' : {'1516':{'yield':0.984,'error':0.086},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':0.984,'error':0.086},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.856,'error':0.182},'17':1.0,'18':1.0}
#                            }

#        elif metwp == "Tighter":
#            nf['2L']     = {'t#bar{t}' : {'1516':{'yield':1.411,'error':0.137},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':1.411,'error':0.137},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.909,'error':0.119},'17':1.0,'18':1.0}#
#
#                       }
#            nf['2L_ISR'] = {'t#bar{t}' : {'1516':{'yield':0.975,'error':0.083},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':0.975,'error':0.083},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.798,'error':0.17},'17':1.0,'18':1.0}
#                            }
#        elif metwp == "Tenacious":
#            nf['2L']     = {'t#bar{t}' : {'1516':{'yield':1.215,'error':0.135},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':1.215,'error':0.135},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.869,'error':0.119},'17':1.0,'18':1.0}
#                            }
#            nf['2L_ISR'] = {'t#bar{t}' : {'1516':{'yield':0.984,'error':0.086},'17':1.0,'18':1.0},
#                            'Single top': {'1516':{'yield':0.984,'error':0.086},'17':1.0,'18':1.0},
#                            'Diboson'   : {'1516':{'yield':0.856,'error':0.182},'17':1.0,'18':1.0}
#                            }


#        elif metwp == "Tighter":
#            nf['3L']     = {'Diboson'   :{'1516':{'yield':0.986,'error':0.107},'17':{'yield':1.238,'error':0.088},'18':{'yield':1.166,'error':0.075}}#}
#            nf['3L_ISR'] = {'Diboson'   :{'1516':{'yield':0.93,'error':0.096},'17':{'yield': 0.976,'error':0.087},'18':{'yield':1.061,'error':0.078}}#}
#        elif metwp == "Tenacious":
#            nf['3L']     = {'Diboson'   :{'1516':{'yield':1.002,'error':0.107},'17':{'yield':1.231,'error':0.087},'18':{'yield':1.167,'error':0.078}}#}
#            nf['3L_ISR'] = {'Diboson'   :{'1516':{'yield':0.948,'error':0.097},'17':{'yield':1.011,'error':0.088},'18':{'yield':1.087,'error':0.079}}}\
