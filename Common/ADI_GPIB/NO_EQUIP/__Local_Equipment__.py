dict_equip = {'GPIB0::5' : 'GW.Inc,PST-3202,J161973 ,FW1.00',
              'GPIB0::9' : 'Agilent Technologies,L4445A,MY46100392,2.43-2.43-0.00-0.00',
              'GPIB0::15': 'TEKTRONIX,PS2521G, ,SCPI:94.0 FW:.15',
              'GPIB0::22': 'HEWLETT-PACKARD,34401A,0,11-5-2',
              'GPIB0::28': 'Rohde&Schwarz,SMA100A,1400.0000k02/101053,2.2.2.3-02.05.04  (Release)',
              'GPIB0::29': 'Rohde&Schwarz,SMA100A,1400.0000k02/101748,2.2.2.3-2.05.68.18 (Release)',
             }

dict_properties = { 'SMA'          : [ ('PHASE'    , 'DEG', 0     , None),
                                       ('FREQ'     , 'MHz', 10.3e6 , None),
                                       ('POW'      , 'dBm', 8      , None),
                                       ('OUTP:STAT', ''   , 'ON'   , None),
                                       ('PM:STAT'  , ''   , 'OFF'  , None),
                                       ('POW:ALC'  , ''   , 'AUTO' , None),
                                       ('OUTP:AMOD', ''   , 'AUTO' , None),
                                       ('SYS:KLOC' , ''   , 'OFF'  , None) ],
    
                    'PS2521G'      : [ ('INST|INST:NSEL', 'P6V|P25V|N25V|1|2|3' , '1'  , '__current__' ),
                                       ('VOLT|MEAS:VOLT', ''                    , 1.8  , 'VOLT'        ),
                                       ('CURR|MEAS:CURR', ''                    , 0.5  , 'CURR'        ),
                                       ('OUTP'          , ''                    , 'ON' , None          ) ] ,
                                       
                    'InstekPST3202': [ (':CHAN1:VOLT|:CHAN1:MEAS:VOLT', ''      , 1.8  , 'VOLT1'       ),
                                       (':CHAN2:VOLT|:CHAN2:MEAS:VOLT', ''      , 1.8  , 'VOLT2'       ),
                                       (':CHAN3:VOLT|:CHAN3:MEAS:VOLT', ''      , 1.8  , 'VOLT3'       ),
                                       (':CHAN1:CURR|:CHAN1:MEAS:CURR', ''      , 0.1  , 'CURR1'       ),
                                       (':CHAN2:CURR|:CHAN2:MEAS:CURR', ''      , 0.1  , 'CURR2'       ), 
                                       (':CHAN3:CURR|:CHAN3:MEAS:CURR', ''      , 0.1  , 'CURR3'       ),
                                       ('OUTP:STAT'                   , ''      ,   1  , None          ) ],
                                       
                    'HP34401A'     : [ ('MEAS:VOLT:DC'                , ''      , 1.79 , None          ),
                                       ('MEAS:CURR:DC'                , ''      , 0.21 , None          ),                                       
                                       ('MEAS:CONT'                   , ''      , True , None          ) ] ,
                    
##                    'AgilentL7206A': [ ('MEAS:VOLT:DC'                , ''      , 1.79 , None          ),
##                                       ('MEAS:CURR:DC'                , ''      , 0.21 , None          ),                                       
##                                       ('MEAS:CONT'                   , ''      , True , None          ) ] ,
                    
                  }


def GetEquipmentProperties ( model ):
    if ( dict_properties.has_key( model ) ):
        return dict_properties[model]
    return None