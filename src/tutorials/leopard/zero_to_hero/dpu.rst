Deep-learning Processor Unit
============================

Goal
----
In this tutorial you will
   - Build bitstream with Deep-learning Processor Unit
   - Include Vitis AI libraries in Yocto project

A bit of background
-------------------

Deep-learning Processor Unit is an IP Core provided by AMD that accelerates deep-learning inference on Xilinx FPGAs. It's part of Vitis AI library and facilities running models created with TensorFlow or PyTorch on FPGA. Integration of Deep-learning Processor Unit into Linux distribution follows similar steps as integration of other IP blocks (like double UART from :doc:`/tutorials/leopard/zero_to_hero/enable_pl_support`).

Prerequisites
-------------
* Preset with Processing System configuration from :doc:`/tutorials/leopard/zero_to_hero/enable_pl_support`
* Yocto project with Programmable Logic support from :doc:`/tutorials/leopard/zero_to_hero/enable_pl_support`

Download Deep-learning Processor Unit repository :tutorial-machine:`Vivado`
---------------------------------------------------------------------------
#. On machine with Vivado create :file:`dpu-ip-repo` directory.
#. Download DPU IP block from https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-system-integration.html#ip-and-reference-designs.

   * Use 'IP-only download' link for 'MPSoC & Kria K26' platform.
   * Note that DPU IP for Zynq UltraScale+ has version 3.0. That version works fine with Vitis AI 3.5 used in this tutorial.

#. Unpack downloaded archive to :file:`dpu-ip-repo` directory.

   * Make sure that after extracting, directory ``DPUCZDX8G_v4_1_0`` is directly in :file:`dpu-ip-repo`.

Create bitstream with Deep-learning Processor Unit :tutorial-machine:`Vivado`
-----------------------------------------------------------------------------
#. Start Vivado and create new project. In new project wizard select following options:

   * Project type: RTL Project

     * Select :menuselection:`Don't specify sources at this time`
     * Don't select :menuselection:`Project is an extensible Vitis platform`

   * Part: ``xczu9eg-ffvc900-1L-i``

#. Add DPU IP repository to project

   1. Open settings by clicking on :menuselection:`Settings` in :menuselection:`Flow Navigator`.
   2. Go to :menuselection:`Project Settings --> IP --> Repository`.
   3. Add :file:`dpu-ip-repo` directory to list of repositories.

      Vivado will show confirmation message and list :menuselection:`Deep-learning Process Unit` as newly added IP.

#. Create top-level block design by using :menuselection:`Create Block Design` in Flow Navigator. Use ``dpu_bd`` as name.
#. In block design diagram editor add Zynq UltraScale+ MPSoC IP block.
#. Start customization of Zynq UltraScale+ MPSoC IP block by double-clicking on it.

   1. Apply previously exported preset by selecting :menuselection:`Presets --> Apply configuration` and select :file:`leopard-minimalistic-with-pl.tcl` file.
   2. :menuselection:`PS-PL Configuration --> PS-PL Interfaces --> Master Interface --> AXI HPM0 FPD`: Set Data Width to 32.
   3. :menuselection:`PS-PL Configuration --> PS-PL Interfaces --> Slave Interface --> AXI LPD`: Set Data Width to 32.

#. Add "Processor System Reset" IP block to block design. In Block properties name it :menuselection:`rst_gen_pl_clk0`.
#. Connect :menuselection:`rst_gen_pl_clk0` IP block inputs:

   1. Connect ``slowest_sync_clk`` to ``pl_clk0`` output port of Zynq UltraScale+ MPSoC IP block.
   2. Connect ``ext_reset_in`` to ``pl_resetn0`` output port of Zynq UltraScale+ MPSoC IP block.

#. Add "Clocking Wizard" IP block to block design.
#. Customize Clocking Wizard block by double-clicking on it.

   1. In Clocking Options, set :menuselection:`Primitve` to "Auto"
   2. On Output Clocks:

      * Set :menuselection:`Port Name` of 'clk_out1' to 'clk_2x_dpu'
      * Set :menuselection:`clk_out1` to '200.000 MHz'
      * Enable :menuselection:`clk_out2`
      * Set :menuselection:`Port Name` of 'clk_out2' to 'clk_dpu'
      * Set :menuselection:`clk_out2` to '100.000 MHz'
      * Enable :menuselection:`Matched Routing` for both clocks
      * Enable :menuselection:`reset` input
      * Select :menuselection:`Reset Type` to 'Active Low'

#. Connect Clocking Wizard IP block inputs:

   1. Connect ``clk_in1`` to ``pl_clk0`` output port of Zynq UltraScale+ MPSoC IP block.
   2. Connect ``resetn`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_pl_clk0` IP block.

