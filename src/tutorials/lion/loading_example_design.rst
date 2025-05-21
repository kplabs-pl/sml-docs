Loading example design
======================

Goal
----
In this tutorial, you will load example design into Kintex FPGA that's part of Lion DPU.


Prerequisites
-------------
* Example design from :ref:`tutorial_files`

  * Tutorial bitstream: :file:`Tutorials/Lion/lion_dpu.bit`

* AMD Vivado Lab Edition installed on EGSE Host

Steps :tutorial-machine:`EGSE Host`
-----------------------------------
#. Upload example bitstream to EGSE Host
#. Verify the bitstream is uploaded

   .. code-block:: shell-session

      customer@egse-host:~$ ls -lh lion_dpu.bit
      -rw-rw-r-- 1 customer customer 16M Feb 17 17:51 lion_dpu.bit

#. Power on the Lion

   .. code-block:: shell-session

      customer@egse-host:~$ sml power on
      Powering on...Success

#. Power on the DPU part of Lion

   .. code-block:: shell-session

      customer@egse-host:~$ sml dpu power on
      Powering on...Success

#. Start XSDB

   .. code-block:: shell-session

      customer@egse-host:~$ xsdb
      rlwrap: warning: your $TERM is 'xterm-256color' but rlwrap couldn't
      find it in the terminfo database. Expect some problems.

      ****** System Debugger (XSDB) v2024.2
      **** Build date : Oct 29 2024-10:16:47
          ** Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
          ** Copyright 2022-2024 Advanced Micro Devices, Inc. All Rights  Reserved.


      xsdb% connect
      tcfchan#0
      xsdb% targets
      1  xcku035
      xsdb%

#. Lower JTAG frequency to maximum supported value

   .. code-block:: shell-session

       xsdb% jtag targets 1
       xsdb% jtag frequency 1500000
       1500000

#. Load bitstream

   .. code-block:: shell-session

       xsdb% fpga lion_dpu.bit
       100%   15MB   0.2MB/s  01:24

#. Start ``minicom`` to observe output of test application

   .. code-block:: shell-session

      customer@egse-host:~$ minicom -D /dev/sml/lion-dpu-uart-1
      uart0
      uart0
      uart0

Summary
-------
In this tutorial, you've loaded the example design using JTAG and observed output of test application. If you are interested in details of that design, please contact Smart Mission Lab support or KP Labs representative directly.
