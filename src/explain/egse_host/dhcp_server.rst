DHCP server
===========

Overview
--------

EGSE Host runs custom DHCP server to provide IP address to Board. As it's common to use dynamic MAC address for Ethernet adapters on DPU, this server provides single, constant IP address. While not useful at all in general use case, in case of SML it makes possible for customer to access DPU using static IP address.

Assigned addresses
------------------

Table below lists IP addresses assigned by DHCP server

.. list-table::
    :header-rows: 1

    * - Board
      - IP address

    * - Antelope
      - * 172.20.200.100

    * - Leopard
      - * 172.20.200.100 (processing node 1)
        * 172.20.201.100 (processing node 2, if present)

systemd services
----------------

DHCP server is running as systemd service with name depending on type of connected Board.

.. list-table::
    :header-rows: 1

    * - Board
      - Service name

    * - Antelope
      - * ``sml-dhcp-server-net_device.service``
    * - Leopard
      - * ``sml-dhcp-server-net_device_pn1.service`` (processing node 1)
        * ``sml-dhcp-server-net_device_pn2.service`` (processing node 2, if present)