#. Add another "Processor System Reset" IP block to block design. In Block properties name it rst_gen_2x_dpu_clk.
#. Connect :menuselection:`rst_gen_2x_dpu_clk` IP block inputs:

   1. Connect ``slowest_sync_clk`` to ``clk_2x_dpu`` output port of Clocking Wizard IP block.
   2. Connect ``ext_reset_in`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_pl_clk0` IP block.

#. Add another "Processor System Reset" IP block to block design. In Block properties name it rst_gen_dpu_clk.
#. Connect :menuselection:`rst_gen_dpu_clk` IP block inputs:

   1. Connect ``slowest_sync_clk`` to ``clk_dpu`` output port of Clocking Wizard IP block.
   2. Connect ``ext_reset_in`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_pl_clk0` IP block.

#. Add Deep learning Processing Unit IP block to block design.
#. Customize Deep learning Process Unit block by double-clicking on it.

   1. On :menuselection:`Arch` tab set :menuselection:`Arch of DPU` to 'B1024'

#. Connect Deep learning Process Unit IP block inputs:

   1. Connect ``S_AXI`` to ``M_AXI_HPM0_FPD`` output port of Zynq UltraScale+ MPSoC IP block.
   2. Connect ``s_axi_aclk`` to ``pl_clk0`` output port of Zynq UltraScale+ MPSoC IP block.
   3. Connect ``s_axi_aresetn`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_pl_clk0` IP block.
   4. Connect ``dpu_2x_clk`` to ``clk_2x_dpu`` output port of Clocking Wizard IP block.
   5. Connect ``dpu_2x_resetn`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_2x_dpu_clk` IP block.
   6. connect ``m_axi_dpu_aclk`` to ``clk_dpu`` output port of Clocking Wizard IP block.
   7. Connect ``m_axi_dpu_aresetn`` to ``peripheral_aresetn[0:0]`` output port of :menuselection:`rst_gen_dpu_clk` IP block.

#. Connect Zynq UltraScale+ MPSoC IP block inputs:

   1. Connect ``S_ACI_HPC0_FPD`` to ``DPU0_M_AXI_DATA0`` output port of Deep-learning Process Unit IP block.
   2. Connect ``S_ACI_HPC1_FPD`` to ``DPU0_M_AXI_DATA1`` output port of Deep-learning Process Unit IP block.
   3. Connect ``S_ACI_LPD`` to ``DPU0_M_AXI_INSTR`` output port of Deep-learning Process Unit IP block.
   4. Connect ``maxihpm0_fpd`` to ``pl_clk0`` output port of Zynq UltraScale+ MPSoC IP block.
   5. Connect ``saxihpc0_fpd_aclk`` to ``clk_dpu`` output port of Clocking Wizard IP block.
   6. Connect ``saxihpc1_fpd_aclk`` to ``clk_dpu`` output port of Clocking Wizard IP block.
   7. Connect ``saxi_lpd_aclk`` to ``clk_dpu`` output port of Clocking Wizard IP block.
   8. Connect ``pl_ps_irq0`` to ``dpu0_interrupt`` output port of Deep-learning Process Unit IP block.


#. Run :menuselection:`Tools --> Validate Design`. When asked about auto assigning address segments, answer "Yes."


#. Final block design should look like this:

   .. figure:: ./DPU/dpu_bd.png
      :align: center

      Block design with Deep-learning Processor Unit

#. In Sources view select :menuselection:`Design Sources --> dpu_bd` and click :menuselection:`Create HDL Wrapper` in context menu. Use :menuselection:`Let Vivado manage wrapper and auto-update` option.
#. Generate bitstream

   .. warning:: Compared to previous tutorials, generating bitstream might take significantly longer time.

#. Export hardware including bitstream to file :file:`leopard-dpu-bd.xsa`

Add Vitis layers to Yocto Project :tutorial-machine:`Yocto`
-----------------------------------------------------------

#. Clone Xilinx ``meta-vitis`` layer:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ git clone -b rel-v2024.1 https://github.com/Xilinx/meta-vitis.git ../sources/meta-vitis

#. Clone KP labs ``meta-kp-vitis-ai`` layer:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ git clone -b nanbield https://github.com/kplabs-pl/meta-kp-vitis-ai.git ../sources/meta-kp-vitis-ai

