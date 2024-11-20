Boot Linux over network
=======================

A bit of background
-------------------
During development of Linux distribution it's beneficial to load entire software over network. That removes the need for frequent and time-consuming writes to storage device.

Prerequisites
-------------
#. Distribution files

   * device tree - ``system.dtb``
   * Linux kernel image - ``Image``
   * Root file system wrapped in U-Boot headers - ``rootfs.cpio.gz.u-boot``

Steps
-----
#. Copy files to TFTP root on EGSE Host

   .. code-block:: shell-session

     user@local-machine:~$ scp system.dtb egse-<id>.egse.vpn.sml.kplabs.space:/var/tftp
     user@local-machine:~$ scp Image egse-<id>.egse.vpn.sml.kplabs.space:/var/tftp
     user@local-machine:~$ scp rootfs.cpio.gz.u-boot egse-<id>.egse.vpn.sml.kplabs.space:/var/tftp

#. Power on the device and stop in U-Boot shell

   .. code-block::

      U-Boot 2023.01 (Sep 21 2023 - 11:02:37 +0000)

      CPU:   ZynqMP
      Silicon: v3
      Chip:  zu9eg
      Board: Xilinx ZynqMP
      DRAM:  2 GiB (effective 16 GiB)
      PMUFW:  v1.1
      PMUFW:  No permission to change config object
      EL Level:       EL2
      Secure Boot:    not authenticated, not encrypted
      Core:  46 devices, 27 uclasses, devicetree: board
      MMC:   mmc@ff170000: 0
      Loading Environment from SPIFlash... SF: Detected s25fl512s with page size 256 Bytes, erase size 256 KiB, total 64 MiB
      *** Warning - bad CRC, using default environment

      In:    serial
      Out:   serial
      Err:   serial
      Bootmode: QSPI_MODE
      Reset reason:   EXTERNAL
      Net:
      ZYNQ GEM: ff0d0000, mdio bus ff0d0000, phyaddr 0, interface rgmii-id
      eth0: ethernet@ff0d0000
      scanning bus for devices...
      SATA link 0 timeout.
      SATA link 1 timeout.
      AHCI 0001.0301 32 slots 2 ports 6 Gbps 0x3 impl SATA mode
      flags: 64bit ncq pm clo only pmp fbss pio slum part ccc apst
      starting USB...
      No working controllers found
      Hit any key to stop autoboot:  0
      ZynqMP>

#. Obtain IP address

   .. code-block:: shell-session

      ZynqMP> dhcp
      BOOTP broadcast 1
      DHCP client bound to address 172.20.200.100 (37 ms)

#. Download device tree

   .. code-block:: shell-session

      ZynqMP> tftpboot ${fdt_addr_r} system.dtb
      Using ethernet@ff0d0000 device
      TFTP from server 172.20.200.1; our IP address is 172.20.200.100
      Filename 'system.dtb'.
      Load address: 0x40000000
      Loading: ###
               6.3 MiB/s
      done
      Bytes transferred = 39583 (9a9f hex)

#. Download root file system

   .. code-block:: shell-session

      ZynqMP> tftpboot ${ramdisk_addr_r} rootfs.cpio.gz.u-boot
      Using ethernet@ff0d0000 device
      TFTP from server 172.20.200.1; our IP address is 172.20.200.100
      Filename 'rootfs.cpio.gz.u-boot'.
      Load address: 0x2100000
      Loading: #################################################################
               #################################################################
               #################################################################
               #################################################################
               16.6 MiB/s
      done
      Bytes transferred = 38257813 (247c495 hex)

#. Download Linux kernel image

   .. code-block:: shell-session

      ZynqMP> tftpboot ${kernel_addr_r} Image
      Using ethernet@ff0d0000 device
      TFTP from server 172.20.200.1; our IP address is 172.20.200.100
      Filename 'Image'.
      Load address: 0x18000000
      Loading: #################################################################
               #################################################################
               #################################################################
               #################################################################
               16.4 MiB/s
      done
      Bytes transferred = 21379584 (1463a00 hex)

#. Boot Linux

   .. code-block:: shell-session

      ZynqMP> booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}
      ## Loading init Ramdisk from Legacy Image at 02100000 ...
         Image Name:   dpu-leopard-leopard-dpu.rootfs-2
         Created:      2011-04-05  23:00:00 UTC
         Image Type:   AArch64 Linux RAMDisk Image (uncompressed)
         Data Size:    38257749 Bytes = 36.5 MiB
         Load Address: 00000000
         Entry Point:  00000000
         Verifying Checksum ... OK
      ## Flattened Device Tree blob at 40000000
         Booting using the fdt blob at 0x40000000
      Working FDT set to 40000000
         Loading Ramdisk to 7973f000, end 7bbbb455 ... OK
         Loading Device Tree to 0000000079732000, end 000000007973ea9e ... OK
      Working FDT set to 79732000

      Starting kernel ...

      [    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
      [    0.000000] Linux version 6.1.30-xilinx-v2023.2 (oe-user@oe-host) (aarch64-oe-linux-gcc (GCC) 13.2.0, GNU ld (GNU Binutils) 2.41.0.20231213) #1 SMP Fri Sep 22 10:41:01 UTC 2023
      [    0.000000] Machine model: xlnx,zynqmp
      [    0.000000] earlycon: cdns0 at MMIO 0x00000000ff000000 (options '115200n8')
      ...

      KP Labs DPU 1.0 leopard-dpu ttyPS0

      leopard-dpu login:

Summary
-------
To boot Linux, you have to download three files from EGSE Host: kernel, root file system and device tree. U-Boot provides commands to download them over TFTP along with set of variables with memory addresses to store them. After downloading, you can boot Linux using ``booti`` command with addresses of kernel, root file system and device tree.
