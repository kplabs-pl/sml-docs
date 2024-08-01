Deep-learning Processor Unit
============================

Goal
----

.. note:: TODO

A bit of background
-------------------

.. note:: TODO

Prerequisites
-------------
* Preset with Processing System configuration from :doc:`/tutorials/antelope/zero_to_hero/enable_pl_support`
* Yocto project with Programmable Logic support from :doc:`/tutorials/antelope/zero_to_hero/enable_pl_support`

Download Deep-learning Processor Unit repository :tutorial-machine:`Vivado`
---------------------------------------------------------------------------
1. On machine with Vivado create ``dpu-ip-repo`` directory.
2. Download DPU IP block from https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-system-integration.html#ip-and-reference-designs.

   * Use 'IP-only download' link for 'MPSoC & Kria K26' platform.

3. Unpack downloaded archive to ``dpu-ip-repo`` directory.

   * Make sure that after extracting, directory ``DPUCZDX8G_v4_1_0`` is directly in ``dpu-ip-repo``.

Create bitstream with Deep-learning Processor Unit :tutorial-machine:`Vivado`
-----------------------------------------------------------------------------
1. Start Vivado and create new project. In new project wizard select following options:

   * Project type: RTL Project

     * Select 'Don't specify sources at this time'
     * Don't select 'Project is an extensible Vitis platform'

   * Part: ``xczu4cg-sfvc784-1L-i``
2. Add DPU IP repository to project

   1. Open settings by clicking on 'Settings' in 'Flow Navigator'.
   2. Go to 'Project Settings' -> 'IP' -> 'Repository'.
   3. Add ``dpu-ip-repo`` directory to list of repositories.

      Vivado will show confirmation message and list 'Deep-learning Process Unit' as newly added IP.

3. Create top-level block design by using 'Create Block Design' in Flow Navigator. Use ``dpu_bd`` as name.
4. In block design diagram editor add Zynq UltraScale+ MPSoC IP block.
5. Start customization of Zynq UltraScale+ MPSoC IP block by double-clicking on it.

   1. Apply previously exported preset by selecting ``Presets`` -> ``Apply configuration`` and select ``antelope-minimalistic-with-pl.tcl`` file.

6. Add Deep-learning Process Unit IP block to block design.
7. Customize Deep-learning Process Unit block by double-clicking on it.

   1. On 'Arch' tab set 'Arch of DPU' to 'B1024'

8. Add AXI SmartConnect IP to block design
9. Customize AXI SmartConnect IP by double-clicking on it.

   1. Set 'Number of slave interfaces' to '3'
   2. Set 'Number of master interfaces' to '1'

10. Connect output pin ``dpu0_interrupt`` of DPU IP block to input pin ``pl_ps_irq`` of Zynq UltraScale+ MPSoC IP block.
11. Connect ``DPU0_M_AXI_DATA0`` output port to ``S00_AXI`` input port of AXI SmartConnect IP block.
12. Connect ``DPU0_M_AXI_DATA1`` output port to ``S01_AXI`` input port of AXI SmartConnect IP block.
13. Connect ``DPU0_M_AXI_INSTR`` output port to ``S02_AXI`` input port of AXI SmartConnect IP block.
14. Click 'Run connection automation' to fill out missing connections

    1. Enable all detected automations by checking checkbox for 'All automation'
    2. Select 'All automation' / 'dpuczdx8g_0' / 'dpu_2x_clk' and change settings:

       * Set 'Clock source' to '/zynq_ultra_ps_e_0/pl_clk1'

    3. Select 'All automation' / 'dpuczdx8g_0' / 'm_axi_dpu_aclk' and change settings:

       * Set 'Clock source' to '/zynq_ultra_ps_e_0/pl_clk0'

    3. Select 'All automation' / 'dpuczdx8g_0' / 'S_AXI' and change settings:

       * Set 'Clock source for driving Bridge IP' to '/zynq_ultra_ps_e_0/pl_clk0'
       * Set 'Clock source for driving Slave interface' to '/zynq_ultra_ps_e_0/pl_clk0'
       * Set 'Clock source for driving Master interface' to '/zynq_ultra_ps_e_0/pl_clk0'
15. Final block design should look like this:

    .. figure:: ./DPU/dpu_bd.png
       :align: center

       Block design with Deep-learning Processor Unit

14. In Sources view select Design Sources -> ``dpu_bd`` and click 'Create HDL Wrapper' in context menu. Use 'Let Vivado manage wrapper and auto-update' option.
15. Generate bitstream

   .. warning:: Compared to previous tutorials, generating bitstream might take significantly longer time.

16. Export hardware including bitstream to file ``antelope-dpu-bd.xsa``

Add Vitis layers to Yocto Project :tutorial-machine:`Yocto`
-----------------------------------------------------------
1. Clone ``meta-oe`` layer

   .. code-block:: shell-session

      machine:~/antelope-linux-1/build$ git clone -b nanbield https://git.openembedded.org/meta-openembedded ../sources/meta-openembedded

1. Clone Xilinx ``meta-vitis`` layer:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ git clone -b rel-v2024.1 https://github.com/Xilinx/meta-vitis.git ../sources/meta-vitis