#. Apply patches to ``meta-vitis`` that fix support for ``nanbield`` Yocto version

   .. code-block:: shell-session

       machine:~/leopard-linux-1/sources/meta-vitis$ git am ../meta-kp-vitis-ai/patches/*.patch
       Applying: Switch to nanbield
       Applying: bbappend to any glog version

#. Add layers to Yocto project:

   .. code-block:: shell-session

      machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-openembedded/meta-python
      machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-vitis
      machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-vitis-ai

#. Change recipe providing ``opencl-icd`` by adding configuarion option to :file:`~/leopard-linux-1/build/conf/local.conf`.

   .. code-block:: bitbake

       PREFERRED_PROVIDER_virtual/opencl-icd = "ocl-icd"

   .. note:: ``meta-vitis`` layer requires particular project configuration

Add Deep-learning Processor Unit bitstream to Linux image :tutorial-machine:`Yocto`
-----------------------------------------------------------------------------------
#. Create directory :file:`~/leopard-linux-1/sources/meta-local/recipes-example/bitstreams/dpu/` and copy :file:`leopard-dpu-bd.xsa` to it.
#. Create new recipe :file:`~/leopard-linux-1/sources/meta-local/recipes-example/bitstreams/dpu.bb` that will install bitstream with DPU.

   .. code-block:: bitbake

        LICENSE = "CLOSED"

        inherit bitstream

        SRC_URI += "file://leopard-dpu-bd.xsa"
        BITSTREAM_HDF_FILE = "${WORKDIR}/leopard-dpu-bd.xsa"

#. Create recipe append for kernel

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ recipetool newappend --wildcard-version ../sources/meta-local/ linux-xlnx

#. Create directory :file:`~/leopard-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx`.
#. Enable Xilinx DPU kernel driver module by creating file :file:`~/leopard-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx/xlnx-dpu.cfg` with content

   .. code-block:: kconfig

      CONFIG_XILINX_DPU=m

#. Enable kernel configuration fragment by adding it to :file:`~/leopard-linux-1/sources/meta-local/recipes-kernel/linux/linux-xlnx_%.bbappend`

   .. code-block:: bitbake

      FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

      SRC_URI += "file://xlnx-dpu.cfg"

#. Add new packages into Linux image by editing :file:`~/leopard-linux-1/sources/meta-local/recipes-leopard/images/dpu-leopard.bbappend` (TODO: limit deps)

   .. code-block:: bitbake

        IMAGE_INSTALL += "\
           fpga-manager-script \
           double-uart \
           dpu \
           vitis-ai-library \
           kernel-module-xlnx-dpu \
        "

#. Build firmware and image

   .. code-block:: shell-session

       machine:~/leopard-linux-1$ bitbake leopard-all

#. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/leopard-linux-1$ mkdir -p ./egse-host-transfer
        machine:~/leopard-linux-1$ cp build/tmp/deploy/images/leopard-dpu/bootbins/boot-common.bin ./egse-host-transfer
        machine:~/leopard-linux-1$ cp build/tmp/deploy/images/leopard-dpu/system.dtb  ./egse-host-transfer
        machine:~/leopard-linux-1$ cp build/tmp/deploy/images/leopard-dpu/dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot ./egse-host-transfer
        machine:~/leopard-linux-1$ cp build/tmp/deploy/images/leopard-dpu/Image ./egse-host-transfer

#. Transfer content of :file:`egse-host-transfer` directory to EGSE Host and place it in :file:`/var/tftp/tutorial` directory


Run model on Deep-learning Processor Unit :tutorial-machine:`EGSE Host`
-----------------------------------------------------------------------
#. Verify that all necessary artifacts are present on EGSE Host: (TODO: fix size after changing dependencies)

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 106M
       -rw-rw-r-- 1 customer customer  21M Jan 23 09:37 Image
       -rw-rw-r-- 1 customer customer 1.6M Jan 23 09:37 boot-common.bin
       -rw-rw-r-- 1 customer customer  93M Jan 23 09:37 dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer  39K Jan 23 09:37 system.dtb

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot`` shall be about ~100MB)


#. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/leopard-pn1-uart

   Leave this terminal open and get back to SSH connection used in previous steps.

#. Power on Leopard

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml power on
       Powering on...Success

#. Power on DPU Processing Node 1

   .. code-block:: shell-session

       customer@egse-367mwbwfg5wy2:~$ sml pn1 power on --nor-memory nor1
       Powering on processing node Node1...Success

#. DPU boot process should be visible in ``minicom`` terminal

#. Log in to DPU using ``root`` user

   .. code-block:: shell-session

      leopard login: root
      root@leopard:~#

#. Load DPU bitstream

   .. code-block:: shell-session

      root@leopard:~# fpgautil -o /lib/firmware/dpu/overlay.dtbo

#. Verify that DPU instance is visible in system

   .. code-block:: shell-session

      root@leopard:~# xdputil query
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


#. Follow :doc:`/tutorials/ml_deployment/index` tutorials to train, compile and deploy model to Deep-learning Processor Unit. (TODO)

Summary
-------
In this tutorial you walked through steps required to include Deep-learning Processor Unit in FPGA design and integrate it with Yocto project.
