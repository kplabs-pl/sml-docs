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

Windows with OpenVPN GUI
++++++++++++++++++++++++

1. Using context menu of OpenVPN GUI icon in notification area select :menuselection:`Import --> Import file...` option.

   .. image:: images/openvpn_gui_import.png

2. After importing connection file, establish connection using :menuselection:`Connect` (only one connection configured) or :menuselection:`<configuration name> --> Connect` (multiple connections configured) option.

   .. image:: images/openvpn_gui_connect.png


3. OpenVPN GUI status window will be visible while connecting to SML server and close automatically after success.

.. note:: SML supports only one connection per-customer at the same time.
