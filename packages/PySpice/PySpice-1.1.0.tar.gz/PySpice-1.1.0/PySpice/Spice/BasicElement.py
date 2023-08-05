####################################################################################################
#
# PySpice - A Spice Package for Python
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

"""This module implements SPICE circuit elements.

.. warning:: Some elements are partially implemented.

.. warning:: The API documentation generated by Sphinx is perfectible for this module. The source
             code can be more informative.

.. note:: It would be nice to have an use-full and working documentation in the interactive environment.

The element's parameters are internally implemented using class attributes and descriptors.

There are two types of parameters, positionals which are required and where the order mater, and
optional parameters which are passed as keyword arguments.

Parameters are registered with more expressive and longer names than their Spice counterparts.  For
optional parameters, we can use both Spice and longer name for convenience.

See Ngspice documentation for details.

+--------------+------------------------------------------------------+
| First letter + Element description                                  |
+--------------+------------------------------------------------------+
| A            + XSPICE code model                                    |
+--------------+------------------------------------------------------+
| B            + Behavioral (arbitrary) source                        |
+--------------+------------------------------------------------------+
| C            + Capacitor                                            |
+--------------+------------------------------------------------------+
| D            + Diode                                                |
+--------------+------------------------------------------------------+
| E            + Voltage-controlled voltage source (VCVS)             |
+--------------+------------------------------------------------------+
| F            + Current-controlled current source (CCCs)             |
+--------------+------------------------------------------------------+
| G            + Voltage-controlled current source (VCCS)             |
+--------------+------------------------------------------------------+
| H            + Current-controlled voltage source (CCVS)             |
+--------------+------------------------------------------------------+
| I            + Current source                                       |
+--------------+------------------------------------------------------+
| J            + Junction field effect transistor (JFET)              |
+--------------+------------------------------------------------------+
| K            + Coupled (Mutual) Inductors                           |
+--------------+------------------------------------------------------+
| L            + Inductor                                             |
+--------------+------------------------------------------------------+
| M            + Metal oxide field effect transistor (MOSFET)         |
+--------------+------------------------------------------------------+
| N            + Numerical device for GSS                             |
+--------------+------------------------------------------------------+
| O            + Lossy transmission line                              |
+--------------+------------------------------------------------------+
| P            + Coupled multiconductor line (CPL)                    |
+--------------+------------------------------------------------------+
| Q            + Bipolar junction transistor (BJT)                    |
+--------------+------------------------------------------------------+
| R            + Resistor                                             |
+--------------+------------------------------------------------------+
| S            + Switch (voltage-controlled)                          |
+--------------+------------------------------------------------------+
| T            + Lossless transmission line                           |
+--------------+------------------------------------------------------+
| U            + Uniformly distributed RC line                        |
+--------------+------------------------------------------------------+
| V            + Voltage source                                       |
+--------------+------------------------------------------------------+
| W            + Switch (current-controlled)                          |
+--------------+------------------------------------------------------+
| X            + Subcircuit                                           |
+--------------+------------------------------------------------------+
| Y            + Single lossy transmission line (TXL)                 |
+--------------+------------------------------------------------------+
| Z            + Metal semiconductor field effect transistor (MESFET) |
+--------------+------------------------------------------------------+

"""

# Fixme: add transmission lines

####################################################################################################

from ..Tools.StringTools import join_list, str_spice
from ..Unit import U_m, U_s, U_A, U_V, U_Degree, U_Ω, U_F, U_H, U_Hz
from .Netlist import (Pin,
                      AnyPinElement,
                      TwoPinElement, ThreePinElement, FourPinElement,
                      NPinElement,
                      TwoPortElement)
from .ElementParameter import (
    # KeyValueParameter,
    BoolKeyParameter,
    ElementNamePositionalParameter,
    ExpressionKeyParameter,
    ExpressionPositionalParameter,
    FlagParameter,
    FloatKeyParameter,
    FloatPairKeyParameter,
    FloatTripletKeyParameter,
    FloatPositionalParameter,
    InitialStatePositionalParameter,
    IntKeyParameter,
    ModelPositionalParameter,
    )

