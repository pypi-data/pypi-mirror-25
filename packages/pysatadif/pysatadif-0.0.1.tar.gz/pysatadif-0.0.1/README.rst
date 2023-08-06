Generate ADIF For Satellite QSOs
================================

Quick Installation
==================

::

    pip install git+https://github.com/jeremymturner/pysatadif.git


Upgrading
=========

::

    pip install --upgrade git+https://github.com/jeremymturner/pysatadif.git


Quick Usage
==========

::

$ pysatadif --satname SO-50 --timeon 0050 --qso N0CALL --qso N1CALL --qso N2CALL,DM00 --output adif


Full Usage
==========

::

usage: pysatadif [-h] -s SATNAME -n TIMEON [-f TIMEOFF] [-d QSODATE]
                 [-g MYGRID] [-r MYRIG] [-c OPERATOR] [-t TXPWR] -q QSO
                 [-o OUTPUT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SATNAME, --satname SATNAME
                        Satellites to track
  -n TIMEON, --timeon TIMEON
                        Start time of QSO (HHMMSS)
  -f TIMEOFF, --timeoff TIMEOFF
                        End time of QSO (HHMMSS)
  -d QSODATE, --qsodate QSODATE
                        QSO Date (YYYYMMDD)
  -g MYGRID, --mygrid MYGRID
                        My grid square
  -r MYRIG, --myrig MYRIG
                        My rig
  -c OPERATOR, --operator OPERATOR
                        My callsign
  -t TXPWR, --txpwr TXPWR
                        TX Power
  -q QSO, --qso QSO     QSO callsign and optionally grid (eg N0CALL,DN70)
  -o OUTPUT, --output OUTPUT
                        Output Format (text, adif)
  -v, --verbose         Print verbose debugging messages


Configuration
=============
Run pysatadif once. Then see $HOME/.pysatadif/defaults.json

You may configure your callsign, maidenhead grid square, radio, and 
transmitting power which will apply to all passes. You may override 
these at any time by using the command-line switches.
