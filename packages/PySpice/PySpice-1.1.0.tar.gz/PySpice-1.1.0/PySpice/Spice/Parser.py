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

####################################################################################################

"""This module implements a partial SPICE netlist parser.

See the :command:`cir2py` tool for an example of usage of the parser.

It would be difficult to implement a full parser for Ngspice since the syntax is mainly contextual.

"""

####################################################################################################

import logging
import os

####################################################################################################

from .BasicElement import SubCircuitElement, BipolarJunctionTransistor
from .ElementParameter import FlagParameter
from .Netlist import ElementParameterMetaClass, NPinElement, Circuit, SubCircuit

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PrefixData:

    """This class represents a device prefix."""

    ##############################################

    def __init__(self, prefix, classes):

        self.prefix = prefix
        self.classes = classes

        number_of_positionals_min = 1000
        number_of_positionals_max = 0
        has_optionals = False
        for element_class in classes:
            number_of_positionals = element_class.number_of_positional_parameters
            number_of_positionals_min = min(number_of_positionals_min, number_of_positionals)
            number_of_positionals_max = max(number_of_positionals_max, number_of_positionals)
            has_optionals = max(has_optionals, bool(element_class.optional_parameters))

        self.number_of_positionals_min = number_of_positionals_min
        self.number_of_positionals_max = number_of_positionals_max
        self.has_optionals = has_optionals

        self.multi_devices = len(classes) > 1
        self.npins = prefix in ('Q', 'X') # NPinElement, Q has 3 to 4 pins
        if self.npins:
            self.number_of_pins = None
        else:
            # Q and X are single
            self.number_of_pins = classes[0].number_of_pins

        self.has_flag = False
        for element_class in classes:
            for parameter in element_class.optional_parameters.values():
                if isinstance(parameter, FlagParameter):
                    self.has_flag = True

    ##############################################

    def __len__(self):
        return len(self.classes)

    ##############################################

    def __iter__(self):
        return iter(self.classes)

    ##############################################

    @property
    def single(self):
        if not self.multi_devices:
            return self.classes[0]
        else:
            raise NameError()

####################################################################################################

_prefix_cache = {}
for prefix, classes in ElementParameterMetaClass.__classes__.items():
    prefix_data = PrefixData(prefix, classes)
    _prefix_cache[prefix] = prefix_data
    _prefix_cache[prefix.lower()] = prefix_data

# for prefix_data in sorted(_prefix_cache.values(), key=lambda x: len(x)):
#     print(prefix_data.prefix,
#           len(prefix_data),
#           prefix_data.number_of_positionals_min, prefix_data.number_of_positionals_max,
#           prefix_data.has_optionals)

# Single:
# B 0 True
# D 1 True
# F 2 False
# G 1 False
# H 2 False
# I 1 False
# J 1 True
# K 3 False
# M 1 True
# S 2 False
# V 1 False
# W 3 False
# Z 1 True

# Two:
# E 0 1 False
# L 1 2 True

# Three:
# C 1 2 True
# R 1 2 True

# NPinElement:
# Q 1 1 True
# X 1 1 False

####################################################################################################

class Statement:

    """ This class implements a statement, in fact a line in a Spice netlist. """

    ##############################################

    def __init__(self, line, statement=None):

        self._line = line
        self._line.lower_case_statement(statement)

    ##############################################

    def __repr__(self):

        return '{} {}'.format(self.__class__.__name__, repr(self._line))

    ##############################################

    def value_to_python(self, x):

        if x:
            if str(x)[0].isdigit():
                return str(x)
            else:
                return "'{}'".format(x)
        else:
            return ''

    ##############################################

    def values_to_python(self, values):

        return [self.value_to_python(x) for x in values]

    ##############################################

    def kwargs_to_python(self, kwargs):

        return ['{}={}'.format(key, self.value_to_python(value))
                for key, value in kwargs.items()]

    ##############################################

    def join_args(self, args):

        return ', '.join(args)

