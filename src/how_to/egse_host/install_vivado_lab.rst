Install AMD Vivado Lab Edition
==============================

A bit of background
-------------------
Vivado Lab Edition enables debug access to DPUs connected to EGSE Host. Due to licensing restrictions, KP Labs can't pre-install Vivado Lab on EGSE Host. This guide describes how to install Vivado Lab on EGSE Host.

Steps
-----
1. Download Vivado Lab for Linux from AMD website.
2. Transfer downloaded file to EGSE Host.

   .. code-block:: shell-session

       my-machine:~$ scp Vivado_Lab_Lin_....tar.gz customer@egse-my-egse.egse.vpn.sml.kplabs.space:~/

3. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine:~$ ssh customer@egse-my-egse.egse.vpn.sml.kplabs.space
        customer@egse-my-egse:~$

4. Run ``sml install-vivado-lab`` command to automatically install Vivado Lab.

   .. code-block:: shell-session

        customer@egse-my-egse:~$ sudo sml install-vivado-lab ~/Vivado_Lab_Lin_....tar.gz
        Creating install directory...Success
        Extracting installer...Success
        Detecting Vivado Lab version...Vivado Lab 2024.1
        Do you accept Xilinx EULA? [(Y)es/(N)o/(P)rint]: y
        Do you accept Third Party EULA? [(Y)es/(N)o/(P)rint]: y
        Installing Vivado Lab...This is a fresh install.
        INFO Could not detect the display scale (hDPI).
            If you are using a high resolution monitor, you can set the insaller scale factor like this:
            export XINSTALLER_SCALE=2
            setenv XINSTALLER_SCALE 2
        Running in batch mode...
        Copyright (c) 1986-2022 Xilinx, Inc.  All rights reserved.
        Copyright (c) 2022-2024 Advanced Micro Devices, Inc.  All rights reserved.
        INFO  - User has accepted the EULAs.
        WARN  - Warning: you are running on an OS version that is not officially supported. AMD does not recommend installing on unsupported OSes.
        INFO  - Installing Edition: Vivado Lab Edition (Standalone)
        INFO  - Installation directory is /opt/xilinx/vivado_lab/versions


        Installing files, 99% completed. (Done)
        It took 1 minute to install files.
        INFO  - Installation completed successfully.

        Success
        Setting up paths...Success
        Starting hw_server.service...Success
        Removing extracted installer...Success


   .. note:: Even with automated installer, you need to agree to Vivado Lab license terms.

5. Verify installation by checking status of ``hw_server`` service.

   .. code-block:: shell-session

        customer@egse-my-egse:~$ systemctl status hw_server.service
        ● hw_server.service - AMD Xilinx Vivado Lab hw_server
               Loaded: loaded (/etc/systemd/system/hw_server.service; enabled; preset: enabled)
               Active: active (running) since Fri 2024-10-04 07:35:11 UTC; 1min 38s ago
               Docs: https://docs.xilinx.com/r/en-US/ug908-vivado-programming-debugging/Vivado-Lab-Edition
           Main PID: 30786 (hw_server)
               Tasks: 13 (limit: 18918)
               Memory: 4.3M
                   CPU: 416ms
               CGroup: /system.slice/hw_server.service
                       ├─30786 /bin/bash /opt/xilinx/vivado_lab/current/bin/hw_server
                       ├─30814 /bin/bash /opt/xilinx/vivado_lab/current/bin/loader -exec hw_server
                       └─30876 /opt/xilinx/vivado_lab/current/bin/unwrapped/lnx64.o/hw_server

6. If ``hw_server`` is running, you can connect to it locally from EGSE Host or from your workstation.