####################################################################################################

class SubCircuitElement(NPinElement):

    """This class implements a sub-circuit.

    Spice syntax::

        XYYYYYY node1 node2 ... subcircuit_name parameter1=value1 ...

    Attributes:

      :attr:`subcircuit_name`

    .note : As opposite to Spice, the circuit's name is specified before the nodes so as to act as
    `*args`.

    """

    alias = 'X'
    prefix = 'X'

    subcircuit_name = ElementNamePositionalParameter(position=0, key_parameter=False)

    ##############################################

    def __init__(self, name, subcircuit_name, *nodes, **parameters):

        pins = [Pin(self, None, node) for node in nodes]

        super().__init__(name, pins, subcircuit_name)

        self.parameters = parameters

        # Fixme: investigate
        # for key, value in parameters.items():
        #     parameter = KeyValueParameter(key)
        #     parameter.__set__(self, value)
        #     self.optional_parameters[key] = parameter
        #     setattr(self, key, parameter)

    ##############################################

    def format_spice_parameters(self):
        """ Return the formatted list of parameters. """

        spice_parameters = super().format_spice_parameters()
        if self.parameters:
            spice_parameters += ' ' + join_list(['{}={}'.format(key, str_spice(value))
                                                 for key, value in self.parameters.items()])

        return spice_parameters

####################################################################################################

class Resistor(TwoPinElement):

    """This class implements a resistor.

    Spice syntax::

        RXXXXXXX n+ n- value <ac=val> <m=val> <scale=val> <temp=val> <dtemp=val> <noisy=0|1>

    Keyword Parameters:

      :attr:`ac`

      :attr:`multiplier`
         alias `m`

      :attr:`scale`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

      :attr:`noisy`

    Attributes:

      :attr:`resistance`

      :attr:`ac`

      :attr:`multiplier`

      :attr:`scale`

      :attr:`temperature`

      :attr:`device_temperature`

      :attr:`noisy`

    """

    alias = 'R'
    prefix = 'R'

    resistance = FloatPositionalParameter(position=0, key_parameter=False, unit=U_Ω)
    ac = FloatKeyParameter('ac', unit=U_Ω)
    multiplier = IntKeyParameter('m')
    scale = FloatKeyParameter('scale')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)
    noisy = BoolKeyParameter('noisy')

####################################################################################################

class SemiconductorResistor(TwoPinElement):

    """This class implements a Semiconductor resistor.

    Spice syntax::

        RXXXXXXX n+ n- <value> <mname> <l=length> <w=width> <temp=val> <dtemp=val> m=<val> <ac=val> <scale=val> <noisy=0|1>

    Keyword Parameters:

      :attr:`model`

      :attr:`length`
         alias `l`

      :attr:`width`
         alias `w`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

      :attr:`multiplier`
         alias `m`

      :attr:`ac`

      :attr:`scale`

      :attr:`noisy`

    Attributes:

      :attr:`resistance`

      :attr:`model`

      :attr:`length`

      :attr:`width`

      :attr:`temperature`

      :attr:`device_temperature`

      :attr:`multiplier`

      :attr:`ac`

      :attr:`scale`

      :attr:`noisy`

    """

    alias = 'SemiconductorResistor'
    prefix = 'R'

    resistance = FloatPositionalParameter(position=0, key_parameter=False, unit=U_Ω)
    model = ModelPositionalParameter(position=1, key_parameter=True)
    length = FloatKeyParameter('l', unit=U_m)
    width = FloatKeyParameter('w', unit=U_m)
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)
    multiplier = IntKeyParameter('m')
    ac = FloatKeyParameter('ac', unit=U_Ω)
    scale = FloatKeyParameter('scale')
    noisy = BoolKeyParameter('noisy')

####################################################################################################