####################################################################################################

class Comment(Statement):
    pass

####################################################################################################

class Title(Statement):

    """ This class implements a title definition. """

    ##############################################

    def __init__(self, line):

        super().__init__(line, statement='title')
        self._title = self._line.read_right_of('.title')

    ##############################################

    def __str__(self):
        return self._title

    ##############################################

    def __repr__(self):
        return 'Title {}'.format(self._title)

####################################################################################################

class Include(Statement):

    """ This class implements a include definition. """

    ##############################################

    def __init__(self, line):

        super().__init__(line, statement='include')
        self._include = self._line.read_right_of('.include')

    ##############################################

    def __str__(self):
        return self._include

    ##############################################

    def __repr__(self):
        return 'Include {}'.format(self._include)

    ##############################################

    def to_python(self, netlist_name):

        return '{}.include({})'.format(netlist_name, self._include) + os.linesep

####################################################################################################

class Model(Statement):

    """ This class implements a model definition.

    Spice syntax::

        .model mname type (pname1=pval1 pname2=pval2)

    """

    ##############################################

    def __init__(self, line):

        super().__init__(line, statement='mode')

        # Fixme
        parameters, dict_parameters = self._line.split_line('.model')
        self._name, self._model_type = parameters[:2]
        self._parameters = dict_parameters

    ##############################################

    @property
    def name(self):
        """ Name of the model """
        return self._name

    ##############################################

    def __repr__(self):

        return 'Model {} {} {}'.format(self._name, self._model_type, self._parameters)

    ##############################################

    def to_python(self, netlist_name):

        args = self.values_to_python((self._name, self._model_type))
        kwargs = self.kwargs_to_python(self._parameters)
        return '{}.model({})'.format(netlist_name, self.join_args(args + kwargs)) + os.linesep

    ##############################################

    def build(self, circuit):

        circuit.model(self._name, self._model_type, **self._parameters)

####################################################################################################

class SubCircuitStatement(Statement):

    """ This class implements a sub-circuit definition.

    Spice syntax::

        .SUBCKT name node1 ... param1=value1 ...

    """

    ##############################################

    def __init__(self, line):

        super().__init__(line, statement='subckt')

        # Fixme
        parameters, dict_parameters = self._line.split_line('.subckt')
        self._name, self._nodes = parameters[0], parameters[1:]

        self._statements = []

    ##############################################

    @property
    def name(self):
        """ Name of the sub-circuit. """
        return self._name

    @property
    def nodes(self):
        """ Nodes of the sub-circuit. """
        return self._nodes

    ##############################################

    def __repr__(self):

        text = 'SubCircuit {} {}'.format(self._name, self._nodes) + os.linesep
        text += os.linesep.join(['  ' + repr(statement) for statement in self._statements])
        return text

    ##############################################

    def __iter__(self):

        """ Return an iterator on the statements. """

        return iter(self._statements)

    ##############################################

    def append(self, statement):

        """ Append a statement to the statement's list. """

        self._statements .append(statement)

    ##############################################

    def to_python(self, ground=0):

        subcircuit_name = 'subcircuit_' + self._name
        args = self.values_to_python([subcircuit_name] + self._nodes)
        source_code = ''
        source_code += '{} = SubCircuit({})'.format(subcircuit_name, self.join_args(args)) + os.linesep
        source_code += SpiceParser.netlist_to_python(subcircuit_name, self, ground)
        return source_code

    ##############################################

    def build(self, circuit):

        subcircuit = SubCircuit(self._name, self._nodes)
        SpiceParser.build_netlist(subcircuit, self._statements)
        return subcircuit

####################################################################################################

