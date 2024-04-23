Antelope commands
=================

Board-level commands
--------------------

* ``sml power on``
    Powers on Antelope board.

    Powering on brings up only Supervisor portion of Antelope and takes few seconds as ``sml`` is waiting for supervisor to report successful boot.

* ``sml power off``
    Powers off entire Antelope board including DPU.

DPU power
---------

* ``sml dpu power on``
    Powers on DPU.

    This only enables power to DPU and keeps it in reset.

* ``sml dpu power off``
    Powers off DPU.

DPU reset
---------
* ``sml dpu reset off [--boot-flash=<0|1>] [<image>]``
    Releases DPU from reset.

    ``--boot-flash`` parameter allows to select with SPI flash memory will be used to boot DPU. Default is 0.

    ``<image>`` (number between 0 and 7) selects which Linux image bootloader shall load and boot. Exact implementation depends on bootloader configuration. Refer to Antelope User Manual for more details.

* ``sml dpu reset on``
    Bring DPU into reset state. In this state, access to debug interface (using XSCT) is possible.

DPU boot flash
--------------

* ``sml dpu boot-flash read [--boot-flash=<0|1>] <offset> <size> <output>``
   Reads content of selected boot flash

   * ``--boot-flash=<0|1>``
       Select SPI flash chip to read from. Default is 0.
   * ``offset``
       Address of first byte to read.
   * ``size``
       Number of bytes to read.
   * ``output``
       Output file.

* ``sml dpu boot-flash write [--boot-flash=<0|1>] <offset> <data>``
    Writes data to selected boot flash

    * ``--boot-flash=<0|1>``
       Select SPI flash chip to write to. Default is 0.
    * ``offset``
       Address in flash where ``sml`` will write first byte from data file.
    * ``data``
       File with data to write.