class BehavioralResistor(TwoPinElement):

    # Behavioral / Behavioural

    """This class implements a behavioral resistor.

    Spice syntax::

        RXXXXXXX n+ n- 'expression' <tc1=value> <tc2=value>
        Rxxxxxxx n+ n- R='expression' <tc1=value> <tc2=value>

    Keyword Parameters:

      :attr:`tc1`

      :attr:`tc2`

    Attributes:

      :attr:`resistance_expression`

      :attr:`tc1`

      :attr:`tc2`

    """

    alias = 'BehavioralResistor'
    prefix = 'R'

    resistance_expression = ExpressionPositionalParameter(position=0, key_parameter=False)
    tc1 = FloatKeyParameter('tc1')
    tc2 = FloatKeyParameter('tc2')

####################################################################################################

class Capacitor(TwoPinElement):

    """This class implements a capacitor.

    Spice syntax::

        CXXXXXXX n+ n- <value> <mname> <m=val> <scale=val> <temp=val> <dtemp=val> <ic=init_condition>

    Keyword Parameters:

      :attr:`model`

      :attr:`multiplier`
         alias `m`

      :attr:`scale`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

      :attr:`initial_condition`
         alias `ic`

    Attributes:

      :attr:`capacitance`

      :attr:`model`

      :attr:`multiplier`

      :attr:`scale`

      :attr:`temperature`

      :attr:`device_temperature`

      :attr:`initial_condition`

    """

    alias = 'C'
    prefix = 'C'

    capacitance = FloatPositionalParameter(position=0, key_parameter=False, unit=U_F)
    model = ModelPositionalParameter(position=1, key_parameter=True)
    multiplier = IntKeyParameter('m')
    scale = FloatKeyParameter('scale')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)
    initial_condition = FloatKeyParameter('ic')

####################################################################################################

class SemiconductorCapacitor(TwoPinElement):

    """This class implements a semiconductor capacitor.

    Spice syntax::

        CXXXXXXX n+ n- <value> <mname> <l=length> <w=width> <m=val> <scale=val> <temp=val> <dtemp=val> <ic=init_condition>

    Keyword Parameters:

      :attr:`model`

      :attr:`length`
         alias `l`

      :attr:`width`
         alias `w`

      :attr:`multiplier`
         alias `m`

      :attr:`scale`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

      :attr:`initial_condition`
         alias `ic`

    Attributes:

      :attr:`capacitance`

      :attr:`model`

      :attr:`length`

      :attr:`width`

      :attr:`multiplier`

      :attr:`scale`

      :attr:`temperature`

      :attr:`device_temperature`

      :attr:`initial_condition`

    """

    alias = 'SemiconductorCapacitor'
    prefix = 'C'

    capacitance = FloatPositionalParameter(position=0, key_parameter=False, unit=U_F)
    model = ModelPositionalParameter(position=1, key_parameter=True)
    length = FloatKeyParameter('l', unit=U_m)
    width = FloatKeyParameter('w', unit=U_m)
    multiplier = IntKeyParameter('m')
    scale = FloatKeyParameter('scale')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)
    initial_condition = FloatKeyParameter('ic')

####################################################################################################

class BehavioralCapacitor(TwoPinElement):

    """This class implements a behavioral capacitor.

    Spice syntax::

        CXXXXXXX n+ n- 'expression' <tc1=value> <tc2=value>
        CXXXXXXX n+ n- C='expression' <tc1=value> <tc2=value>

    Keyword Parameters:

      :attr:`tc1`

      :attr:`tc2`

    Attributes:

      :attr:`capacitance_expression`

      :attr:`tc1`

      :attr:`tc2`

    """

    alias = 'BehavioralCapacitor'
    prefix = 'C'

    capacitance_expression = ExpressionPositionalParameter(position=0, key_parameter=False)
    tc1 = FloatKeyParameter('tc1')
    tc2 = FloatKeyParameter('tc2')

####################################################################################################

