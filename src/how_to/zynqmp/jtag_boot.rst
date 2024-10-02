Booting over JTAG
=================

A bit of background
-------------------
With boot mode set to JTAG, it's possible to load entire boot firmware (FSBL, U-Boot) using debug interface. This mode is particularly useful with frequent changes to these components as it avoids the need to re-write storage device.

Prerequisites
-------------
1. Vivado Lab installed on EGSE Host
2. Boot files

   * ELF file with First Stage Boot Loader (FSBL) - ``fsbl.elf``
   * ELF file with PMU Firmware - ``pmufw.elf``
   * ELF file with U-Boot - ``u-boot.elf``
   * ELF file with ARM Trusted Firmware (ATF) - ``arm-trusted-firmware.elf``
   * ELF file with device tree for U-Boot - ``system.dtb``

3. Boot mode set to JTAG

Steps
-----
1. Log in to EGSE Host

   .. code-block:: shell-session

        my-machine:~$ ssh customer@egse-my-egse.egse.sml.lan
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

        xsdb% targets
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

6. Enable access to PMU target

   .. code-block:: shell-session

        xsdb% rwr csu jtag_sec ssss_pmu_sec 7
        xsdb% targets
        1  PS TAP
            2  PMU
                12  MicroBlaze PMU (Sleeping. No clock)
            3  PL
        5* PSU
            6  RPU (Reset)
                7  Cortex-R5 #0 (No Power)
                8  Cortex-R5 #1 (No Power)
            9  APU
            10  Cortex-A53 #0 (Running)
            11  Cortex-A53 #1 (Running)

7. Select Microblaze PMU target

   .. code-block:: shell-session

        xsdb% targets -set -filter {name =~ "MicroBlaze PMU"}
        xsdb%

8. Load and run PMU firmware

   .. code-block:: shell-session

         xsdb% dow pmufw.elf
         Downloading Program -- pmufw.elf
                 section, .vectors.reset: 0xffdc0000 - 0xffdc0007
                 section, .vectors.sw_exception: 0xffdc0008 - 0xffdc000f
                 section, .vectors.interrupt: 0xffdc0010 - 0xffdc0017
                 section, .vectors.hw_exception: 0xffdc0020 - 0xffdc0027
                 section, .text: 0xffdc0050 - 0xffdd19c3
                 section, .rodata: 0xffdd19c4 - 0xffdd2bdf
                 section, .data: 0xffdd2be0 - 0xffdd6d3f
                 section, .sdata2: 0xffdd6d40 - 0xffdd6d3f
                 section, .sdata: 0xffdd6d40 - 0xffdd6d3f
                 section, .sbss: 0xffdd6d40 - 0xffdd6d3f
                 section, .bss: 0xffdd6d40 - 0xffddaa5f
                 section, .srdata: 0xffddaa60 - 0xffddb37b
                 section, .stack: 0xffddb37c - 0xffddc37f
                 section, .xpbr_serv_ext_tbl: 0xffddf6e0 - 0xffddfadf
         100%    0MB   0.2MB/s  00:00
         Setting PC to Program Start Address 0xffdd11dc
         Successfully downloaded pmufw.elf
         xsdb% con
         Info: MicroBlaze PMU (target 3) Running (Sleeping. No clock)

9. Select ARM Cortex-A53 target

   .. code-block:: shell-session

        xsdb% targets -set -filter {name =~ "Cortex-A53 #0"}
        xsdb%

10. Reset processor, then load and run FSBL

    .. code-block:: shell-session

        xsdb% rst -processor -clear-registers
        Info: Cortex-A53 #0 (target 10) Stopped at 0xffff0000 (Reset Catch)
        xsdb% dow fsbl.elf
        Downloading Program -- fsbl.elf
                section, .text: 0xfffc0000 - 0xfffcdf47
                section, .note.gnu.build-id: 0xfffcdf48 - 0xfffcdf6b
                section, .init: 0xfffcdf80 - 0xfffcdfb3
                section, .fini: 0xfffcdfc0 - 0xfffcdff3
                section, .rodata: 0xfffce000 - 0xfffcead1
                section, .sys_cfg_data: 0xfffceb00 - 0xfffcf187
                section, .mmu_tbl0: 0xfffd0000 - 0xfffd000f
                section, .mmu_tbl1: 0xfffd1000 - 0xfffd2fff
                section, .mmu_tbl2: 0xfffd3000 - 0xfffd6fff
                section, .data: 0xfffd7000 - 0xfffd8247
                section, .sbss: 0xfffd8248 - 0xfffd827f
                section, .bss: 0xfffd8280 - 0xfffdeabf
                section, .heap: 0xfffdeac0 - 0xfffdeebf
                section, .stack: 0xfffdeec0 - 0xfffe0ebf
                section, .drvcfg_sec: 0xfffe0ec0 - 0xfffe0ebf
                section, .dup_data: 0xfffe0ec0 - 0xfffe2107
                section, .handoff_params: 0xfffe9e00 - 0xfffe9e87
                section, .bitstream_buffer: 0xffff0040 - 0xfffffc3f
        100%    0MB   0.1MB/s  00:00
        Setting PC to Program Start Address 0xfffc0000
        Successfully downloaded fsbl.elf
        xsdb% con
        Info: Cortex-A53 #0 (target 10) Running

    After resuming processor, give FSBL some time to run before loading next firmware.

11. Load then run ARM Trusted Firmware and U-Boot.

    .. code-block:: shell-session

        xsdb% dow -data system.dtb 0x00100000
        100%    0MB   0.1MB/s  00:00
        Successfully downloaded system.dtb
        xsdb% dow u-boot.elf
        Downloading Program -- u-boot.elf
                section, .data: 0x08000000 - 0x0814ba19
        100%    1MB   0.2MB/s  00:08
        Setting PC to Program Start Address 0x08000000
        Successfully downloaded u-boot.elf
        xsdb% Info: Cortex-A53 #0 (target 10) Stopped at 0xfffcacd8 (External Debug Request)
        xsdb% dow arm-trusted-firmware.elf
        Downloading Program -- arm-trusted-firmware.elf
                section, .text: 0xfffea000 - 0xffff1fff
                section, .rodata: 0xffff2000 - 0xffff2fff
                section, .data: 0xffff3000 - 0xffff6091
                section, stacks: 0xffff60c0 - 0xffff71bf
                section, .bss: 0xffff71c0 - 0xffff7fbf
                section, xlat_table: 0xffff8000 - 0xffffcfff
                section, coherent_ram: 0xffffd000 - 0xffffdfff
        100%    0MB   0.2MB/s  00:00
        Setting PC to Program Start Address 0xfffea000
        Successfully downloaded arm-trusted-firmware.elf
        xsdb% con
        Info: Cortex-A53 #0 (target 10) Running

    .. note::

        Address ``0x00100000`` must match ``CONFIG_XILINX_OF_BOARD_DTB_ADDR`` configuration value in U-Boot (defaults to ``0x00100000``).

12. At this point, DPU should be running U-Boot.

References
----------
* PMU Firmware loading options in Zynq UltraScale+ MPSoC Software Developer Guide (UG1137) (https://docs.amd.com/r/en-US/ug1137-zynq-ultrascale-mpsoc-swdev/PMU-Firmware-Loading-Options)