2. Retrieve KP Labs-provided ``meta-kp-vitis-ai`` layer and save it as ``~/antelope-linux-1/sources/meta-kp-vitis-ai``.
3. Apply patches to ``meta-vitis`` that fix support for ``nanbield`` Yocto version

   .. code-block:: shell-session

       machine:~/antelope-linux-1/sources/meta-vitis$ git am ../meta-kp-vitis-ai/patches/*.patch
       Applying: Switch to nanbield
       Applying: bbappend to any glog version

4. Add layers to Yocto project:

   .. code-block:: shell-session

      machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-openembedded/meta-oe
      machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-openembedded/meta-python
      machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-vitis
      machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-vitis-ai

5. Change recipe providing ``opencl-icd`` by adding configuarion option to ``~/antelope-linux-1/build/conf/local.conf``.

   .. code-block::

       PREFERRED_PROVIDER_virtual/opencl-icd = "ocl-icd"

   .. note:: ``meta-vitis`` layer requires particular project configuration

Add Deep-learning Processor Unit bitstream to Linux image :tutorial-machine:`Yocto`
-----------------------------------------------------------------------------------
1. Create directory ``~/antelope-linux-1/sources/meta-local/recipes-example/bitstreams/antelope-dpu/`` and copy ``antelope-dpu-bd.xsa`` to it.
2. Create new recipe ``~/antelope-linux-1/sources/meta-local/recipes-example/bitstreams/antelope-dpu.bb`` that will install bitstream with double UART.

   .. code-block::

        LICENSE = "CLOSED"

        inherit bitstream

        SRC_URI += "file://antelope-dpu-bd.xsa"
        BITSTREAM_HDF_FILE = "${WORKDIR}/antelope-dpu-bd.xsa"

3. Create recipe append for kernel

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ recipetool newappend --wildcard-version ../sources/meta-local/ linux-xlnx

4. Create directory ``~/antelope-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx``.
5. Enable Xilinx DPU kernel driver module by creating file ``~/antelope-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx/xlnx-dpu.cfg`` with content

   .. code-block::

      CONFIG_XILINX_DPU=m

6. Enable kernel configuration fragment by adding it to ``~/antelope-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx/linux-xlnx_%.bbappend``

   .. code-block::

      FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

      SRC_URI += "file://xlnx-dpu.cfg"

3. Add new packages into Linux image by editing ``~/antelope-linux-1/sources/meta-local/recipes-core/images/core-image-minimal.bbappend``

   .. code-block::

        IMAGE_INSTALL += "\
            fpga-manager-script \
            double-uart \
            antelope-dpu \
            vart \
            xir \
            vitis-ai-library \
            kernel-module-xlnx-dpu \
        "

5. Build firmware and image

   .. code-block:: shell-session

       machine:~/antelope-linux-1$ bitbake core-image-minimal bootbin-firmware boot-script-pins virtual/kernel device-tree

6. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/antelope-linux-1$ mkdir -p ./egse-host-transfer
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/bootbins/boot-firmware.bin ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/u-boot-scripts/boot-script-pins/boot-pins.scr ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/system.dtb ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/Image ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/core-image-minimal-antelope.rootfs.cpio.gz.u-boot ./egse-host-transfer/

7. Transfer content of ``egse-host-transfer`` directory to EGSE Host and place it in ``/var/tftp/tutorial`` directory


Run model on Deep-learning Processor Unit :tutorial-machine:`EGSE Host`
-----------------------------------------------------------------------
1. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 30M
       -rw-rw-r-- 1 customer customer  22M Jul 10 11:14 Image
       -rw-rw-r-- 1 customer customer 1.6M Jul 10 11:14 boot-firmware.bin
       -rw-rw-r-- 1 customer customer 2.8K Jul 10 11:14 boot-pins.scr
       -rw-rw-r-- 1 customer customer  86M Jul 10 11:14 core-image-minimal-antelope.rootfs.cpio.gz.u-boot
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

12. Load DPU bitstream

   .. code-block::

        root@antelope:~# fpgautil -o /lib/firmware/antelope-dpu/overlay.dtbo

13. Verify that DPU instance is visible in system

    .. code-block:: shell-session

        root@antelope:~# xdputil query
        {
           "DPU IP Spec":{
              "DPU Core Count":1,
              "IP version":"v4.1.0",
              "enable softmax":"False"
           },
           "VAI Version":{
              "libvart-runner.so":"Xilinx vart-runner Version: 3.5.0-b7953a2a9f60e23efdfced5c186328dd144966,
              "libvitis_ai_library-dpu_task.so":"Advanced Micro Devices vitis_ai_library dpu_task Version: ,
              "libxir.so":"Xilinx xir Version: xir-b7953a2a9f60e23efdfced5c186328dd1449665c 2024-07-15-16:5,
              "target_factory":"target-factory.3.5.0 b7953a2a9f60e23efdfced5c186328dd1449665c"
           },
           "kernels":[
              {
                    "DPU Arch":"DPUCZDX8G_ISA1_B1024",
                    "DPU Frequency (MHz)":100,
                    "XRT Frequency (MHz)":100,
                    "cu_idx":0,
                    "fingerprint":"0x101000056010402",
                    "is_vivado_flow":true,
                    "name":"DPU Core 0"
              }
           ]
        }

.. note:: TODO Run model

Summary
-------

.. note:: TODO