class Inductor(TwoPinElement):

    """This class implements an inductor.

    Spice syntax::

        LYYYYYYY n+ n- <value> <mname> <nt=val> <m=val> <scale=val> <temp=val> <dtemp=val> <ic=init_condition>

    Keyword Parameters:

      :attr:`nt`

      :attr:`multiplier`
         alias `m`

      :attr:`scale`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

      :attr:`initial_condition`
         alias `ic`

    Attributes:

      :attr:`inductance`

      :attr:`model`

      :attr:`nt`

      :attr:`multiplier`

      :attr:`scale`

      :attr:`temperature`

      :attr:`device_temperature`

      :attr:`initial_condition`

    """

    alias = 'L'
    prefix = 'L'

    inductance = FloatPositionalParameter(position=0, key_parameter=False, unit=U_H)
    model = ModelPositionalParameter(position=1, key_parameter=True)
    nt = FloatKeyParameter('nt')
    multiplier = IntKeyParameter('m')
    scale = FloatKeyParameter('scale')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)
    initial_condition = FloatKeyParameter('ic')

####################################################################################################

class BehavioralInductor(TwoPinElement):

    """This class implements a behavioral inductor.

    Spice syntax::

        LXXXXXXX n+ n- 'expression' <tc1=value> <tc2=value>
        LXXXXXXX n+ n- L='expression' <tc1=value> <tc2=value>

    Keyword Parameters:

      :attr:`tc1`

      :attr:`tc2`

    Attributes:

      :attr:`inductance_expression`

      :attr:`tc1`

      :attr:`tc2`

    """

    alias = 'BehavioralInductor'
    prefix = 'L'

    inductance_expression = ExpressionPositionalParameter(position=0, key_parameter=False)
    tc1 = FloatKeyParameter('tc1')
    tc2 = FloatKeyParameter('tc2')

####################################################################################################

class CoupledInductor(AnyPinElement):

    """This class implementss a coupled (mutual) inductors.

    Spice syntax::

        KXXXXXXX LYYYYYYY LZZZZZZZ value

    Keyword Parameters:

    Attributes:

      :attr:`inductor1`

      :attr:`inductor2`

      :attr:`coupling_factor`

    """

    alias = 'CoupledInductor'
    prefix = 'K'

    inductor1 = ElementNamePositionalParameter(position=0, key_parameter=False)
    inductor2 = ElementNamePositionalParameter(position=1, key_parameter=False)
    coupling_factor = FloatPositionalParameter(position=2, key_parameter=False)

 ##############################################

    def __init__(self, name, inductor_name1, inductor_name2, coupling_factor):

        # Fixme: any pins here
        super().__init__(name, (),
                                              inductor_name1, inductor_name2, coupling_factor)
        self._inductor_names = (inductor_name1, inductor_name2)

####################################################################################################

class VoltageControlledSwitch(TwoPortElement):

    """This class implements a voltage controlled switch.

    Spice syntax::

        SXXXXXXX n+ n- nc+ nc- model <on> <off>

    Keyword Parameters:

      :attr:`model`

      :attr:`initial_state`

    Attributes:

      :attr:`model`

      :attr:`initial_state`

    """

    alias = 'VCS'
    prefix = 'S'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    initial_state = InitialStatePositionalParameter(position=1, key_parameter=True)

####################################################################################################

class CurrentControlledSwitch(TwoPinElement):

    """This class implements a current controlled switch.

    Spice syntax::

        WYYYYYYY n+ n- vname model <on> <off>

    Keyword Parameters:

      :attr:`source`

      :attr:`model`

      :attr:`initial_state`

    Attributes:

      :attr:`source`

      :attr:`model`

      :attr:`initial_state`

    """

    alias = 'CCS'
    prefix = 'W'

    source = ElementNamePositionalParameter(position=0, key_parameter=True)
    model = ModelPositionalParameter(position=1, key_parameter=True)
    initial_state = InitialStatePositionalParameter(position=2, key_parameter=True)