class Element(Statement):

    """ This class implements an element definition.

    "{ expression }" are allowed in device line.

    """

    _logger = _module_logger.getChild('Element')

    ##############################################

    def __init__(self, line):

        super().__init__(line)

        line_str = str(line)
        # self._logger.debug(os.linesep + line_str)

        # Retrieve device prefix
        self._prefix = line_str[0]
        prefix_data = _prefix_cache[self._prefix]

        # Retrieve device name
        start_location = 1
        stop_location = line_str.find(' ')
        # Fixme: if stop_location == -1:
        self._name = line_str[start_location:stop_location]

        self._nodes = []
        self._parameters = []
        self._dict_parameters = {}

        # Read nodes
        if not prefix_data.npins:
            number_of_pins = prefix_data.number_of_pins
            if number_of_pins:
                self._nodes, stop_location = self._line.read_words(stop_location, number_of_pins)
        else: # Q or X
            if prefix_data.prefix == 'Q':
                self._nodes, stop_location = self._line.read_words(stop_location, 3)
                # Fixme: optional node
            else: # X
                args, stop_location = self._line.split_words(stop_location, until='=')
                self._nodes = args[:-1]
                self._parameters.append(args[-1]) # model name

        # Read positionals
        number_of_positionals = prefix_data.number_of_positionals_min
        if number_of_positionals and stop_location is not None: # model is optional
            self._parameters, stop_location = self._line.read_words(stop_location, number_of_positionals)
        if prefix_data.multi_devices and stop_location is not None:
            remaining, stop_location = self._line.split_words(stop_location, until='=')
            self._parameters.extend(remaining)

        if prefix_data.prefix in ('V', 'I') and stop_location is not None:
            # merge remaining
            self._parameters[-1] += line_str[stop_location:]

        # Read optionals
        if prefix_data.has_optionals and stop_location is not None:
            kwargs, stop_location = self._line.split_words(stop_location)
            for kwarg in kwargs:
                try:
                    key, value = kwarg.split('=')
                    self._dict_parameters[key] = value
                except ValueError:
                    if kwarg in ('off',) and prefix_data.has_flag:
                        self._dict_parameters['off'] = True
                    else:
                        self._logger.warn(line_str)
                        # raise NameError('Bad element line:', line_str)

        if prefix_data.multi_devices:
            for element_class in prefix_data:
                if len(self._parameters) == element_class.number_of_positional_parameters:
                    break
        else:
            element_class = prefix_data.single
        self.factory = element_class

        # Move positionals passed as kwarg
        to_delete = []
        for parameter in element_class.positional_parameters.values():
            if parameter.key_parameter:
                i = parameter.position
                self._dict_parameters[parameter.attribute_name] = self._parameters[i]
                to_delete.append(i)
        for i in to_delete:
            del self._parameters[i]

        self._logger.debug(os.linesep + self.__repr__())

    ##############################################

    @property
    def name(self):
        """ Name of the element """
        return self._name

    ##############################################

    def __repr__(self):

        return 'Element {0._prefix} {0._name} {0._nodes} {0._parameters} {0._dict_parameters}'.format(self)


    ##############################################

    def to_python(self, netlist_name, ground=0):

        nodes = []
        for node in self._nodes:
            if str(node) == ground:
                node = 0
            nodes.append(node)
        args = [self._name]
        if self._prefix != 'X':
            args += nodes + self._parameters
        else: # != Spice
            args += self._parameters + nodes
        args = self.values_to_python(args)
        kwargs = self.kwargs_to_python(self._dict_parameters)
        return '{}.{}({})'.format(netlist_name, self._prefix, self.join_args(args + kwargs)) + os.linesep

    ##############################################

    def build(self, circuit, ground=0):

        factory = getattr(circuit, self.factory.alias)
        nodes = []
        for node in self._nodes:
            if str(node) == ground:
                node = 0
            nodes.append(node)
        if self._prefix != 'X':
            args = nodes + self._parameters
        else: # != Spice
            args = self._parameters + nodes
        kwargs = self._dict_parameters
        message = ' '.join([str(x) for x in (self._prefix, self._name, nodes,
                                             self._parameters, self._dict_parameters)])
        self._logger.debug(message)
        factory(self._name, *args, **kwargs)

