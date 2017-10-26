import inspect, re, os
import __Local_Equipment__
reload (__Local_Equipment__)

ENV_ADI_GPIB_DEBUG = os.getenv('ADI_GPIB_DEBUG')

if (ENV_ADI_GPIB_DEBUG is None):
    __flag_to_be_run_in_local_mode__ = False
else:
    try:
        __flag_to_be_run_in_local_mode__ = bool(ENV_ADI_GPIB_DEBUG)
    except:
        __flag_to_be_run_in_local_mode__ = False

if ( __flag_to_be_run_in_local_mode__ == True ):
    print "--------------------------------------"
    print "*** RUNNING ADI_GPIB in DEBUG mode ***"
    print "--------------------------------------"

    class visa (object):
        dict_equip = __Local_Equipment__.dict_equip

        def get_instruments_list (self, flag):
            return self.dict_equip.keys()

        class GpibInstrument (object):
            __current__ = 1

            def __init__ (self, rname):
                self.key = None
                for key, value in visa.dict_equip.items() :
                    key2 = "%s::0%s" % tuple( key.split("::") )
                    if ( rname in [ key, key2 ] ):
                        self.key   = key
                        self.model = inspect.stack()[2][1].split( '\\' )[-1].replace( '.py','')
                        #self.__handle_equipment__ ( 'SET_DEFAULTS' )
                        return

                raise ValueError ( 'Cannot instantiate GPIB onject at %s', rname )

            def ask (self, string):
                if ( string == '*IDN?' ):
                    return visa.dict_equip[self.key]
                elif (string == "*RST" ):
                    raise Exception ( "We don't handle it as of now" )
                ret = self.__handle_equipment__ (string)
                return ret

            def write (self, string):
                return self.__handle_equipment__ (string)

            def __handle_equipment__ (self, command):
                item = __Local_Equipment__.dict_equip[ self.key ]
                #print item
                #if ( 'SMA' in item ):
                #    properties = __Local_Equipment__.__sma_properties__ ()
                #el
                properties = __Local_Equipment__.GetEquipmentProperties( self.model )
                if ( properties is None ):
                    print "**** Unhandled command %s for %s ****" % (command, self.model)
                    return False

                for (attrib, unit, default, var) in properties :
                    #print
                    #print attrib, unit, default, var
                    #if ( command == 'SET_DEFAULTS' ):
                    #    matchstr = '%s?' % var
                    #else:
                    matchstr = command

                    #print "Match Expression :", '^(%s)(.*)(%s|\?)$' % (attrib,unit), " ", matchstr
                    #m = re.match( '^(%s)(.*)(%s|\?)$' % (attrib,unit), matchstr )
                    m = re.match( '^(%s)([^?]*)(%s|\?)$' % (attrib,unit), matchstr )

                    if ( m ):
                        grps = m.groups()
                        curr = None
                        if ( var is None ):
                            var  = grps[0].replace(':', hex(ord(':')) )
                        else:
                            if ( var == '__current__' ) :
                                setval = grps[1].strip()
                                #print "Setting __current__ to ", setval
                                setattr ( self, var, setval )
                                #print dir (self), self.__current__
                                continue

                        if ( not hasattr( self, var ) ):
                            #print "Setting up dictionary %s" % var
                            setattr( self, var, dict() )

                        dictionary = getattr( self, var )
                        if ( not dictionary.has_key( self.__current__ ) ):
                            # Then create a default
                            dictionary[ self.__current__ ] = default

                        if ( grps[-1] == '?' ):
                            getval     = dictionary[ self.__current__ ]
                            print "Getting Attribute %s : %s" % (var, str(getval))
                            return str(getval)
                        else:
                            setval = grps[1].strip()

                            # ==================================================
                            # PLACE FOR HANDLING EXCEPTIONS
                            # ==================================================
                            if (self.model == 'SMA'):
                                if (attrib == 'FREQ'):
                                    setval = str(float(setval)*1e6)

                            #setattr ( self, var, setval )
                            dictionary[ self.__current__ ] = setval
                            print "Setting Attribute %s : %s" % (var, setval)
                            return

                # If you reach here then you did not find the item
                #print "Invalid Command : %s" % string
                return False

    visa = visa ()
