.. include:: abbreviation.txt
.. include:: project-links.txt

.. _overview-page:

==========
 Overview
==========

What is PySpice ?
-----------------

In short PySpice is an open source Python module which interface |Python|_ and the |Ngspice|_
circuit simulator, which is a clone of the famous `Spice <https://en.wikipedia.org/wiki/SPICE>`_
circuit simulator.

Mainly it permits:

 * to define a circuit, so called netlist,
 * to perform a simulation using |Ngspice|_,
 * to analyse the output using |Numpy|_ and |Matplotlib|_.

How is licensed PySpice ?
-------------------------

PySpice is licensed under `GPLv3 <https://www.gnu.org/licenses/quick-guide-gplv3.en.html>`_ therms.

Is there some papers or talks about PySpice ?
---------------------------------------------

You can look this talk `Circuit Simulation using Python
<https://www.slideshare.net/PoleSystematicParisRegion/pyparis2017-circuit-simulation-using-python-by-fabrice-salvaire>`_
given at the `PyParis 2017 <http://pyparis.org/>`_ conference (`PDF file
<https://pyspice.fabrice-salvaire.fr/pyparis-2017-talk.pdf>`_)

How to go further with PySpice ?
--------------------------------

The best way to know what you can do with PySpice and to learn it, is to look at the examples.

 * :ref:`Examples <examples-page>`
 * :ref:`PySpice Reference Manual <reference-manual-page>`
 * :ref:`Bibliography <bibliography-page>`

How PySpice can be used for learning ?
--------------------------------------

 * PySpice comes with many examples covering several topics.
 * PySpice features a documentation generator which permits to generate an HTML or PDF documentation

  | cf. supra for the documentation generator features

What are the platforms supported by PySpice ?
---------------------------------------------

PySpice runs on Linux, Windows 64-bit and Mac OS X.

How to install PySpice ?
------------------------

The procedure to install PySpice is described in the :ref:`Installation Manual <installation-page>`.

How PySpice differs from simulator like LTspice ?
-------------------------------------------------

 * PySpice and Ngspice are `Free Software <https://en.wikipedia.org/wiki/Free_software>`_ and thus open source,
 * PySpice don't feature a schematic editor (*) or GUI,
 * But it has the power of Python for data analysis,
 * And thus provide modern data analysis tools.
 * Moreover PySpice is feature unlocked due to its open design.

(*) However you can export netlist form Kicad to PySpice.

How can help a non GUI simulator ?
----------------------------------

Obviously, it is not an evident task to write a netlist and a tool like a schematic editor help to
visualise the circuit.  It is more obvious that tool like Circuit_macros or Tikz are complex and
need some practices.  However the learning curve is not worst than for a music instrument.

Another question is to discuss the possibility to simulate a real design, i.e. to integrate the
simulation in the EDA design process from the schematic to the PCB.  In general, it does not make
sense to simulate a real design, we will only simulate parts or models of a design to ensure the
real design is right.

In fact each tool has advantages and drawbacks which are often orthogonal.

We have discussed the main drawback, we will now look at the advantages:

 * Since it is code, you can describe completely your simulation project.  There is any actions that
   require to use a mouse to interact with the GUI.
 * And it can be easily versioned using a tool like Git.
 * If you work with an editor and a console in parallel, then you can easily and quickly change
   things and rerun the simulation, e.g. comment a diode or a capacitor to see what happen.  Using a
   GUI, this task would require many actions.
 * Thanks to a tool like the documentation generator, you can enrich your simulation with text,
   formulae and figure all in one.

Finally, it is possible to use both approaches all together ? The technical answer is yes we
can. For example the Modelica language uses a concept of annotations to describe the schema.  A
schematic editor like Kicad could be updated to interact closely with PySpice.

What is the benefits of PySpice over Ngspice ?
----------------------------------------------

 * You can steer your netlist and simulation using Python.

  | Which supersede Spice *parameters* and *expressions*.
  | Which make Monte Carlo simulation easier for example.

 * You can analyse the output using the Python Scientific packages.

  | Which supersede tools like TclSpice.

How PySpice is interfaced to Ngspice ?
--------------------------------------

 * PySpice can parse a Spice netlist and generate the equivalent Python code or instanciate it.
 * PySpice can generate a Spice netlist.
 * PySpice can send a simulation and read back the output using either the *server* or *shared* mode.

  | By default, PySpice use the server mode. Shared mode is only required when you need advanced features.

When using *shared* mode

 * PySpice permits to define external voltage and current source in Python (or even in C).
 * PySpice permits to get and send data during the simulation process.
 * |CFFI|_ is used to interface C to Python.

How is defined netlist ?
------------------------

 * Netlist is defined using an oriented object API,
 * But PySpice can also work with Spice netlist and import netlist from a schematic editor like |Kicad|_.

Can I run Ngspice using interpreter commands ?
----------------------------------------------

Thanks to the Ngspice shared library binding, you are not tied to the Oriented Object API of
PySpice.  You can run Ngspice as you did before and just upload the simulation output as Numpy
arrays.  For an example, look at the Ngspice shared examples.

How are handled Spice libraries ?
---------------------------------

 * PySpice features a libraries manager that scan a path for library files.
 * Libraries can be included as is using the *include* directive.
 * Subcircuit can be defined as Python class.

How are handled units ?
-----------------------

 * PySpice features a unit module that support the International System of Units.
 * Unit value can be defined using function shortcuts or a special syntax: e.g. :code:`kilo(1.2)`, :code:`1.2@u_kV`, :code:`1.2@u_mΩ`.

Which version of Python is required ?
-------------------------------------

PySpice requires Python 3 and the version 3.5 is recommended so as to benefits of the new *@* syntax
for units.

Which version of Ngspice is required ?
--------------------------------------

You should use the last version of Ngspice and take care it was compiled according to the Ngspice
manual, i.e. you should check somebody don't enabled experimental features which could break
PySpice, generate a wrong simulation, or produce bugs.

*Notice that Ngspice is not distributed with PySpice !*

Which flavour of Spice are supported ?
--------------------------------------

Up to now PySpice only support Ngspice. But PySpice could support easily any simulator providing an
API similar to Ngspice shared.

What should you aware of ?
--------------------------

Users should be aware of these advertisements:

 * Ngspice and PySpice are provided without any warranty.

  | Thus you must use it with care for real design.
  | Best is to cross check the simulation using an industrial grade simulator.

 * Ngspice is not compliant with industrial quality assurance processes.
 * Simulation is a design tool and not a perfect description of the real world.

How is coded PySpice ?
----------------------

PySpice is not the crappy code you can found on Github, but is rather coded carefully and use
advanced Python features like metaclass.

What are the features of the documentation generator ?
------------------------------------------------------

The documentation generator features:

 * intermixing of codes, texts, `LaTeX formulae <https://www.mathjax.org>`_, figures and plots
 * use the `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_ syntax for text
 * use the |Sphinx|_ generator
 * embed computations in the text content
 * generation of circuit schematics using |Circuit_macros|_
 * generation of figures using |Tikz|_
 * generation of plots using |Matplotlib|_

Somehow, it is similar to an `Jupyter notebook <https://ipython.org/notebook.html>`_, but it works
differently and provides specific features.