####################################################################################################

class VoltageSource(TwoPinElement):

    """This class implements an independent sources for voltage.

    Spice syntax::

        VXXXXXXX n+ n- <<dc> dc/tran value> <ac <acmag <acphase>>> <distof1 <f1mag <f1phase>>> <distof2 <f2mag <f2phase>>>

    Keyword Parameters:

    Attributes:

      :attr:`dc_value`

    """

    alias = 'V'
    prefix = 'V'

    # Fixme: ngspice manual doesn't describe well the syntax
    dc_value = FloatPositionalParameter(position=0, key_parameter=False, unit=U_V)

####################################################################################################

class CurrentSource(TwoPinElement):

    """This class implements an independent sources for current.

    Spice syntax::

       IYYYYYYY n+ n- <<dc> dc/tran value> <ac <acmag <acphase>>> <distof1 <f1mag <f1phase>>> <distof2 <f2mag <f2phase>>>

    Keyword Parameters:

    Attributes:

      :attr:`dc_value`

    """

    alias = 'I'
    prefix = 'I'

    # Fixme: ngspice manual doesn't describe well the syntax
    dc_value = FloatPositionalParameter(position=0, key_parameter=False, unit=U_A)

####################################################################################################

class VoltageControlledVoltageSource(TwoPortElement):

    """This class implements a linear voltage-controlled voltage sources (VCVS).

    Spice syntax::

        EXXXXXXX n+ n- nc+ nc- value

    Keyword Parameters:

    Attributes:

      :attr:`voltage_gain`

    """

    alias = 'VCVS'
    prefix = 'E'

    voltage_gain = ExpressionPositionalParameter(position=0, key_parameter=False)

####################################################################################################

class CurrentControlledCurrentSource(TwoPinElement):

    """This class implements a linear current-controlled current sources (CCCS).

    Spice syntax::

       FXXXXXXX n+ n- vname value

    Keyword Parameters:

    Attributes:

      :attr:`source`

      :attr:`current_gain`

    """

    alias = 'CCCS'
    prefix = 'F'

    source = ElementNamePositionalParameter(position=0, key_parameter=False)
    current_gain = ExpressionPositionalParameter(position=1, key_parameter=False)

####################################################################################################

class VoltageControlledCurrentSource(TwoPortElement):

    """This class implements a linear voltage-controlled current sources (VCCS).

    .. warning:: partially implemented

    Spice syntax::

        Gxxx n+ n- nc+ nc- value
        Gxxx n+ n- value={expr}
        Gxxx n1 n2 TABLE {expression}=(x0,y0) (x1,y1) (x2,y2)
        Gxxx n+ n- ( POLY (nd) ) nc1+ nc1- ( nc2+ nc2- ... ) p0 ( p1 ... )
        Laplace

    Keyword Parameters:

    Attributes:

      :attr:`transconductance`

    """

    alias = 'VCCS'
    prefix = 'G'

    transconductance = ExpressionPositionalParameter(position=0, key_parameter=False)

####################################################################################################

class CurrentControlledVoltageSource(TwoPinElement):

    """This class implements a linear current-controlled voltage sources (ccvs).

    Spice syntax::

        HXXXXXXX n+ n- vname value

    Keyword Parameters:

    Attributes:

      :attr:`source`

      :attr:`transresistance`

    """

    alias = 'CCVS'
    prefix = 'H'

    source = ElementNamePositionalParameter(position=0, key_parameter=False)
    transresistance = ExpressionPositionalParameter(position=1, key_parameter=False)

####################################################################################################

