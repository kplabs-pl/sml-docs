EGSE Host
=========

.. toctree::
    :maxdepth: 1

    egse_host/dhcp_server
    egse_host/tftp_server

**EGSE Host** acts as gateway to single subscribed Board. When subscription becomes active, user gains access to dedicated machine connected to Board. That machine provides tools to control Board in terms of power control, accessing telemetry readouts and DPU boot memories. EGSE Host connects to Board using interfaces like JTAG, Ethernet, and UART. With these interfaces user can control full boot process of DPU and communicate with it.

Within EGSE Host, customer has full permission and can tune environment as they see fit by installing additional software or tuning configuration of pre-installed one.
