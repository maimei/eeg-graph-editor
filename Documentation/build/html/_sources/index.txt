.. GraphEditor documentation master file, created by
   sphinx-quickstart on Thu Sep 12 16:20:29 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GraphEditor 1.0 Documentation
=======================================

Welcome to GraphEditor's documentation!

============
Introduction
============

GraphEditor can be used to analyse arboreal graph structures. It visualizes the data hold in a .csv file.
It is both possible to visualize the correlations between the nodes of EEG graphs and phaseshift graphs.

To draw the graph the Python libraries Networkx and Matplotlib are used. 

For each of these graphs certain actions can be performed:

 * getting a node's degree
 * filtering the graph setting a lower and upper limit. All edges not within these limits are faded out.


========
Contents
========

.. toctree::
   :maxdepth: 2

   components.rst
   howtouse.rst
   referencedocumentation.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

