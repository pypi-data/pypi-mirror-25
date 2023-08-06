========
Overview
========


Python wrapper for strategies originally written in Fortran

* Free software: MIT license

Installation
============

::

    pip install axelrod-fortran


Usage
=====

Running a match:

.. code-block:: python

   >>> import axelrod_fortran as axlf
   >>> import axelrod as axl
   >>> p1 = axlf.Player('k31r')
   >>> p2 = axlf.Player('k33r')
   >>> match = axl.Match((p1, p2), turns=5)
   >>> match.play()
   [(C, C), (C, C), (C, D), (C, D), (C, C)]

Running an instance of Axelrod's second tournament:

.. code-block:: python

   >>> import axelrod_fortran as axlf
   >>> import axelrod as axl
   >>> players = [axlf.Player(name) for name in axlf.second_tournament_strategies]
   >>> print(len(players), "players")
   63 players
   >>> tournament = axl.Tournament(players, repetitions=1, turns=200)
   >>> results = tournament.play()
   >>> results.write_summary('summary.csv')
   >>> plot = axl.Plot(results)
   >>> plot.save_all_plots("second_tournament")


Contributing
============

Please see `CONTRIBUTING.rst` for details about installing for development and
running the test suite.

Changelog
=========

v0.2.0 (2017-07-30)
-------------------

* Identify strategy K74R as participating in the second tournament, written
  by Edward Friedland and ranked at 61

`All changes between v0.1.0 and this release
<https://github.com/Axelrod-Python/axelrod-fortran/compare/v0.1.0...v0.2.0>`_

v0.1.0 (2017-07-29)
-------------------

* Player class to wrap a fortran strategy function into the axelrod library
* Characteristics dict with details of stochasticity, author and original
  ranking for each function
* Pre-built lists for all strategies and strategies which participated in
  Axelrod's second tournament


