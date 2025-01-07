Access SMB (Samba) shares
=========================

A bit of background
-------------------
EGSE Host runs SMB server that by default exposes several shares which you can use to exchange files between customer's machine and EGSE Host.

SMB requires password that you must setup before first use.

Set-up password
---------------
#. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine$ ssh customer@egse-my-egse.egse.sml.lan
        customer@egse-my-egse:~$

#. Run ``sudo smbpasswd -a customer`` to set password

   .. code-block:: shell-session

      customer@egse-753gf3hhrkivm:~$ sudo smbpasswd -a customer
      New SMB password:
      Retype new SMB password:
      Added user customer.

Access shares (Windows)
-----------------------
#. Open Windows Explorer
#. In address bar type ``\\egse-<id>.egse.vpn.sml.kplabs.space`` and press Enter
#. Enter credentials
#. Enter any of the listed shares to transfer files


Access shares (Ubuntu)
----------------------
#. Open Files
#. On left panel click ``+ Other Locations``
#. On the bottom in the ``Connect to Server`` put address ``smb://egse-<id>.egse.vpn.sml.kplabs.space/<share>``
#. Click Connect
#. Enter credentials
#. Transfer files between share and local machine

Access shares (Linux terminal)
------------------------------
#. Open terminal
#. Create folder for mountpoint

   .. code-block:: shell-session

      local-machine:~$ sudo mkdir /media/smb

#. Mount share into folder created in previous step

   .. code-block:: shell-session

      local-machine:~$ sudo mount -t cifs -o username=customer //egse-<id>-customer.egse.sml.lan/<share> /media/smb
      Password for customer@//egse-<id>-customer.egse.sml.lan/<share>:

#. Transfer files between share and local machine

See also
--------
* :doc:`/reference/egse_host/samba_shares`
