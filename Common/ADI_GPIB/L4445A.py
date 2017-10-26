#-----------------------------------------------------------------------------
# Name:        L4445A.py
# Purpose:     GPIB Instrument wrapper for Agilent L4445A Switch Driver
#              supporting the 87206A, L7206A and N1810UL switches.
#
# Author:      Kaushal Shrestha
#
# Created:     2013/10/17
# RCS-ID:      $Id: L4445A.py 421 2014-03-12 14:57:26Z kshresth $
# Copyright:   (c) Analog Devices Inc. 2013
#-----------------------------------------------------------------------------

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass

def overridden(method):
    import inspect, re
    stack = inspect.stack()
    base_classes = re.search(r'class.+\((.+)\)\s*\:', stack[2][4][0])
    if base_classes is not None:
        base_classes = base_classes.group(1)

    if base_classes is not None:
        # Handle multiple inheritance
        base_classes = [s.strip() for s in base_classes.split(',')]

    if not base_classes:
        raise AttributeError('overrides decorator: unable to determine base class')

    # stack[0]=overrides, stack[1]=inside class def'n, stack[2]=outside class def'n
    derived_class_locals = stack[2][0].f_locals

    # Replace each class name in base_classes with the actual class type
    for i, base_class in enumerate(base_classes):

        if '.' not in base_class:
            base_classes[i] = derived_class_locals[base_class]

        else:
            components = base_class.split('.')

            # obj is either a module or a class
            obj = derived_class_locals[components[0]]

            for c in components[1:]:
                assert(inspect.ismodule(obj) or inspect.isclass(obj))
                obj = getattr(obj, c)

            base_classes[i] = obj

    import operator
    assert(reduce(operator.or_, [hasattr(cls, method.__name__) for cls in base_classes] ))
    return method