class BehavioralSource(TwoPinElement):

    """This class implements a behavioral source.

    Spice syntax::

        BXXXXXXX n+ n- <i=expr> <v=expr> <tc1=value> <tc2=value> <temp=value> <dtemp=value>

    Keyword Parameters:

      :attr:`current_expression`
          alias `i`

      :attr:`voltage_expression`
          alias `v`

      :attr:`tc1`

      :attr:`tc2`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

    Attributes:

      :attr:`current_expression`

      :attr:`voltage_expression`

      :attr:`tc1`

      :attr:`tc2`

      :attr:`temperature`

      :attr:`device_temperature`

    """

    alias = 'BehavioralSource'
    prefix = 'B'

    current_expression = ExpressionKeyParameter('i')
    voltage_expression = ExpressionKeyParameter('v')
    tc1 = FloatKeyParameter('tc1')
    tc2 = FloatKeyParameter('tc2')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)

####################################################################################################

class NonLinearVoltageSource(TwoPinElement):

    """This class implements a non linear voltage source.

    .. warning:: partially implemented

    Spice syntax::

        Exxx n+ n- vol='expr'
        Exxx n+ n- value={expr}
        Exxx n1 n2 TABLE {expression}=(x0,y0) (x1,y1) (x2,y2)
        Exxx n+ n- ( POLY (nd) ) nc1+ nc1- ( nc2+ nc2- ... ) p0 ( p1 ... )
        Laplace

    Keyword Parameters:

    Attributes:

    """

    alias = 'NonLinearVoltageSource'
    prefix = 'E'

    ##############################################

    def __init__(self, name,
                 node_plus, node_minus,
                 expression=None,
                 table=None):

        super().__init__(name, node_plus, node_minus)

        self.expression = expression
        self.table = table

    ##############################################

    def __str__(self):

        spice_element = self.format_node_names()
        # Fixme: expression
        if self.table is not None:
            # TABLE {expression} = (x0, y0) (x1, y1) ...
            table = ['({}, {})'.format(str_spice(x), str_spice(y)) for x, y in self.table]
            spice_element += ' TABLE {%s} = %s' % (self.expression, join_list(table))
        return spice_element

####################################################################################################

class Diode(TwoPinElement):

    """This class implements a junction diode.

    Spice syntax::

        DXXXXXXX n+ n- mname <area=val> <m=val> <pj=val> <off> <ic=vd> <temp=val> <dtemp=val>

    Keyword Parameters:

      :attr:`model`

      :attr:`area`

      :attr:`multiplier`
         alias `m`

      :attr:`pj`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

    Attributes:

      :attr:`model`

      :attr:`area`

      :attr:`multiplier`

      :attr:`pj`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`

      :attr:`device_temperature`

    """

    alias = 'D'
    prefix = 'D'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    area = FloatKeyParameter('area')
    multiplier = IntKeyParameter('m')
    pj = FloatKeyParameter('pj')
    off = FlagParameter('off')
    ic = FloatPairKeyParameter('ic')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)

####################################################################################################

class BipolarJunctionTransistor(NPinElement):

    """This class implements a bipolar junction transistor.

    Spice syntax::

         QXXXXXXX nc nb ne <ns> mname <area=val> <areac=val> <areab=val> <m=val> <off> <ic=vbe,vce> <temp=val> <dtemp=val>

    Keyword Parameters:

      :attr:`model`

      :attr:`area`

      :attr:`areac`

      :attr:`areab`

      :attr:`multiplier`
         alias `m`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`
         alias `temp`

      :attr:`device_temperature`
         alias `dtemp`

    Attributes:

      :attr:`model`

      :attr:`area`

      :attr:`areac`

      :attr:`areab`

      :attr:`multiplier`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`

      :attr:`device_temperature`

    """

    # Fixme: off doesn't fit in kwargs !

    alias = 'BJT'
    prefix = 'Q'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    area = FloatKeyParameter('area')
    areac = FloatKeyParameter('areac')
    areab = FloatKeyParameter('areab')
    multiplier = IntKeyParameter('m')
    off = FlagParameter('off')
    ic = FloatPairKeyParameter('ic')
    temperature = FloatKeyParameter('temp', unit=U_Degree)
    device_temperature = FloatKeyParameter('dtemp', unit=U_Degree)

    ##############################################

    def __init__(self, name,
                 collector_node, base_node, emitter_node,
                 substrate_node=None, # default is ground
                 **kwargs):

        pins = [Pin(self, 'collector', collector_node),
                Pin(self, 'base', base_node),
                Pin(self, 'emitter', emitter_node),]
        if substrate_node is not None:
            self._substrate_pin = Pin(self, 'substrate', substrate_node)
            pins.append(self._substrate_pin)

        super().__init__(name, pins, **kwargs)

    ##############################################

    @property
    def collector(self):
        return self.pins[0]

    ##############################################

    @property
    def base(self):
        return self.pins[1]

    ##############################################

    @property
    def emitter(self):
        return self.pins[2]

    ##############################################

    @property
    def substrate(self):
        try:
            return self.pins[3]
        except IndexError:
            return None

