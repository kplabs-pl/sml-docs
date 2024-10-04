Dnsmasq
=======

Overview
--------
EGSE Host comes with preinstalled instance of ``dnsmasq`` (https://thekelleys.org.uk/dnsmasq/doc.html) that serves as TFTP server for Board along with DNS proxy.

TFTP server
-----------
Bootloader running on DPU can use TFTP server to fetch operating system files from EGSE Host. This approach is particularly useful during development, as there is no need to re-write persistent memory on each image change. Provided TFTP server is available at IP address of EGSE Host:

.. list-table::
    :header-rows: 1

    * - Board
      - TFTP server IP address

    * - Antelope
      - * 172.20.100.1
    * - Leopard
      - * 172.20.100.1 (processing node 1)
        * 172.20.101.1 (processing node 2, if present)

TFTP server gives access to files stored in ``/var/tftp`` directory. By default, server permits both reads and writes.

DNS proxy
---------
EGSE Host acts as DNS proxy for Board allowing it to resolve Internet domain names. DHCP server automatically provides necessary configuration to DPU, without any need for manual configuration.
