Accessing the EGSE Host via SSH
===============================

Goal
----
The goal of this tutorial is access EGSE Host using SSH connection.

A bit of background
-------------------
You access EGSE Host using SSH connection. After connecting, you will be able to control your Board. Customer authenticates using **public key authentication** - built in feature in SSH that provides secure passwordless login without need to share any sensitive data. This authentication flow requires generation of **key pair**, uploading public key via User panel and using private key to authenticate.

This kind of access is popular with Git hosting services like GitHub or GitLab.

Prerequisites
-------------

* Active subscription within Smart Mission Lab system
* OpenVPN installed on your computer

  * For Linux: typically installed out-of-box
  * For Windows: OpenSSH is an optional feature

Generation of SSH key pair
--------------------------

.. note:: If you already have SSH key pair generated, you can skip this step.

1. Use ``ssh-keygen`` to generate key file. Accept default values by pressing Enter. Note that setting passphrase is optional (if you set passphrase, you will be asked for it every time key is used).

   .. code-block:: shell-session

      user@local-machine:~$ ssh-keygen
      Generating public/private ed25519 key pair.
      Enter file in which to save the key (/home/user/.ssh/id_ed25519):
      Created directory '/home/user/.ssh'.
      Enter passphrase (empty for no passphrase):
      Enter same passphrase again:
      Your identification has been saved in /home/user/.ssh/id_ed25519
      Your public key has been saved in /home/user/.ssh/id_ed25519.pub
      The key fingerprint is:
      SHA256:t5m75rzyyadx3NjNSc9Tm+t5tafOM5En+Z6qo0lcwNU user@local-machine
      The key's randomart image is:
      +--[ED25519 256]--+
      |           ..    |
      |        . .  E   |
      |         o       |
      |          .      |
      |        S ..   +.|
      |        ...= +*+O|
      |         o= + oXB|
      |        ooo*..o.O|
      |         B%*oo*X+|
      +----[SHA256]-----+

Upload SSH public key to Smart Mission Lab
------------------------------------------
#. Copy contents of :file:`/home/user/.ssh/id_ed25519.pub` file. This is your public key.
#. Login to Smart Mission Lab's User Panel and navigate to **SSH Keys** section.
#. Click **Add SSH Key** and fill the form

   * :menuselection:`Title` - descriptive name of public key
   * :menuselection:`Key` - paste contents of public key file

   .. image:: ./images/add_ssh_key.png
      :alt: Adding SSH key in User Panel

#. Click :menuselection:`Save` to add new public key.

.. note:: You can add many different public keys to your account. This is useful when you have multiple devices that you want to access.

Connect to EGSE Host using SSH
------------------------------
#. Login to Smart Mission Lab's User Panel and navigate to **Subscriptions** section.
#. Note the name in :menuselection:`DNS` - should be similar  to ``egse-<something>.egse.vpn.sml.kplabs.space``.
#. Use ``ssh`` command to connect to EGSE Host:

   .. code-block:: shell-session

     user@local-machine:~$ ssh customer@egse-<something>.egse.vpn.sml.kplabs.space.
     Warning: Permanently added 'egse-753gf3hhrkivm.egse.vpn.sml.kplabs.space' (ED25519) to the list of known hosts.
     Welcome to Ubuntu 23.04 (GNU/Linux 6.8.0-47-generic x86_64)
       _____   _  _      _
      / ___/  / \/ |    / /
      \__ \  /     |   / /
      __/ / / /|/| |  / /__
     /___/ /_/   |_| /____/

     SMART MISSION LAB
         by KP Labs

     Board: Antelope
     Run sml --help to see available commands
     Visit https://docs.sml.kplabs.space for documentation
     Visit https://sml.kplabs.space to manage your subscriptions
     Visit https://grafana.vpn.sml.kplabs.space to see telemetry readouts from your boards
     customer@egse-<something>:~$