class L4445A(GPIBObjectBaseClass):
    def __boa_dummy_collapse__():
        pass
    """
    @brief : Class that represents the L4445A Agilent Switch Driver.
    """

    MODULE_DRIVE_SOURCE_INTERNAL = property(lambda x: "INT", None, None, "Readonly INT Source ID.")
    MODULE_DRIVE_SOURCE_EXTERNAL = property(lambda x: "EXT", None, None, "Readonly EXT Source ID.")
    MODULE_DRIVE_SOURCE_OFF      = property(lambda x: "OFF", None, None, "Readonly EXT Source ID.")

    class _34945EXT_(object):
        def __boa_dummy_collapse__():
            pass
        """
        @brief : Innerclass that represents the 34945EXT module.
        """

        NUMBER_OF_BANKS = 4

        def __init__(self, index, l4445a_ref, switches):
            """
            __init__(index)
                @brief : Initializes the 34945EXT module instance.
                @param : index      : Index of the 34945EXT module in the daisy chain.
                @param : l4445a_ref : Reference to an instance of the L4445A object.
                @param : switches   : Python dictionary as defined in __init__ function of L4445A class. @ref L4445A.__init__.switches
            """
            assert(type(index) == int and index > 0)
            self.__index__ = index
            self.__switches__ = {}
            self.__InitializeSwitches__(l4445a_ref, switches)

        def __GetBanks__(self):
            """
            __GetBanks__()
                @brief : Gets the banks in use of the 34945EXT module.
            """
            keys = sorted(self.__switches__.keys())
            return [key[0] for key in keys]

        def __GetIndex__(self):
            """
            __GetIndex__()
                @brief : Gets the index of the 34945EXT module."
            """
            return self.__index__

        def __GetSwitches__(self):
            """
            __GetSwitches__()
                @brief : Gets the swich instances of the 34945EXT module."
            """
            keys = sorted(self.__switches__.keys())
            return [self.__switches__[key] for key in keys]

        def __InitializeSwitches__(self, l4445a_ref, switches):
            """
            __InitializeSwitches__(l4445a_ref, switches)
                @brief : Initializes the switches connected to the banks of the 34945EXT module.
                @param : l4445a_ref : Reference to an instance of the L4445A object.
                @param : switches   : Python dictionary as defined in __init__ function of L4445A class.
                @sa    : L4445A.__init__()
            """
            assert(type(l4445a_ref) == L4445A)
            assert(type(switches) == dict)
            for (bank_no, switch_no), switch_type in sorted(switches.items()):
                assert(type(bank_no) == int)
                assert(type(switch_no) == int)
                assert(type(switch_type) == str)
                if (switch_type == '87206A'):
                    sw_inst = L4445A._87206A_(l4445a_ref, self.Index, bank_no, switch_no)
                elif (switch_type == 'L7206A'):
                    sw_inst = L4445A._L7206A_(l4445a_ref, self.Index, bank_no, switch_no)
                elif (switch_type == 'N1810UL'):
                    sw_inst = L4445A._N1810UL_(l4445a_ref, self.Index, bank_no, switch_no)
                self.__switches__[(bank_no, switch_no)] = sw_inst

        Banks    = property(__GetBanks__,    None, None, "Gets the banks of the 34945EXT module.")
        Index    = property(__GetIndex__,    None, None, "Gets the index of the 34945EXT module the switch is attached to.")
        Switches = property(__GetSwitches__, None, None, "Gets the switch instances of the 34945EXT module.")

    class _AbstractSwitch_(object):
        def __boa_dummy_collapse__():
            pass
        """
        @brief : Innerclass that represents a generic supported Switch.
        """

        def __init__(self, l4445a_ref, _34945ext_index, bank_no, switch_no, pair_mode):
            """
            __init__(l4445a_ref, _34945ext_index, bank_no, switch_no)
                @brief : Initializes an Abstract switch with the given bank number for the given L4445A instance
                        on the given 34945EXT, bank_no and switch_no.
                @param : l4445a_ref      : A python object instance reference of the L4445A.
                @brief : _34945ext_index : The index of the 34945EXT module.
                @param : bank_no         : The bank used on the 34945EXT distribution board.
                @param : switch_no       : The switch used on the selected bank on the 34945EXT distribution board.
                @param : pair_mode       : The switch pairing mode, ON or OFF.
            """
            if (type(self) == L4445A._AbstractSwitch_): raise Exception("Cannot instantiate an Abstract Switch.")
            assert(type(l4445a_ref) == L4445A)
            assert(type(_34945ext_index) == int and _34945ext_index > 0)
            assert(type(bank_no) == int and bank_no >= 1 and bank_no <= L4445A._34945EXT_.NUMBER_OF_BANKS)
            assert(type(switch_no == int and switch_no >= 1 and switch_no <= self.MAX_NUMBER_OF_SWITCHES_PER_BANK))
            assert(type(pair_mode == str and pair_mode in ['OFF', 'ON']))
            self.__34945ext__   = _34945ext_index
            self.__l4445a__     = l4445a_ref
            self.__bank_no__    = bank_no
            self.__switch_no__  = switch_no
            self.__pair_mode__  = pair_mode
            bank = (self.__34945ext__ - 1) * L4445A._34945EXT_.NUMBER_OF_BANKS + self.__bank_no__
            self.__name__       = 'SW%d%d' % (bank, self.__switch_no__)

        def __Get_34945EXT__(self):
            """
            __Get_34945EXT__()
                @brief : Gets the index number of the 34945EXT module the switch is associated with.
            """
            return self.__34945ext__

        def __GetBank__(self):
            """
            __GetBank__()
                @brief : Gets the bank associated with the switch.
            """
            return self.__bank_no__

        def __GetChannel__(self):
            """
            __GetChannel__()
                @brief : Returns the currently closed channel for the switch.
            """
            position_command = 'ROUTe:CHANnel:VERify:POSition:STATe? '
            current_channel = 0
            for ch in [1, 2, 3, 4, 5, 6]:
                position = self.__l4445a__.Query(position_command + self.GetHWChannelID(ch))
                position = position.strip()
                if (position == ""): position = 0
                if (int(position) == 1):
                    current_channel = ch
                    break
            return current_channel

        def __SetChannel__(self, channel):
            """
            __SetChannel__()
                @brief : Prototype for method to set the channel to be overridden by the derived class.
            """
            raise Exception("Needs implementation of __SetChannel__ in the derived class.")

        def __GetID__(self):
            """
            __GetID__()
                @brief : Gets the ID of the switch. It is the combination of the driver (1) and the 34945EXT index and the virtual bank (0 through 7).
            """
            id = "1%d%d" % (self._34945EXT, (self.Bank - 1) * 2 + self.SwitchNo - 1)
            return id

        def __GetName__(self):
            """
            __GetName__()
                @brief : Returns the name of the swich.
            """
            return self.__name__

        def __GetPairMode__(self):
            """
            __GetPairMode__()
                @brief : Returns the pair mode of the swich.
            """
            return self.__pair_mode__

        def __GetSwitchNo__(self):
            """
            __GetSwitchNo__()
                @brief : Returns the index number of the swich.
            """
            return self.__switch_no__

        def GetHWChannelID(self, channel):
            """
            GetHWChannelID(channel)
                @brief : Returns the fully qualified channel name representation of the given channel
                         tagged along with the 34945ext index and the bank.
                @param : channel : Channel.
            """
            assert(type(channel) == int and channel in range(0, 8+1))
            channel_string = "(@%s%d)" % (self.ID, channel)
            return channel_string

        def SelfTest(self):
            raise Exception("Needs implementation of SelfTest in the derived class")

        _34945EXT  = property(__Get_34945EXT__, None, None, "Gets the 34945EXT index of the attached 34945EXT module.")
        Bank       = property(__GetBank__,      None, None, "Gets the bank of the switch in the attached 34945EXT module.")
        ID         = property(__GetID__,        None, None, "Gets the identification string of the switch.")
        Name       = property(__GetName__,      None, None, "Gets the name of the switch.")
        PairMode   = property(__GetPairMode__,  None, None, "Gets the pair mode of the switch.")
        SwitchNo   = property(__GetSwitchNo__,  None, None, "Gets the switch number that the switch is connected as.")

    class _87206A_(_AbstractSwitch_):
        def __boa_dummy_collapse__():
            pass
        """
        @brief : Innerclass that represents the 87206A SP6T switch.
        """

        MAX_NUMBER_OF_SWITCHES_PER_BANK = property(lambda x: 1, None, None, "Readonly maximum number of switches as property")

        def __init__(self, l4445a_ref, _34945ext_index, bank_no, switch_no):
            """
            __init__(l4445a_ref, bank_no, switch_no)
                @brief : Initializes an Agilent L7206A switch with the given bank number for the given
                        L4445A instance on the given 34945EXT, bank_no and switch_no.
                @param : l4445a_ref      : @ref _AbstractSwitch_.l4445a_ref
                @param : _34945ext_index : @ref _AbstractSwitch_._34945ext_index
                @param : bank_no         : @ref _AbstractSwitch_.bank_no
                @param : switch_no       : @ref _AbstractSwitch_.switch_no
                @sa    : See L4445A._AbstractSwitch_() for the parameter definitions.
            """
            super(L4445A._87206A_, self).__init__(l4445a_ref, _34945ext_index, bank_no, switch_no, pair_mode = "ON")

        @overridden
        def __GetChannel__(self):
            """
            __GetChannel__()
                @brief : Returns the currently closed channel for the switch.
            """
            return super(L4445A._87206A_, self).__GetChannel__()

        @overridden
        def __SetChannel__(self, channel):
            """
            __SetChannel__(channel)
                @brief : Sets the channel for the switch.
                @param : channel : Channel
            """
            # Disconnect all the paths, uses CLOSe to disconnect in pair mode.
            command = 'ROUTe:CLOSe (@%s1:%s8)' % (self.ID, self.ID)
            self.__l4445a__.Write(command)

            # If the intent is not to disconnect all, then connect the path that has been requested
            if (channel != 0):
                # Connect the desired path, use OPEN to connect in pair mode.
                command = 'ROUTe:OPEN %s' % (self.GetHWChannelID(channel))
                self.__l4445a__.Write(command)

        @overridden
        def SelfTest(self):
            """
            SelfTest()
                @brief : Executes a self-test on the given switch by toggling through all the channels.
            """
            # Save the state of the switch
            channel = self.Channel

            # Cycle through the switch positions.
            for pos in [6, 5, 4, 3, 2, 1, 0]:
                self.Channel = pos

            # Restore the position of the switch
            self.Channel = channel

        # Overridden Poperties
        Channel = property(__GetChannel__, __SetChannel__, None, "Selects the channel or checks the connected channel.")

    class _L7206A_(_AbstractSwitch_):
        def __boa_dummy_collapse__():
            pass
        """
        @brief : Innerclass that represents the L7206A SP6T switch.
        """

        MAX_NUMBER_OF_SWITCHES_PER_BANK = property(lambda x: 2, None, None, "Readonly maximum number of switches as property")

        def __init__(self, l4445a_ref, _34945ext_index, bank_no, switch_no):
            """
            __init__(l4445a_ref, bank_no, switch_no)
                @brief : Initializes an Agilent L7206A switch with the given bank number for the given
                        L4445A instance on the given 34945EXT, bank_no and switch_no.
                @param : l4445a_ref      : @ref _AbstractSwitch_.l4445a_ref
                @param : _34945ext_index : @ref _AbstractSwitch_._34945ext_index
                @param : bank_no         : @ref _AbstractSwitch_.bank_no
                @param : switch_no       : @ref _AbstractSwitch_.switch_no
                @sa    : See L4445A._AbstractSwitch_() for the parameter definitions.
            """
            super(L4445A._L7206A_, self).__init__(l4445a_ref, _34945ext_index, bank_no, switch_no, pair_mode = "OFF")

        @overridden
        def __GetChannel__(self):
            """
            __GetChannel__()
                @brief : Returns the currently closed channel for the switch.
            """
            position_command = 'ROUTe:CHANnel:VERify:POSition:STATe? '
            current_channel = 0
            for ch in [1, 2, 3, 4, 5, 6]:
                position = self.__l4445a__.Query(position_command + self.GetHWChannelID(ch))
                position = position.strip()
                if (position == ""): position = 0
                if (int(position) == 1):
                    current_channel = ch
                    break
            return current_channel

        @overridden
        def __SetChannel__(self, channel):
            """
            __SetChannel__(channel)
                @brief : Sets the channel for the switch.
                @param : channel : Channel
            """
            assert(type(channel) == int and channel in range(0, 8+1))
            if (channel == 0): channel = 8 # Channel 0 is not valid, 0 : disconnect is really 8
            # Closing one of the switches is enough to disconnect the other in case of L7206A.
            command = 'ROUTe:CLOSe %s' % (self.GetHWChannelID(channel))
            self.__l4445a__.Write(command)

        @overridden
        def SelfTest(self):
            """
            SelfTest()
                @brief : Executes a self-test on the given switch by toggling through all the channels.
            """
            # Save the state of the switch
            channel = self.Channel

            # Cycle through the switch positions.
            for pos in [6, 5, 4, 3, 2, 1, 0]:
                self.Channel = pos

            # Restore the position of the switch
            self.Channel = channel

        # Overridden Poperties
        Channel = property(__GetChannel__, __SetChannel__, None, "Selects the channel or checks the connected channel.")

    class _N1810UL_(_AbstractSwitch_):
        def __boa_dummy_collapse__():
            pass
        """
        @brief : Innerclass that represents the N1810UL SPDT switch.
        """

        MAX_NUMBER_OF_SWITCHES_PER_BANK = property(lambda x: 8, None, None, "Readonly maximum number of switches as property")

        def __init__(self, l4445a_ref, _34945ext_index, bank_no, switch_no):
            """
            __init__(l4445a_ref, _34945ext_index, bank_no, switch_no)
                @brief : Initializes an Agilent N1810UL switch with the given bank number for the given
                        L4445A instance on the given 34945EXT, bank_no and switch_no.
                @param : l4445a_ref      : @ref _AbstractSwitch_.l4445a_ref
                @param : _34945ext_index : @ref _AbstractSwitch_._34945ext_index
                @param : bank_no         : @ref _AbstractSwitch_.bank_no
                @param : switch_no       : @ref _AbstractSwitch_.switch_no
                @sa    : See L4445A._AbstractSwitch_() for the parameter definitions.
            """
            super(L4445A._N1810UL_, self).__init__(l4445a_ref, _34945ext_index, bank_no, switch_no, pair_mode = "ON")

        @overridden
        def __GetChannel__(self):
            """
            __GetChannel__()
                @brief : Gets the channel for the switch.
            """
            position_command = 'ROUTe:CLOSe? '
            position = self.__l4445a__.Query(position_command + self.GetHWChannelID(self.SwitchNo))
            if (position == ""): position = "0"
            position = int(position) + 1
            return position

        @overridden
        def __SetChannel__(self, channel):
            """
            __SetChannel__(channel)
                @brief : Sets the channel for the switch.
                @param : channel : Channel
            """
            assert(type(channel) == int)
            if (channel == 0):
                print "*** INFO  *** : N1810UL Switch model doesn't support complete disconnect"
            else:
                connect_str = ""
                if (channel == 1):
                    connect_str = "OPEN"
                elif (channel == 2):
                    connect_str = "CLOSe"
                else:
                    print "*** WARN *** : Invalid channel %d for N1810UL" % channel
                    return
                command = 'ROUTe:%s (@%s%d)' % (connect_str, self.ID, self.SwitchNo)
                self.__l4445a__.Write(command)

        @overridden
        def __GetID__(self):
            """
            __GetID__()
                @brief : Gets the ID of the switch.
            """
            id = "1%d%d" % (self._34945EXT, (self.Bank - 1) * 2)
            return id

        @overridden
        def SelfTest(self):
            """
            SelfTest()
                @brief : Executes a self-test on the given switch by toggling through all the channels.
            """
            # Save the state of the switch
            channel = self.Channel

            # Cycle through the switch positions.
            for pos in [2, 1]:
                self.Channel = pos

            # Restore the position of the switch
            self.Channel = channel

        # Overridden Poperties
        Channel = property(__GetChannel__, __SetChannel__, None, "Selects the channel or checks the connected channel.")
        ID      = property(__GetID__,      None,           None, "Gets the identification string of the switch")

    def __init__(self, gpib_addr, switches, drive = MODULE_DRIVE_SOURCE_INTERNAL, delay = 0.25, self_test = False):
        """
        __init__(gpib_addr, switches, drive = L4445A.MODULE_DRIVE_SOURCE_INTERNAL, delay = 0.25, self_test = False)
            @brief  : Initializes the L4445A Switch Driver Object, with default switch delay of 0.25 seconds.
            @param  : gpib_addr  : GPIB address of the L4445A Switch Driver. Generally it's set to 9.
            @param  : switches   : Python dictionary keyed with a tuple of (bank_no, switch_no) with values
                                   of the switch model number used on the 34945EXT board using the
                                               Y1150A switch control for N1810UL,
                                               Y1151A switch control for L7206A,
                                               Y1152A switch control for 87206A
                                   The bank no. and switch no. on the bank is used in combination as a key.
                                   The range for banks is [1, 2, 3, 4] for 34945EXT = 1,
                                                           [5, 6, 7, 8] for 34945EXT = 2, and so on.
            @param  : drive      : Drive source for the 34945EXT module (master only)
            @param  : delay      : Delay between switch transitions.
            @param  : self_test  : Run Self Test after initialization.
            @example: L4445A(9, switches = {(1, 1) : 'L7206A', (1, 2) : 'L7206A', (2, 2) : '87206A', (3, 1) : 'N1810UL', (3, 2) : 'N1810UL'})
            @note   : If more than one 34945EXT is used in a daisy chain format, then the bank number
                    needs to have an offset of the total number of banks from the previous 34945EXT modules.
        """
        GPIBObjectBaseClass.__init__(self, 'Agilent Technologies,L4445A', gpib_addr, delay)

        # Validate the switches
        self.__ValidateSwitchMatrix__(switches)

        # Intitialize the switches with the banks. This will also calculate the 34945EXT index based
        # on the bank numbers. If 34945EXT = 2, then the banks should represent (34945EXT*8 + bank_no)
        self.__Initialize34945EXTandSwitches__(switches)

        # Expose the instantiated switches as named attributes of the class
        self.__ExportSwitchesAsAttributes__()

        # Set the drive source for the 34945EXT module based on evaluation of the no. of banks used.
        for _34945ext in self._34945EXTs:
            idx   = _34945ext.Index

            # Turn off Drive Source
            self.__SetDriverModuleSource__(idx, self.MODULE_DRIVE_SOURCE_OFF)
            # Set the pair mode
            self.__SetSwitchPairModeAndVerifyPolarity__()
            # Turn on Drive Source
            drive = self.__EvaluateModuleDriveSource__(idx)
            self.__SetDriverModuleSource__(idx, drive)

        # Disable Channel Verification.
        self.__DisableChannelVerification__()

        # Test out the switches, they should click
        try:
            if (self_test):
                self.TestSwitches()
        except Exception, e:
            print "*** ERROR *** : Unable to run the self-test on the switches. "
            print "                You might want to check the drive source."
            print "                Exception : %s" % str(e)

    def __Initialize34945EXTandSwitches__(self, switches):
        """
        __Initialize34945EXTandSwitches__(switches)
            @brief : Initializes the 34945EXT modules along with the connected switches.
            @param : switches : @ref L4445A.__init__.switches
            @sa    : L4445A.__init__()
        """
        self.__34945exts__ = []
        set_34945ext_idx   = set()
        dict_switches      = dict()

        for bank_no, switch_no in sorted(switches.keys()):
            idx     = ((bank_no - 1) / L4445A._34945EXT_.NUMBER_OF_BANKS) + 1
            bank_no = ((bank_no - 1) % L4445A._34945EXT_.NUMBER_OF_BANKS) + 1
            set_34945ext_idx.add(idx)
            list_switches = []
            if (dict_switches.has_key(idx)): list_switches = dict_switches[idx]
            list_switches.append((bank_no, switch_no))
            dict_switches[idx] = list_switches

        for _34945ext_idx in set_34945ext_idx:
            switches_list = []
            for b, s in dict_switches[_34945ext_idx]:
                switch_key = (b + (_34945ext_idx - 1) * L4445A._34945EXT_.NUMBER_OF_BANKS, s)
                switches_list.append( ((b, s), switches[switch_key]))
            _34945ext = L4445A._34945EXT_(_34945ext_idx, self, dict(switches_list))
            self.__34945exts__.append(_34945ext)

    def __DisableChannelVerification__(self):
        """
        __DisableChannelVerification__()
            @brief : Disables electronic channel verification of the switch position.
        """
        self.__EnableChannelVerification__(False)

    def __EnableChannelVerification__(self, enable = True):
        """
        __EnableChannelVerification__(enable = True)
            @brief : Enables or disables electronic channel verification of the switch position.
            @param : enable : Boolean value representing whether to enable or disable the verification.
        """
        assert(type(enable) == bool)

        if (enable == True):
            enable = "ON"
        else:
            enable = "OFF"

        for _34945ext in self._34945EXTs:
            for sw_inst in _34945ext.Switches:
                id = sw_inst.ID
                ROUTE_CHANNEL_VERIFICATION_command = 'ROUTe:CHANnel:VERify:ENABle %s, (@%s1:%s8)'
                command = ROUTE_CHANNEL_VERIFICATION_command % (enable, id, id)
                self.Write(command)

    def __ExportSwitchesAsAttributes__(self):
        """
        __ExportSwitchesAsAttributes__()
            @brief : Export the switch instances as attributes of the L4445 instance.
        """
        self.__switch_instances__ = []
        for _34945ext in self._34945EXTs:
            for sw_inst in _34945ext.Switches:
                sw_name = sw_inst.Name
                setattr(self, sw_name, sw_inst)
                self.__switch_instances__.append(sw_inst)

    def __EvaluateModuleDriveSource__(self, idx_34945ext):
        """
        __EvaluateModuleDriveSource__(idx_34945ext)
            @brief : Evaluate the module drive source for the given 34945EXT index based on the number
                    of switches connected.
            @param : idx_34945ext : Index of the 34945EXT module.
        """
        for _34945ext in self._34945EXTs:
            if (_34945ext.Index == idx_34945ext):
                if (_34945ext.Index != 1):
                    return self.MODULE_DRIVE_SOURCE_EXTERNAL
                banks_on_34945ext = _34945ext.Banks
                if (len(banks_on_34945ext) > 3):
                    return self.MODULE_DRIVE_SOURCE_EXTERNAL
                break
        return self.MODULE_DRIVE_SOURCE_INTERNAL

    def __Get34945EXTs__(self):
        """
        __Get34945EXTs__()
            @brief : Returns the instances of the 34945EXT modules available.
        """
        return self.__34945exts__

    def __GetSwitches__(self):
        """
        __GetSwitches__()
            @brief : Returns the switch instances in the system.
        """
        return self.__switch_instances__

    def __SetDriverModuleSource__(self, idx_34945ext, source):
        """
        __SetDriverModuleSource__(idx_34945ext, source)
            @brief : Automatically sets the driver module driver source for the 34945EXT module.
            @param : idx_34945ext : Index of the 34945EXT module.
            @param : source : INT or EXT or OFF source.
        """
        assert(type(source) == str and source in [self.MODULE_DRIVE_SOURCE_EXTERNAL, \
                                                  self.MODULE_DRIVE_SOURCE_INTERNAL, \
                                                  self.MODULE_DRIVE_SOURCE_OFF])
        assert(type(idx_34945ext) == int and idx_34945ext > 0)
        #print "*** INFO  *** : Setting Drive source on 34945EXT#%d : %s" % (idx_34945ext, source)
        MODULE_DRIVE_SOURCE_command = 'ROUTe:RMODule:DRIVe:SOURce %s, (@1%d00)'
        command = MODULE_DRIVE_SOURCE_command % (source, idx_34945ext)
        self.Write(command)

    def __SetSwitchPairModeAndVerifyPolarity__(self):
        """
        __SetSwitchPairModeAndVerifyPolarity__()
            @brief : Sets the pair mode based on the pair mode definition described in the switch definition.
        """
        for _34945ext in self._34945EXTs:
            for sw_inst in _34945ext.Switches:
                id = sw_inst.ID
                pair_mode = sw_inst.PairMode
                polarity = "NORMal"
                # ------------------------
                # Set Pair Mode
                # ------------------------
                ROUTE_CHANNEL_PAIR_MODE_command = 'ROUTe:CHANnel:DRIVe:PAIR:MODE %s, (@%s1:%s8)'
                command = ROUTE_CHANNEL_PAIR_MODE_command % (pair_mode, id, id)
                #print "*** INFO  *** : Setting Pair Mode to %s on (@%s1:%s8)" % (pair_mode, id, id)
                self.Write(command)
                # ------------------------
                # Set Verify Polarity Mode
                # ------------------------
                if (pair_mode == "ON"): polarity = "INVerted"
                #print "*** INFO  *** : Setting Verification Polarity to %s on (@%s1:%s8)" % (polarity, id, id)
                ROUTE_CHANNEL_VERIFY_POLARITY_command = 'ROUTe:CHANnel:VERify:POLarity %s, (@%s1:%s8)'
                command = ROUTE_CHANNEL_VERIFY_POLARITY_command % (polarity, id, id)
                self.Write(command)

    def __ValidateSwitchMatrix__(self, switches):
        """
        __ValidateSwitchMatrix__(switches):
            @brief : Validates the switches defined based on
            @param : switches : @ref L4445A.__init__.switches
        """
        assert(type(switches) == dict)
        prev_bank_no = 0
        prev_switch_type = ''
        for bank_sw_key in sorted(switches.keys()):
            if not (len(bank_sw_key) == 2):
                raise AttributeError("Expected a bank/switch tuple for a key but instead got %s." % str(bank_sw_key))
            bank_no, switch_no = bank_sw_key
            switch_type = switches[bank_sw_key]
            if not (type(bank_no) is int and type(switch_no) is int):
                raise AttributeError("Expected numeric value for bank and switch but instead got %s and %s." % (str(type(bank_no)), str(type(switch_no))))
            if not (type(switch_type) is str):
                raise AttributeError("Expected string value for switch type but instead got %s." % (str(type(switch_type))))
            if not (bank_no in [1, 2, 3, 4]):
                raise AttributeError("Expected bank number to be a value between 1 and 4, but instead got %d. \nIf using a second 34945EXE board, please contact Kaushal Shrestha." % (bank_no))
            if (switch_type == '87206A' and not switch_no in [1]):
                raise AttributeError("An 87206A switch can only be assigned to swtich port 1, but instead got %d." % switch_no)
            if (switch_type == 'L7206A' and not (switch_no in [1, 2])):
                raise AttributeError("A L7206A switch can only be assigned to swtich port 1 or 2, but instead got %d." % switch_no)
            if (switch_type == 'N1810UL' and not (switch_no in [1, 2, 3, 4, 5, 6, 7, 8])):
                raise AttributeError("A N1810UL switch can only be assigned to swtich port 1 through 8, but instead got %d." % switch_no)
            if (prev_bank_no == bank_no and prev_switch_type == '87206A'):
                    raise AttributeError("An 87206A switch has already been defined at bank %d switch 1, and hence this bank cannot be used to define switch %d." % (prev_bank_no, switch_no))
            prev_bank_no = bank_no
            prev_switch_type = switch_type

    def ClearErrors(self):
        """
        ClearErrors()
            @brief : Clears the errors in the L4445 driver.
        """
        error = self.Write( '*CLS' )

    def GetErrors(self):
        """
        GetErrors()
            @brief : Gets the errors from the L4445 driver.
        """
        errors=[]
        while ( True ) :
            error = self.Query( 'SYST:ERR?' )
            if ( error == '+0,"No error"' ): break
            errors.append( error )
        return errors

    def Reset(self):
        """
        Reset()
            @brief : Resets the L4445 driver.
        """
        self.Write('*RST')

    def SwitchDriverModuleSource(self, idx_34945ext, source):
        """
        SwitchDriverModuleSource(idx_34945ext, source)
            @brief : Forces the driver module driver source for the 34945EXT module.
            @param : idx_34945ext : Index of the 34945EXT module.
            @param : source : INT or EXT source.
        """
        assert(type(source) == str and source in [self.MODULE_DRIVE_SOURCE_EXTERNAL, self.MODULE_DRIVE_SOURCE_INTERNAL])
        assert(type(idx_34945ext) == int and idx_34945ext > 0)
        # Issue Reset
        self.Reset()
        # Setup the driver source
        self.__SetDriverModuleSource__(idx_34945ext, source)
        # Disable Channel Verification (as the reset was issued)
        self.__DisableChannelVerification__()

    def TestSwitches(self):
        """
        TestSwitches()
            @brief : Run self-test on all available switches in the system.
        """
        try:
            delay = self.Delay
            self.Delay = 0
            for _34945ext in self._34945EXTs:
                for sw in _34945ext.Switches:
                    try:
                        # Run the SelfTest for the switches.
                        sw.SelfTest()
                    except Exception, e:
                        raise RuntimeError("%s.SelfTest() : %s" % (sw.__name__, str(e)))
            self.Delay = delay
        except RuntimeError, e:
            self.Delay = delay
            raise e

    _34945EXTs = property(__Get34945EXTs__, None, None, "Gets the 34945EXT indices")
    Errors     = property(GetErrors,        None, None, "Gets the errors from the L4445 driver")
    Switches   = property(__GetSwitches__,  None, None, "Gets the switch instances in the system")