####################################################################################################

class JunctionFieldEffectTransistor(ThreePinElement):

    """This class implements a bipolar junction transistor.

    Spice syntax::

         JXXXXXXX nd ng ns mname <area> <off> <ic=vds,vgs> <temp=t>

    Keyword Parameters:

      :attr:`model`

      :attr:`area`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`
         alias `temp`

    Attributes:

      :attr:`model`

      :attr:`area`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`

    """

    # Fixme: off doesn't fit in kwargs !

    alias = 'JFET'
    prefix = 'J'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    area = FloatKeyParameter('area')
    multiplier = IntKeyParameter('m')
    off = FlagParameter('off')
    ic = FloatPairKeyParameter('ic')
    temperature = FloatKeyParameter('temp', unit=U_Degree)

    ##############################################

    def __init__(self, name,
                 drain_node, gate_node, source_node,
                 **kwargs):

        pins = [Pin(self, 'drain', drain_node),
                Pin(self, 'gate', gate_node),
                Pin(self, 'source', source_node),]

        super().__init__(name, pins, **kwargs)

    ##############################################

    @property
    def drain(self):
        return self.pins[0]

    ##############################################

    @property
    def gate(self):
        return self.pins[1]

    ##############################################

    @property
    def source(self):
        return self.pins[2]

####################################################################################################

class Mesfet(ThreePinElement):

    """This class implements a Metal Semiconductor Field Effect Transistor.

    Spice syntax::

         ZXXXXXXX nd ng ns mname <area> <off> <ic=vds,vgs>

    Keyword Parameters:

      :attr:`model`

      :attr:`area`

      :attr:`off`

      :attr:`ic`

    Attributes:

      :attr:`model`

      :attr:`area`

      :attr:`off`

      :attr:`ic`

    """

    # Fixme: off doesn't fit in kwargs !

    alias = 'MESFET'
    prefix = 'Z'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    area = FloatKeyParameter('area')
    multiplier = IntKeyParameter('m')
    off = FlagParameter('off')
    ic = FloatPairKeyParameter('ic')

    ##############################################

    def __init__(self, name,
                 drain_node, gate_node, source_node,
                 **kwargs):

        pins = [Pin(self, 'drain', drain_node),
                Pin(self, 'gate', gate_node),
                Pin(self, 'source', source_node),]

        super().__init__(name, pins, **kwargs)

    ##############################################

    @property
    def drain(self):
        return self.pins[0]

    ##############################################

    @property
    def gate(self):
        return self.pins[1]

    ##############################################

    @property
    def source(self):
        return self.pins[2]

####################################################################################################

