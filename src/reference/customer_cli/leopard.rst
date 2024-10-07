Leopard commands
================

Board-level commands
--------------------

* ``sml power on``
    Powers on Leopard board.

    Powering on brings up only Supervisor portion of Leopard and takes few seconds as ``sml`` is waiting for supervisor to report successful boot.

* ``sml power off``
    Powers off entire Leopard board including DPU.

Processing node power
---------------------

* ``sml pn1/pn2 power on [--nor-image nor1|nor2|nor3|tmr>] [<image>]``
    Powers on selected processing node (``pn1`` or ``pn2``).

    * ``--nor-image``
        Selects SPI flash chip to boot from. Default is ``tmr``.
    * ``image``
        Selects which Linux image bootloader shall load and boot. Defaults to ``0``.

    Optionally it can select which Linux image bootloader shall load and boot.

* ``sml pn1/pn2 power off``
    Powers off selected processing node (``pn1`` or ``pn2``).
