Create minimalist Vivado project
================================

Goal
----
The goal of this tutorial is to create minimalist Vivado project for Leopard that you can use for building Linux distribution.

A bit of background
-------------------
Building Linux distribution for Zynq UltraScale+ device (such as Leopard DPU) requires **hardware definition file** (``.xsa``). That file includes essential configuration such as:

* DDR memory
* Clocks
* Enabled peripherals
* I/O pins, in particular how peripherals connect to physical pins of chip
* Connectivity between Processing System (PS) and Programmable Logic (PL)

Vivado lets you to configure all these settings and export them in form of ``.xsa`` file. Simplest way to create Vivado project is by using **block design** which offers graphical way to layout IP cores, customize them and connect together.

Prerequisites
-------------
* AMD Vivado Design Suite

  * Leopard requires licensed Vivado (https://www.xilinx.com/products/design-tools/vivado.html) that enables working with Zynq UltraScale+ ``xczu9eg-ffvc900-1L-i``.
  * Enable support for Zynq UltraScale+ MPSoC during installation

    * During installation when selecting devices support make sure to select **Zynq** UltraScale+ MPSoC in SoC group. Just UltraScale+ is different family of devices.
    * Both 'Vitis' and 'Vivado' selections include Vivado. You can use either of them but using 'Vitis' installs additional tools.

  * This tutorial uses 2024.1 version. Other versions might also work correctly but it's possible that exact steps will be different.

Create project :tutorial-machine:`Vivado`
-----------------------------------------
.. note:: Leopard User Manual describes all configuration values used in these steps.

1. Start Vivado and create new project. In new project wizard select following options:

   * Project type: RTL Project

     * Select :menuselection:`Don't specify sources at this time`
     * Don't select :menuselection:`Project is an extensible Vitis platform`

   * Part: ``xczu9eg-ffvc900-1L-i``

2. Create top-level block design by using :menuselection:`Create Block Design` in Flow Navigator. Use ``top_bd`` as name.
3. In block design diagram editor add Zynq UltraScale+ MPSoC IP block.
4. Start customization of Zynq UltraScale+ MPSoC IP block by double-clicking on it.

   1. Go to I/O Configuration and set following options:

      * MIO Voltage Standard on all I/O Banks: LVCMOS18
      * :menuselection:`Low Speed --> Memory Interfaces --> QSPI`: Single, x1, **without** feedback clock
      * :menuselection:`Low Speed --> Memory Interfaces --> NAND`: Single Ready/busy on MIO10, Data strobe on MIO12
      * :menuselection:`Low Speed --> Memory Interfaces --> SD --> SD 1`: on MIO46..51, Slot Type SD 2.0, enable CD on MIO 45
      * :menuselection:`Low Speed --> I/O Peripherals --> UART --> UART0`: on MIO74..75, no modem signals
      * :menuselection:`Low Speed --> I/O Peripherals --> GPIO --> GPIO2 MIO`: on MIO52..77
      * :menuselection:`Low Speed --> I/O Peripherals --> I2C --> I2C 0`: on MIO66..67
      * :menuselection:`High Speed --> GEM --> GEM2`: on MDIO 52..53, enable MDIO2 on MIO76..77
      * :menuselection:`High Speed --> SATA`: enable SATA Lane0 on GT Lane0 and enable SATA Lane1 on GT Lane1

   2. Go to Clock Configuration and set following options:

      * :menuselection:`Input --> Input Reference Frequency --> PSS_REF_CLK`: 33.333 MHz (make sure it's set to this exact value)
      * :menuselection:`Input --> Input Reference Frequency --> GT Lane Reference frequency`: 125 MHz (make sure it's set to this exact value)
      * :menuselection:`Output --> Low Power Domain Clocks --> PL Fabric Clocks`: disable all clocks

   3. Go to DDR Configuration and set following options:

      * Requested Device Frequency: 800
      * Effective DRAM Bus Width: 64-bit
      * ECC: Enabled
      * Speed Bin: DDR4 1600K
      * DRAM Device Capacity: 8192 MBits
      * Row Address Count: 16
      * tRC: 50
      * tFAW: 30
      * Dual Rank: enabled
      * Data Mask and DBI: NO DM DBI RD WR
      * Parity: enabled

   4. Go to PS-PL Configuration and set following options:

      * :menuselection:`General --> Fabric Reset Enable`: Disable
      * :menuselection:`PS-PL Interfaces --> Master Interface`: Disable all interfaces

5. In Sources view select :menuselection:`Design Sources --> top_bd` and click :menuselection:`Create HDL Wrapper` in context menu. Use :menuselection:`Let Vivado manage wrapper and auto-update` option.
6. Click 'Generate Bitstream' in Flow Navigator to finalize design and generate outputs.
7. Export hardware by clicking :menuselection:`File --> Export --> Export Hardware`. Don't include bitstream. Save exported ``.xsa`` file in known place for next tutorials.

Summary
-------
In this tutorial you walked through creating minimalist Vivado project for Leopard. Configuration enables only minimal set of peripherals (UART, Ethernet and flash memories) and doesn't provide support of usage of Programmable Logic. In the next step you can use exported ``.xsa`` as base of building Linux distribution for Leopard.