####################################################################################################

class Line:

    """ This class implements a line in the netlist. """

    ##############################################

    def __init__(self, text, line_range):

        text = str(text)
        for marker in ('$', ';', '//'):
            location = text.find(marker)
            if location != -1:
                break
        if location != -1:
            text = text[:location]
            comment = text[location:]
        else:
            comment = ''

        self._text = text
        self._comment = comment
        self._line_range = line_range

    ##############################################

    def __repr__(self):
        return '{0._line_range} {0._text}'.format(self)

    ##############################################

    def __str__(self):
        return self._text

    ##############################################

    def lower_case_statement(self, statement):

        if statement:
            self._text = self._text.replace(statement.upper(), statement.lower())

    ##############################################

    def read_right_of(self, text):

        return self._text[len(text):].strip()

    ##############################################

    def read_words(self, start_location, number_of_words):

        line_str = self._text
        number_of_words_read = 0
        words = []
        while number_of_words_read < number_of_words: # and start_location < len(line_str)
            stop_location = line_str.find(' ', start_location)
            if stop_location == -1:
                stop_location = None # read until end
            word = line_str[start_location:stop_location].strip()
            if word:
                number_of_words_read += 1
                words.append(word)
            if stop_location is None: # we should stop
                if number_of_words_read != number_of_words:
                    template = 'Bad element line, looking for word {}/{}:' + os.linesep
                    raise NameError(template.format(number_of_words_read, number_of_words) +
                                    line_str + os.linesep +
                                    ' '*start_location + '^')
            else:
                if start_location < stop_location:
                    start_location = stop_location
                else: # we have read a space
                    start_location += 1

        return words, stop_location

    ##############################################

    def split_words(self, start_location, until=None):

        line_str = self._text
        stop_location = None
        if until is not None:
            location = line_str.find(until, start_location)
            if location != -1:
                stop_location = location
                location = line_str.rfind(' ', start_location, stop_location)
                if location != -1:
                    stop_location = location
                else:
                    raise NameError('Bad element line, missing key? ' + line_str)

        line_str = line_str[start_location:stop_location]
        words = [x for x in line_str.split(' ') if x]

        return words, stop_location

    ##############################################

    def split_line(self, keyword):

        """ Split the line according to the following pattern::

            keyword parameter1 parameter2 ... key1=value1 key2=value2 ...

        Return the list of parameters and the dictionnary.
        """

        parameters = []
        dict_parameters = {}

        text = self._text[len(keyword):]
        parts = []
        for part in text.split():
            if '=' in part:
                left, right = [x for x in part.split('=')]
                parts += [left, '=', right]
            else:
                parts.append(part)
        i = 0
        i_stop = len(parts)
        while i < i_stop:
            if i + 1 < i_stop and parts[i + 1] == '=':
                key, value = parts[i], parts[i + 2]
                dict_parameters[key] = value
                i += 3
            else:
                parameters.append(parts[i])
                i += 1

        return parameters, dict_parameters

####################################################################################################

