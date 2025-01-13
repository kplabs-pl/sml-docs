Security measures
=================
To keep your data secure, Smart Mission Lab uses several strategies:

* Network

  * Customers get access to Smart Mission Lab network through OpenVPN connection secured with TLS 1.3 and individual certificates.
  * Once connected, each customer has access to their own isolated network. No connectivity is possible between these networks.

* EGSE Hosts

  * SSH connection uses public key authentication. There is no need for any form of password sharing.
  * EGSE Host are available only for single customer at a time.
  * After the subscription ends, clean-up process removes all data from EGSE Host and Board.

* Telemetry collection

  * Customers have their own databases for telemetry storage.
  * Only owning customer can read data from telemetry storage using predefined Grafana instance.

* Physical access

  * Only authorized personnel have access to server room.
