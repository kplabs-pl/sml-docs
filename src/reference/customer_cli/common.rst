Common commands
===============

Telemetry access
----------------

* ``sml telemetry get``
    Return current telemetry data as pretty-printed table.

    ``sml`` reports each telemetry value with unique ID, name, raw and converted value.


Install Vivado Lab Edition
--------------------------
Due to licensing restrictions, KP Labs isn't allowed to install Vivado Lab Edition automatically. End user needs to download archive and install it manually. For convenience, KP Labs provides a command that will install Vivado Lab Edition from downloaded archive.


* ``sml install-vivado-lab [--agree-eula] [--sudo] <vivado-lab archive>``
    Runs Vivado Lab installer, installs it in predefined location and enables EGSE Host integration for Vivado Lab.

    * ``--agree-eula`` - Customer accepts EULA and automated installer will not ask for agreement interactively.
    * ``--sudo`` - Automatically restart installer as ``root``.
