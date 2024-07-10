Enable programmable logic support
=================================


Goal
----
This tutorial you will
    - Enable programmable logic support in the Antelope DPU
    - Build bitstream with two UART peripherals connected together

Prerequisites
-------------
* Base Antelope DPU project
* Base Yocto project for Antelope DPU
* EGSE Host prepared to boot Antelope DPU from network

Enable programmable logic support
---------------------------------
1. Open Antelope DPU project in Vivado
2. Modify Zynq UltraScale+ block

   * Enable PL to PS interrupts ``IRQ0[0-7]``
   * Enable PS to PL Master interface ``AXI HPM0 FPD``
   * Enable PL fabric clock ``PL0``
   * Enable Fabric Reset Enable
   * Set Number of Fabric Resets to 1
3. In ``top_bd`` block design connect ``maxihpm0_fpd_aclk`` to ``pl0_clk``
4. Open Zynq UltraScale+ IP block and export preset by selecting ``Presets`` -> ``Save configuration``

   * Use ``antelope-minimalistic-with-pl`` as preset name
   * Save to ``antelope-minimalistic-with-pl.tcl`` file

5. Generate bitstream
6. Export hardware without bitstream. Use ``antelope-minimalistic-pl-base.xsa`` for output file name.

Create 2xUART bitstream
-----------------------

1. Create new project in Vivado

   * Project type: RTL Project

     * Select 'Don't specify sources at this time'
     * Don't select 'Project is an extensible Vitis platform'

   * Part: ``xczu4cg-sfvc784-1L-i``
2. Create block design with name ``double_uart_bd``.
3. Place Zynq UltraScale+ IP block in the block design.
4. Open Zynq UltraScale+ IP customization and apply previously exported preset by selecting ``Presets`` -> ``Apply configuration`` and select ``antelope-minimalistic-with-pl.tcl`` file.
5. In ``double_uart_bd`` block design connect ``maxihpm0_fpd_aclk`` to ``pl0_clk``.
6. Place two AXI Uartlite IPs on block design
7. Cross-connect UARTs by connecting ``axu_uartlite1`` TX to ``axu_uartlite0`` RX and vice versa.
8. Click ``Run connection automation`` and let Vivado instantiate necessary interconnects and resets.
9. Add ``Concat`` IP block
10. Connect ``dout`` pin of ``Concat`` block to ``pl_ps_irq`` pin of Zynq UltraScale+ block
11. Connect ``interrupt`` pin of ``axi_uartlite0`` to ``In0`` of ``Concat`` block
12. Connect ``interrupt`` pin of ``axi_uartlite1`` to ``In1`` of ``Concat`` block
13. Final block design should look like this:

    .. figure:: ./enable_pl_support/double_uart_bd.png
       :align: center
14. In Sources view select Design Sources -> ``double_uart_bd`` and click 'Create HDL Wrapper' in context menu. Use 'Let Vivado manage wrapper and auto-update' option.
15. Generate bitstream
16. Export hardware including bitstream to file ``antelope-double-uart.xsa``

Add double UART bitstream to Linux distribution
-----------------------------------------------
1. Add ``antelope-minimalistic-pl-base.xsa`` to ``sources/meta-local/recipes-bsp/hdf/external-hdf/`` directory.
2. Modify ``sources/meta-local/recipes-bsp/hdf/external-hdf_%.bbappend`` to use new XSA file.

   .. code-block::

        HDF_BASE = "file://"
        HDF_PATH = "antelope-minimalistic-pl-base.xsa"

3. Create new recipe ``sources/meta-local/recipes-example/bitstreams/double-uart.bb`` that will install bitstream with double UART.

   .. code-block::

        LICENSE = "CLOSED"

        inherit bitstream

        SRC_URI += "file://antelope-double-uart.xsa"
        BITSTREAM_HDF_FILE = "${WORKDIR}/antelope-double-uart.xsa"

4. Add ``antelope-double-uart.xsa`` to ``sources/meta-local/recipes-example/bitstreams/double-uart/`` directory.
5. Create append for ``core-image-minimal`` recipe

   .. code-block:: shell-session

        machine:~/antelope-linux-1$ recipetool newappend ./sources/meta-local/ core-image-minimal
        NOTE: Starting bitbake server...
        WARNING: The ZynqMP pmu-rom is not enabled, qemu may not be able to emulate a ZynqMP system without it. To enable this you must add 'xilinx' to the LICENSE_FLAGS_ACCEPTED to indicate you accept the software license.
        Loading cache: 100% |#############################################################################################################################################################################| Time: 0:00:00
        Loaded 2030 entries from dependency cache.
        Parsing recipes: 100% |###########################################################################################################################################################################| Time: 0:00:00
        Parsing of 1071 .bb files complete (1069 cached, 2 parsed). 2032 targets, 364 skipped, 0 masked, 0 errors.
        WARNING: No bb files in default matched BBFILE_PATTERN_meta-kp-classes '^~/antelope-linux-1/sources/meta-kp-classes/meta-kp-classes/'

        Summary: There was 1 WARNING message.
        ~/antelope-linux-1/sources/meta-local/recipes-core/images/core-image-minimal.bbappend created
