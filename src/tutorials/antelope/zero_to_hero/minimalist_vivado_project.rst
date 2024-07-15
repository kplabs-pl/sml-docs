Create minimalist Vivado project
================================

Goal
----
The goal of this tutorial is to create minimalist Vivado project for Antelope that you can use for building Linux distribution.

A bit of background
-------------------
Building Linux distribution for Zynq UltraScale+ device (such as Antelope DPU) requires **hardware definition file** (``.xsa``). That file includes essential configuration such as:

* DDR memory
* Clocks
* Enabled peripherals
* I/O pins, in particular how peripherals connect to physical pins of chip
* Connectivity between Processing System (PS) and Programmable Logic (PL)

Vivado lets you to configure all these settings and export them in form of ``.xsa`` file. Simplest way to create Vivado project is by using **block design** which offers graphical way to layout IP cores, customize them and connect together.

Prerequisites
-------------
* AMD Vivado Design Suite

  * Free Standard Edition can be download from https://www.xilinx.com/products/design-tools/vivado.html
  * Enable support for Zynq UltraScale+ MPSoC during installation

    * During installation when selecting devices support make sure to select **Zynq** UltraScale+ MPSoC in SoC group. Just UltraScale+ is different family of devices.
    * Both 'Vitis' and 'Vivado' selections include Vivado. You can use either of them but using 'Vitis' installs additional tools.

  * This tutorial uses 2024.1 version. Other versions might also work correctly but it's possible that exact steps will be different.

Create project
--------------
.. note:: Antelope User Manual describes all configuration values used in these steps.

1. Start Vivado and create new project. In new project wizard select following options:

   * Project type: RTL Project

     * Select 'Don't specify sources at this time'
     * Don't select 'Project is an extensible Vitis platform'

   * Part: ``xczu4cg-sfvc784-1L-i``

2. Create top-level block design by using 'Create Block Design' in Flow Navigator. Use ``top_bd`` as name.
3. In block design diagram editor add Zynq UltraScale+ MPSoC IP block.
4. Start customization of Zynq UltraScale+ MPSoC IP block by double-clicking on it.

   1. Go to I/O Configuration and set following options:

      * MIO Voltage Standard on all I/O Banks: LVCMOS18
      * Low Speed -> Memory Interfaces -> QSPI: Single, x4, **without** feedback clock
      * Low Speed -> Memory Interfaces -> NAND: Single Ready/busy on MIO10, Data strobe on MIO12
      * Low Speed -> I/O Peripherals -> UART -> UART0: on MIO46..47, no modem signals
      * Low Speed -> I/O Peripherals -> GPIO -> GPIO1 MIO: on MIO26..51
      * High Speed -> GEM -> GEM3: on MIO 64..75, enable MDIO3 on MIO76..77

   2. Go to Clock Configuration and set following options:

      * Input -> Input Reference Frequency -> PSS_REF_CLK: 33.3333 MHz
      * Output -> Low Power Domain Clocks -> PL Fabric Clocks: disable all clocks

   3. Go to DDR Configuration and set following options:

      * Requested Device Frequency: 1067
      * Effective DRAM Bus Width: 32-bit
      * ECC: Disabled
      * Speed Bin: DDR4 2133R
      * DRAM Device Capacity: 16384 MBits
      * Row Address Count: 17

   4. Go to PS-PL Configuration and set following options:

      * General -> Fabric Reset Enable: Disable
      * PS-PL Interfaces -> Master Interface: Disable all interfaces

5. In Sources view select Design Sources -> ``top_bd`` and click 'Create HDL Wrapper' in context menu. Use 'Let Vivado manage wrapper and auto-update' option.
6. Click 'Generate Bitstream' in Flow Navigator to finalize design and generate outputs.
7. Export hardware by clicking File -> Export -> Export Hardware. Don't include bitstream. Save exported ``.xsa`` file in known place for next tutorials.

Summary
-------
In this tutorial you walked through creating minimalist Vivado project for Antelope. Configuration enables only minimal set of peripherals (UART, Ethernet and flash memories) and doesn't provide support of usage of Programmable Logic. In the next step you can use exported ``.xsa`` as base of building Linux distribution for Antelope.
