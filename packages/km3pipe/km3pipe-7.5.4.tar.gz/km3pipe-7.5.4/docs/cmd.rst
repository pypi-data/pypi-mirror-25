Command Line Tools
==================

.. contents:: :local:

If you've installed KM3Pipe via ``pip``, you have access to some useful
command line utilities out of the box.

KM3Pipe
-------

Most of the commands have to be prefixed with ``km3pipe`` to avoid possible
nameclashes and also for an improved overview.
You can for example simply run ``km3pipe -h`` in your shell to see all available
commands:

.. command-output:: km3pipe --help
   :shell:

``update``
~~~~~~~~~~

The command ``km3pipe update [GIT_BRANCH]`` should be used to (once installed)
get latest version of KM3Pipe. If no git branch is specified, it will pull
the master branch, which always holds the stable releases.

If you want to try the newest features, pull the develop branch via
``km3pipe update develop``. This is 99.9% stable, since we always do our
experiments in ``feature/x`` branches. However, we might break it sometimes.
Have a look at our git repository to see what we're working on if you're
interested.

``runtable``
~~~~~~~~~~~~

To get a list of runs taken with one of the KM3NeT detectors, you can use
the ``runtable`` command.

The following command pulls the last 10 runs which matches the regular
expression ``PHYS``. In other words, you'll get a list of physics runs::

    km3pipe runtable -n 10 -s PHYS 14

An example output is::

    RUN	UNIXSTARTTIME	STARTTIME_DEFINED	RUNSETUPID	RUNSETUPNAME	T0_CALIBSETID	DATETIME
    848	3611	1465506000553	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-09 21:00:00.553000+00:00
    849	3612	1465506060554	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-09 21:01:00.554000+00:00
    850	3613	1465509600606	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-09 22:00:00.606000+00:00
    851	3614	1465509660607	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-09 22:01:00.607000+00:00
    852	3615	1465520400799	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 01:00:00.799000+00:00
    853	3616	1465520460800	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 01:01:00.800000+00:00
    854	3617	1465531200966	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 04:00:00.966000+00:00
    855	3618	1465531260967	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 04:01:00.967000+00:00
    856	3619	1465542000119	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 07:00:00.119000+00:00
    857	3620	1465542060119	Y	A01466427	PHYS.1606v1-TMP.HV-SFP.Power-XTRA.700ns		2016-06-10 07:01:00.119000+00:00


PipeInspector
-------------

PipeInspector is a tool to inspect different kinds of data formats used
within the KM3NeT collaboration. It utilises the KM3Pipe framework to
deal with data I/O and allows easy access to the stored information.

.. image:: _static/PipeInspector_Screenshot.png
    :alt: PipeInspector
    :width: 700
    :align: center

It is currently in an early alpha status, but already able to handle the
DAQ binary data, ROOT and Aanet-ROOT format.

If you installed KM3Pipe via `pip`, you'll be able to launch `pipeinspector`
directly from the terminal::

    pipeinspector /path/to/data/file.ext


.. _h5cli:

HDF5 CLI Utils
--------------

``tohdf``
~~~~~~~~~

Convert an aanet/root/evt/jpp file to hdf5.

Example::

    tohdf5 --aa-fmt=jevt_jgandalf some_jgandalf_file.aa.root

    $ tohdf5 --help
    Convert ROOT and EVT files to HDF5.

    Usage:
        tohdf5 [-o OUTFILE] [-n EVENTS] [-e NROWS] [--correct-zed] [--aa-format=<fmt>] [--aa-lib=<lib.so>] FILE...
        tohdf5 [-o OUTFILE] [-n EVENTS] [-e NROWS] [-j] [-s] [-l] FILE...
        tohdf5 (-h | --help)
        tohdf5 --version

    Options:
        --aa-format=<fmt>          tohdf5: Which aanet subformat ('minidst',
                                   'orca_recolns', 'gandalf',
                                   'generic_track') [default: None]
        --aa-lib-<lib.so>          tohdf5: path to aanet binary (for old versions which
                                   must be loaded via `ROOT.gSystem.Load()` instead
                                   of `import aa`)
        -h --help                  Show this screen.
        -j --jppy                  tohdf5: Use jppy (not aanet) for Jpp readout
        -l --with-timeslice-hits   Include timeslice-hits [default: False]
        -n EVENTS/RUNS             Number of events/runs.
        -o OUTFILE                 Output file.
        -s --with-summaryslices    Include summary slices [default: False]
        --correct-zed              Correc toffset in mc tracks (aanet) [default: False]
        -e --expected-rows NROWS   Approximate number of events.  Providing a
                                   rough estimate for this (100, 10000000, ...)
                                   will greatly improve reading/writing speed and
                                   memory usage. Strongly recommended if the
                                   table/array size is >= 100 MB. [default: 10000]


``calibrate``
~~~~~~~~~~~~~

Apply geometry and time calibration to an HDF5 file.

Example::

    calibrate km3net_jul13_90m_r1494.detx km3net_jul13_90m_muatm10T23.h5

    $ calibrate -h
    Apply geometry and time calibration from a DETX to an HDF5 file.

    Usage:
        calibrate DETXFILE HDF5FILE
        calibrate (-h | --help)
        calibrate --version

    Options:
        -h --help       Show this screen.


``hdf2root``
~~~~~~~~~~~~

Convert a HDF5 file to a plain ROOT file (requires ``rootpy`` + ``root_numpy``).

Example::

  hdf52root FOO.h5 BAR.h5

  $ hdf2root --help
  Convert HDF5 to vanilla ROOT.

  Usage:
       hdf2root FILES...
       hdf2root (-h | --help)

  Options:
      -h --help           Show this screen.


``ptdump`` (from PyTables)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspect the contents of a HDF5 file, walking through all the subgroups.

Read the `PyTables docs <http://www.pytables.org/usersguide/utilities.html#id1>`_ for more details.

Example output::

    ┌─[moritz@averroes ~/km3net/data ]
    └─╼ ptdump nueCC.h5
    / (RootGroup) ''
    /event_info (Table(121226,), shuffle, zlib(5)) ''
    /hits (Table(0,), shuffle, zlib(5)) ''
    /mc_hits (Table(0,), shuffle, zlib(5)) ''
    /mc_tracks (Table(242452,), shuffle, zlib(5)) ''
    /reco (Group) ''
    /reco/aa_shower_fit (Table(121226,), shuffle, zlib(5)) ''
    /reco/dusj (Table(121226,), shuffle, zlib(5)) ''
    /reco/j_gandalf (Table(121226,), shuffle, zlib(5)) ''
    /reco/q_strategy (Table(121226,), shuffle, zlib(5)) ''
    /reco/reco_lns (Table(121226,), shuffle, zlib(5)) ''
    /reco/thomas_features (Table(121226,), shuffle, zlib(5)) ''


``h5info``
~~~~~~~~~~

Show some H5 metadata (KM3 H5 version, km3pipe version, etc).

Example::

    $ h5info km3net_jul13_90m_muatm50T655.km3_v5r1.JTE_r2356.root.0-499.h5
    format_version: b'4.1'
    km3pipe: b'7.1.2.dev'
    pytables: b'3.4.0'


    $ h5info --help

    Show the km3pipe etc. version used to write a H5 file.

    Usage:
      h5info FILE [-r]
      h5info (-h | --help)
      h5info --version

    Options:
      FILE        Input file.
      -r --raw    Dump raw metadata.
      -h --help   Show this screen.