6. Add new packages into Linux image by editing ``sources/meta-local/recipes-core/images/core-image-minimal.bbappend``

   .. code-block::

        IMAGE_INSTALL += "\
            fpga-manager-script \
            double-uart \
        "

7. Build firmware and image

    .. code-block:: shell-session

        machine:~/antelope-linux-1$ bitbake core-image-minimal bootbin-firmware boot-script-pins virtual/kernel device-tree

8. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/antelope-linux-1$ mkdir ./egse-host-transfer
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/bootbins/boot-firmware.bin ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/u-boot-scripts/boot-script-pins/boot-pins.scr ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/system.dtb ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/Image ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/core-image-minimal-antelope.rootfs.cpio.gz.u-boot ./egse-host-transfer/

9. Transfer content of ``egse-host-transfer`` directory to EGSE Host and place it in ``/var/tftp/tutorial`` directory

Loading double UART bitstream on DPU
------------------------------------

1. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 30M
       -rw-rw-r-- 1 customer customer  22M Jul 10 11:14 Image
       -rw-rw-r-- 1 customer customer 1.6M Jul 10 11:14 boot-firmware.bin
       -rw-rw-r-- 1 customer customer 2.8K Jul 10 11:14 boot-pins.scr
       -rw-rw-r-- 1 customer customer  16M Jul 10 11:14 core-image-minimal-antelope.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer  37K Jul 10 11:14 system.dtb

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``core-image-minimal-antelope.rootfs.cpio.gz.u-boot`` shall be about ~20MB)

2. Power on Antelope

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml power on
       Powering on...Success

3. Power on DPU

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml dpu power on
       Powering on...Success

4. Write boot firmware to DPU boot flash

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml dpu boot-flash write 0 /var/tftp/tutorial/boot-firmware.bin
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 43.1 MB/s
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 383.9 kB/s
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 13.1 kB/s

5. Write U-Boot boot script to DPU boot flash

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml dpu boot-flash write 0x4E0000 /var/tftp/tutorial/boot-pins.scr
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 63.9 MB/s

8. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/antelope-dpu-uart

    Leave this terminal open and get back to SSH connection used in previous steps.

9. Release DPU from reset

   .. code-block:: shell-session

      customer@egse-host:~$ sml dpu reset off 7

10. DPU boot process should be visible in ``minicom`` terminal
11. Log in to DPU using ``root`` user

    .. code-block::

      antelope login: root
      root@antelope:~#

12. Load double UART bitstream

    .. code-block::

        root@antelope:~# fpgautil -o /lib/firmware/double-uart/overlay.dtbo
        [   17.334051] fpga_manager fpga0: writing double-uart/bitstream.bit.bin to Xilinx ZynqMP FPGA Manager
        [   17.478795] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/firmware-name
        [   17.488941] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/resets
        [   17.498582] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /__symbols__/afi0
        [   17.508081] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /__symbols__/axi_uartlite_0
        [   17.518445] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /__symbols__/axi_uartlite_1
        [   17.532846] a0000000.serial: ttyUL0 at MMIO 0xa0000000 (irq = 45, base_baud = 0) is a uartlite
        [   17.543564] uartlite a0000000.serial: Runtime PM usage count underflow!
        [   17.553041] a0010000.serial: ttyUL1 at MMIO 0xa0010000 (irq = 46, base_baud = 0) is a uartlite
        [   17.563853] uartlite a0010000.serial: Runtime PM usage count underflow!
        root@antelope:~#

    .. note:: Despite warnings UARTs in bitstream will still function correctly

13. Verify presence of two new UART devices

    .. code-block:: shell-session

        root@antelope:~# ls -l /dev/ttyUL*
        crw-rw----    1 root     dialout   204, 187 Sep 20 11:23 /dev/ttyUL0
        crw-rw----    1 root     dialout   204, 188 Sep 20 11:23 /dev/ttyUL1

14. Start receiving data from ``/dev/ttyUL0`` in background

    .. code-block:: shell-session

        root@antelope:~# cat /dev/ttyUL0 &

    ``cat`` process will be running in background allowing you to enter another command in the same terminal. Output from ``cat`` (data received from UART) and your commands will mix in terminal.

15. Write something to second UART:

    .. code-block:: shell-session

        root@antelope:~# echo "Hello from UART1" > /dev/ttyUL1
        Hello from UART1
        root@antelope:~#

    Text ``Hello from UART1`` is coming from ``cat`` running in background.

Summary
-------
In this tutorial, you enabled usage of Programmable Logic part of Zynq UltraScale+ device. As an example, you added bitstream with two UARTs connected together. After rebuilding Yocto project, you used FPGA Manager to load bitstream dynamically and used newly added devices.