class SpiceParser:

    """ This class parse a Spice netlist file and build a syntax tree.

    Public Attributes:

      :attr:`circuit`

      :attr:`models`

      :attr:`subcircuits`

    """

    _logger = _module_logger.getChild('SpiceParser')

    ##############################################

    def __init__(self, path=None, source=None):

        # Fixme: empty source

        if path is not None:
            with open(str(path), 'r') as f:
                raw_lines = f.readlines()
        elif source is not None:
            raw_lines = source.split(os.linesep) # Fixme: other os
        else:
            raise ValueError

        lines = self._merge_lines(raw_lines)
        self._title = None
        self._statements = self._parse(lines)
        self._find_sections()

    ##############################################

    def _merge_lines(self, raw_lines):

        """Merge broken lines and return a new list of lines.

        A line starting with "+" continues the preceding line.
        """

        # Fixme: better using lines[-1] ?
        lines = []
        current_line = ''
        current_line_index = None
        for line_index, line in enumerate(raw_lines):
            if line.startswith('+'):
                current_line += ' ' + line[1:].strip()
            else:
                if current_line:
                    lines.append(Line(current_line, slice(current_line_index, line_index)))
                current_line = line.strip()
                current_line_index = line_index
        if current_line:
            lines.append(Line(current_line, slice(current_line_index, len(raw_lines))))
        return lines

    ##############################################

    def _parse(self, lines):

        """ Parse the lines and return a list of statements. """

        statements = []
        sub_circuit = None
        scope = statements
        for line in lines:
            # print(repr(line))
            text = str(line)
            lower_case_text = text.lower() # !
            if text.startswith('*'):
                scope.append(Comment(line))
            elif lower_case_text.startswith('.'):
                lower_case_text = lower_case_text[1:]
                if lower_case_text.startswith('subckt'):
                    sub_circuit = SubCircuitStatement(line)
                    statements.append(sub_circuit)
                    scope = sub_circuit
                elif lower_case_text.startswith('ends'):
                    sub_circuit = None
                    scope = statements
                elif lower_case_text.startswith('title'):
                    self._title = Title(line)
                    scope.append(self._title)
                elif lower_case_text.startswith('end'):
                    pass
                elif lower_case_text.startswith('model'):
                    model = Model(line)
                    scope.append(model)
                elif lower_case_text.startswith('include'):
                    scope.append(Include(line))
                else:
                    # options param ...
                    # .global
                    # .lib filename libname
                    # .param
                    # .func .csparam .temp .if
                    # { expr } are allowed in .model lines and in device lines.
                    self._logger.warn(line)
            else:
                element = Element(line)
                scope.append(element)

        return statements

    ##############################################

    def _find_sections(self):

        """ Look for model, sub-circuit and circuit definitions in the statement list. """

        self.circuit = None
        self.subcircuits = []
        self.models = []
        for statement in self._statements:
            if isinstance(statement, Title):
                if self.circuit is None:
                    self.circuit = statement
                else:
                    raise NameError('More than one title')
            elif isinstance(statement, SubCircuitStatement):
                self.subcircuits.append(statement)
            elif isinstance(statement, Model):
                self.models.append(statement)

    ##############################################

    def is_only_subcircuit(self):

        return bool(not self.circuit and self.subcircuits)

    ##############################################

    def is_only_model(self):

        return bool(not self.circuit and not self.subcircuits and self.models)

    ##############################################

    @staticmethod
    def build_netlist(netlist, statements):

        for statement in statements:
            if isinstance(statement, Include):
                netlist.include(str(statement))

        for statement in statements:
            if isinstance(statement, Element):
                statement.build(netlist, netlist.gnd)
            elif isinstance(statement, Model):
                statement.build(netlist)
            elif isinstance(statement, SubCircuit):
                subcircuit = statement.build()
                netlist.subcircuit(subcircuit)

    ##############################################

    def build_circuit(self, ground=0):

        circuit = Circuit(str(self._title))
        self.build_netlist(circuit, self._statements)
        return circuit

    ##############################################

    @staticmethod
    def netlist_to_python(netlist_name, statements, ground=0):

        source_code = ''
        for statement in statements:
            if isinstance(statement, Element):
                source_code += statement.to_python(netlist_name, ground)
            elif isinstance(statement, Include):
                pass
            elif isinstance(statement, Model):
                source_code += statement.to_python(netlist_name)
            elif isinstance(statement, SubCircuitStatement):
                source_code += statement.to_python(netlist_name)
            elif isinstance(statement, Include):
                source_code += statement.to_python(netlist_name)
        return source_code

    ##############################################

    def to_python_code(self, ground=0):

        ground = str(ground)

        source_code = ''

        if self.circuit:
            source_code += "circuit = Circuit('{}')".format(self._title) + os.linesep
        source_code += self.netlist_to_python('circuit', self._statements, ground)

        return source_code