class Mosfet(FourPinElement):

    """This class implements a Metal Oxide Field Effect Transistor.

    Spice syntax::

         MXXXXXXX nd ng ns nb mname <m=val> <l=val> <w=val>
         + <ad=val> <as=val> <pd=val> <ps=val> <nrd=val>
         + <nrs=val> <off> <ic=vds,vgs,vbs> <temp=t>

    Keyword Parameters:

      :attr:`model`

      :attr:`multiplier`
         alias `m`

      :attr:`length`
         alias `l`

      :attr:`width`
         alias `w`

      :attr:`drain_area`
          alias `ad`

      :attr:`source_area`
          alias `as`

      :attr:`drain_perimeter`
          alias `pd`

      :attr:`source_perimeter`
          alias `ps`

      :attr:`drain_number_square`
          alias `nrd`

      :attr:`source_number_square`
          alias `nrs`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`
         alias `temp`

    Attributes:

      :attr:`model`

      :attr:`multiplier`

      :attr:`length`

      :attr:`width`

      :attr:`drain_area`

      :attr:`source_area`

      :attr:`drain_perimeter`

      :attr:`source_perimeter`

      :attr:`drain_number_square`

      :attr:`source_number_square`

      :attr:`off`

      :attr:`ic`

      :attr:`temperature`

    """

    # Fixme: off doesn't fit in kwargs !

    alias = 'MOSFET'
    prefix = 'M'

    model = ModelPositionalParameter(position=0, key_parameter=True)
    multiplier = IntKeyParameter('m')
    length = FloatKeyParameter('l', unit=U_m)
    width = FloatKeyParameter('w', unit=U_m)
    drain_area = FloatKeyParameter('ad')
    source_area = FloatKeyParameter('as')
    drain_perimeter = FloatKeyParameter('pd')
    source_perimeter = FloatKeyParameter('ps')
    drain_number_square = FloatKeyParameter('nrd')
    source_number_square = FloatKeyParameter('nrs')
    off = FlagParameter('off')
    ic = FloatTripletKeyParameter('ic')
    temperature = FloatKeyParameter('temp', unit=U_Degree)

    ##############################################

    def __init__(self, name,
                 drain_node, gate_node, source_node, substrate_node,
                 **kwargs):

        pins = [Pin(self, 'drain', drain_node),
                Pin(self, 'gate', gate_node),
                Pin(self, 'source', source_node),
                Pin(self, 'substrate', substrate_node), # bulk
        ]

        super().__init__(name, pins, **kwargs)

    ##############################################

    @property
    def drain(self):
        return self.pins[0]

    ##############################################

    @property
    def gate(self):
        return self.pins[1]

    ##############################################

    @property
    def source(self):
        return self.pins[2]

    ##############################################

    @property
    def substrate(self):
        return self.pins[3]

####################################################################################################

class TransmissionLine(TwoPortElement):

    """This class implements a lossless transmission line.

    Spice syntax::

        TXXXXXXX N1 N2 N3 N4 Z0=VALUE <TD=VALUE> <F=FREQ <NL=NRMLEN>>

    where TD or F, NL must be specified.

    Keyword Parameters:

      :attr:`impedance`
         alias:`Z0`

      :attr:`time_delay`
         alias:`TD`

      :attr:`frequency`
         alias:`F`

      :attr:`normalized_length`
         alias:`NL`

    Attributes:

      :attr:`impedance`

      :attr:`time_delay`

      :attr:`frequency`

      :attr:`normalized_length`

    Note: Either time_delay or frequency must be given.

    """

    alias = 'TransmissionLine'
    prefix = 'T'

    impedance = FloatKeyParameter('Z0', default=50, unit=U_Ω)
    time_delay = FloatKeyParameter('TD', unit=U_s)
    frequency = FloatKeyParameter('F', unit=U_Hz)
    normalized_length = FloatKeyParameter('NL')

    ##############################################

    def __init__(self, name,
                 input_node_plus, input_node_minus,
                 output_node_plus, output_node_minus,
                 *args, **kwargs):

        # check: ^ xor, & bitwise and
        if not (('time_delay' in kwargs) ^
                (('frequency' in kwargs) & ('normalized_length' in kwargs))):
            raise NameError('Either TD or F, NL must be specified')

        super().__init__(name,
                         output_node_plus, output_node_minus,
                         input_node_plus, input_node_minus, # Fixme: inverted inputs
                         *args, **kwargs)
