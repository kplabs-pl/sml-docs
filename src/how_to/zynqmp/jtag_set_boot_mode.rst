Override boot mode using JTAG
=============================


A bit of background
-------------------
AMD Zynq UltraScale+ MPSoC devices boot by using firmware from storage selected by **boot mode** pins. When accessing hardware remotely (as is the case in Smart Mission Lab), it's possible to use JTAG access to override boot mode.

Prerequisites
-------------
1. Vivado Lab installed on EGSE Host

Steps
-----
1. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine$ ssh customer@egse-my-egse.egse.vpn.sml.kplabs.space
        customer@egse-my-egse:~$

2. Start Xilinx System Debugger (``xsdb``)

   .. code-block:: shell-session

        customer@egse-my-egse:~$ xsdb
        rlwrap: warning: your $TERM is 'xterm-256color' but rlwrap couldn't find it in the terminfo database. Expect some problems.

        ****** System Debugger (XSDB) v2024.1
        **** Build date : May 22 2024-19:19:01
            ** Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
            ** Copyright 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.


        xsdb%

3. Connect to locally running ``hw_server`` instance

   .. code-block:: shell-session

        xsdb% connect
        tcfchan#0
        xsdb%

4. Check if DPU is running and reachable by JTAG

   .. code-block:: shell-session

        xsdb% xsdb% targets
        1  PS TAP
            2  PMU
            3  PL
        5  PSU
            6  RPU
                7  Cortex-R5 #0 (Halted)
                8  Cortex-R5 #1 (Lock Step Mode)
            9  APU
            10  Cortex-A53 #0 (Running)
            11  Cortex-A53 #1 (Power On Reset)
5. Select ``PSU`` target

   .. code-block:: shell-session

        xsdb% targets -set -filter {name =~ "PSU"}
        xsdb%

6. Set alternative boot mode in ``boot_mode_user`` register

   .. code-block:: shell-session

        xsdb% rwr crl_apb boot_mode_user alt_boot_mode <new boot mode>

7. Enable usage of alternative boot mode

   .. code-block:: shell-session

        xsdb% rwr crl_apb boot_mode_user use_alt 1

8. Trigger system reset

   .. code-block:: shell-session

         xsdb% rst -system

9. DPU will reset and boot using firmware from storage selected by new boot mode
10. To revert to default boot mode set ``use_alt`` to 0 and reset device

    .. code-block:: shell-session

        xsdb% rwr crl_apb boot_mode_user use_alt 0
        xsdb% rst -system


References
----------
* ``BOOT_MODE_USER`` register in Zynq UltraScale+ Devices Register References (UG1087) (https://docs.amd.com/r/en-US/ug1087-zynq-ultrascale-registers/BOOT_MODE_USER-CRL_APB-Register)
