Setting up VPN connection
=========================

Prerequisites
-------------

* Active subscription within Smart Mission Lab system
* OpenVPN installed on your computer

Getting OpenVPN configuration file
-----------------------------------

Customers can download OpenVPN configuration from Smart Mission Lab website.

1. Go to Subscriptions page of your account on Smart Mission Lab website (https://sml.kplabs.space/subscriptions).
2. Click :menuselection:`Download VPN configuration` link and save downloaded file.

   .. image:: images/subscription_download_vpn_config.png

.. note::

    If :menuselection:`Download VPN configuration` link isn't active, your subscription is still in preparation. Wait for a while and try again later.

Connecting to VPN
-----------------

Exact steps needed to connect to VPN depends on operating system and OpenVPN client used. Follow steps in section matching your setup.

.. note:: SML supports only one connection per-customer at the same time.

Windows with OpenVPN GUI
++++++++++++++++++++++++

1. Using context menu of OpenVPN GUI icon in notification area select :menuselection:`Import --> Import file..` option.

   .. image:: images/openvpn_gui_import.png

2. After importing connection file, establish connection using :menuselection:`Connect` (only one connection configured) or :menuselection:`<configuration name> --> Connect` (multiple connections configured) option.

   .. image:: images/openvpn_gui_connect.png


3. OpenVPN GUI status window will be visible while connecting to SML server and close automatically after success.

Linux with systemd-resolved
+++++++++++++++++++++++++++
Follow this steps if you are using Linux distribution with systemd-resolved

1. Install https://github.com/jonathanio/update-systemd-resolved using your distribution's package manager

   .. code-block:: shell-session

      my-machine:~$ sudo apt install openvpn-systemd-resolved

   .. note:: Exact package name and installation method might differ for your distribution. This tutorial uses names and paths from Debian 12.

2. Modify OpenVPN connection profile (downloaded from Smart Mission Lab website) by adding following lines at the end of file:

   .. code-block:: shell

      ...

      <tls-auth>
      ...
      </tls-auth>

      script-security 2
      up /etc/openvpn/update-systemd-resolved
      up-restart
      down /etc/openvpn/update-systemd-resolved
      down-pre

   .. note:: Verify that :file:`/etc/openvpn/update-systemd-resolved` points to existing file from ``update-systemd-resolved``. Different distributions might place it in different place.

3. Connect to Smart Mission Lab VPN

   .. vale off

   .. code-block:: shell-session
      :emphasize-lines: 4-10

      my-machine:~$ sudo openvpn <path to customer>.ovpn
      ...
      2025-03-03 09:51:40 net_addr_ptp_v4_add: 10.100.0.17 peer 10.100.0.18 dev tun0
      2025-03-03 09:51:40 /etc/openvpn/update-systemd-resolved tun0 1500 0 10.100.0.17 10.100.0.18 init
      <14>Mar  3 09:51:40 update-systemd-resolved: Link 'tun0' coming up
      <14>Mar  3 09:51:40 update-systemd-resolved: Adding IPv4 DNS Server 10.80.4.42
      <14>Mar  3 09:51:40 update-systemd-resolved: Adding IPv4 DNS Server 10.80.4.42
      <14>Mar  3 09:51:40 update-systemd-resolved: Adding DNS Search Domain vpn.sml.kplabs.space
      <14>Mar  3 09:51:40 update-systemd-resolved: SetLinkDNS(4 2 2 4 10 80 4 42 2 4 10 80 4 42)
      <14>Mar  3 09:51:40 update-systemd-resolved: SetLinkDomains(4 1 vpn.sml.kplabs.space false)
      2025-03-03 09:51:40 net_route_v4_add: 10.80.4.40/29 via 10.100.0.18 dev [NULL] table 0 metric -1
      2025-03-03 09:51:40 net_route_v4_add: 10.80.4.16/29 via 10.100.0.18 dev [NULL] table 0 metric -1
      2025-03-03 09:51:40 net_route_v4_add: 10.80.4.56/29 via 10.100.0.18 dev [NULL] table 0 metric -1
      2025-03-03 09:51:40 net_route_v4_add: 10.80.16.128/27 via 10.100.0.18 dev [NULL] table 0 metric -1
      2025-03-03 09:51:40 Initialization Sequence Completed
      ```

   .. vale on

   Highlighted lines indicate that systemd-resolved configuration now uses Smart Mission Lab DNS server.
