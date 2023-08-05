==============
PiPocketGeiger
==============

Radiation Watch Pocket Geiger Type 5 library for Raspberry Pi.

Usage
=====
::

    from PiPocketGeiger import RadiationWatch
    import time

    with RadiationWatch(24, 23) as radiationWatch:
        while 1:
            print(radiationWatch.status())
            time.sleep(5)


See GitHub repository for complete documentation.


