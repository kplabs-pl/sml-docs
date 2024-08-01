Minimalist Linux distribution
=============================

Goal
----
In this tutorial you will:
  * create Linux distribution using Yocto (along with support firmware) based on Vivado project created earlier
  * boot Linux on Antelope DPU through EGSE Host

A bit of background
-------------------
Running Linux on device like Antelope DPU requires set of artifacts

* Boot firmware (in particular *first stage bootloader* and U-Boot)
* Linux kernel
* Device tree
* Root filesystem

Yocto can build these items automatically. Developers construct project using Yocto from **layers** coming from Yocto project itself, hardware manufactures and their own. Each layer contributes series of **recipes** that are describing how to build particular components of Linux distribution. **BitBake** tool manages all dependencies between recipes and hides build complexity.

After building all required artifacts you can use Antelope DPU boot capabilities to load boot firmware into persistent memory and load Linux kernel and root filesystem from network.

Prerequisites
-------------
* ``.xsa`` file with platform configuration from :doc:`./minimalist_vivado_project`
* Machine with Linux edition supported by Yocto
* Tools installed on machine:

  * ``libtinfo5`` (required by Xilinx layers)
  * Yocto requirements (https://docs.yoctoproject.org/ref-manual/system-requirements.html#required-packages-for-the-build-host)
* At least 60GB free space for Yocto build

Create project
--------------
1. Create new directory for Yocto project and navigate to it.

   .. code-block:: shell-session

       machine:~$ mkdir ~/antelope-linux-1
       machine:~$ cd ~/antelope-linux-1
       machine:~/antelope-linux-1$

2. Clone Poky layer from Yocto project

   .. code-block:: shell-session

       machine:~/antelope-linux-1$ git clone -b nanbield https://git.yoctoproject.org/poky sources/poky

3. Create new build configuration

   .. code-block:: shell-session

       machine:~/antelope-linux-1$ source sources/poky/oe-init-build-env ./build
       You had no conf/local.conf file. This configuration file has therefore been
       created for you from ~/antelope-linux-1/sources/poky/meta-poky/conf/templates/default/local.conf.sample
       You may wish to edit it to, for example, select a different MACHINE (target
       hardware).

       You had no conf/bblayers.conf file. This configuration file has therefore been
       created for you from ~/antelope-linux-1/sources/poky/meta-poky/conf/templates/default/bblayers.conf.sample
       To add additional metadata layers into your configuration please add entries
       to conf/bblayers.conf.

       The Yocto Project has extensive documentation about OE including a reference
       manual which can be found at:
           https://docs.yoctoproject.org

       For more information about OpenEmbedded see the website:
           https://www.openembedded.org/


       ### Shell environment set up for builds. ###

       You can now run 'bitbake <target>'

       Common targets are:
           core-image-minimal
           core-image-full-cmdline
           core-image-sato
           core-image-weston
           meta-toolchain
           meta-ide-support

       You can also run generated qemu images with a command like 'runqemu qemux86-64'.

       Other commonly useful commands are:
       - 'devtool' and 'recipetool' handle common recipe tasks
       - 'bitbake-layers' handles common layer tasks
       - 'oe-pkgdata-util' handles common target package tasks
       machine:~/antelope-linux-1/build$

Add layers
----------
1. Clone Xilinx layers:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx.git ../sources/meta-xilinx
       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx-tools.git ../sources/meta-xilinx-tools

2. Add set of required layers from Xilinx repositories:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-core
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-bsp
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-standalone
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx-tools


   .. note::

        After adding Xilinx layers, BitBake might report warning

            The ZynqMP pmu-rom is not enabled (...) To enable this you must add 'xilinx' to the LICENSE_FLAGS_ACCEPTED to indicate you accept the software license.

        This is for informational purposes only and you can ignore it.

3. Retrieve KP Labs-provided layers
4. Add set of required layers from KP Labs repositories:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-classes/meta-kp-classes/
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-antelope

Create layer for customizations
-------------------------------
1. Create empty layer

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers create-layer ../sources/meta-local

2. Add newly created layer to project

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-local

3. Verify set of layers enabled in project by opening ``~/antelope-linux-1/build/conf/bblayers.conf`` and checking its contents:

   .. code-block::

       # POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
       # changes incompatibly
       POKY_BBLAYERS_CONF_VERSION = "2"

       BBPATH = "${TOPDIR}"
       BBFILES ?= ""

       BBLAYERS ?= " \
       ~/antelope-linux-1/sources/poky/meta \
       ~/antelope-linux-1/sources/poky/meta-poky \
       ~/antelope-linux-1/sources/poky/meta-yocto-bsp \
       ~/antelope-linux-1/sources/meta-xilinx/meta-xilinx-core \
       ~/antelope-linux-1/sources/meta-xilinx/meta-xilinx-bsp \
       ~/antelope-linux-1/sources/meta-xilinx/meta-xilinx-standalone \
       ~/antelope-linux-1/sources/meta-xilinx-tools \
       ~/antelope-linux-1/sources/meta-kp-classes/meta-kp-classes \
       ~/antelope-linux-1/sources/meta-kp-antelope \
       ~/antelope-linux-1/sources/meta-local \
       "

Configure project
-----------------
1. Edit ``~/antelope-linux-1/build/conf/local.conf`` and add following lines at the beginning:

   .. code-block::

       MACHINE = "antelope"
       DISTRO = "kplabs-dpu"
       INHERIT += "rm_work"

2. Create recipe append to set XSA file

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ recipetool newappend --wildcard-version ../sources/meta-local/ external-hdf

3. Create directory ``~/antelope-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf`` and copy ``top_bd_wrapper.xsa`` to it.
4. Edit recipe append ````~/antelope-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf.bb`` and set path XSA file

   .. code-block::

       FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

       HDF_BASE = "file://"
       HDF_PATH = "top_bd_wrapper.xsa"


Build project
-------------
1. Build project artifacts:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake core-image-minimal bootbin-firmware boot-script-pins virtual/kernel device-tree

   .. warning:: First build might take a long time to complete. Be patient.

2. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/antelope-linux-1$ mkdir -p ./egse-host-transfer
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/bootbins/boot-firmware.bin ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/u-boot-scripts/boot-script-pins/boot-pins.scr ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/system.dtb ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/Image ./egse-host-transfer/
        machine:~/antelope-linux-1$ cp build/tmp/deploy/images/antelope/core-image-minimal-antelope.rootfs.cpio.gz.u-boot ./egse-host-transfer/

3. Transfer content of ``egse-host-transfer`` directory to EGSE Host and place it in ``/var/tftp/tutorial`` directory

Booting Linux on DPU
--------------------
1. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 30158
       -rw-rw-r-- 1 customer customer  22M Jul 10 08:38 Image
       -rw-rw-r-- 1 customer customer 1.6M Jul 10 08:35 boot-firmware.bin
       -rw-rw-r-- 1 customer customer 2.8K Jul 10 08:38 boot-pins.scr
       -rw-rw-r-- 1 customer customer  16M Jul 10 08:39 core-image-minimal-antelope.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer  37K Jul 10 08:38 system.dtb

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

6. Prepare U-Boot script for booting from network by writing following content to ``/var/tftp/antelope-boot.cmd``

   .. code-block:: bash

       dhcp ${kernel_addr_r} /tutorial/Image
       dhcp ${ramdisk_addr_r} /tutorial/core-image-minimal-antelope.rootfs.cpio.gz.u-boot
       dhcp ${fdt_addr_r} /tutorial/system.dtb
       booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}

7. Compile U-Boot script

   .. code-block:: shell-session

       customer@egse-host:~$ mkimage -A arm64 -O U-Boot -T script -C none -d /var/tftp/antelope-boot.cmd /var/tftp/antelope-boot.scr
       Image Name:
       Created:      Wed Jul 10 08:50:54 2024
       Image Type:   AArch64 U-Boot Script (uncompressed)
       Data Size:    216 Bytes = 0.21 KiB = 0.00 MiB
       Load Address: 00000000
       Entry Point:  00000000
       Contents:
           Image 0: 208 Bytes = 0.20 KiB = 0.00 MiB

8. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/antelope-dpu-uart

    Leave this terminal open and get back to SSH connection used in previous steps.

9. Release DPU from reset

   .. code-block:: shell-session

      customer@egse-host:~$ sml dpu reset off 7

10. DPU boot process should be visible in ``minicom`` terminal

    .. include:: ./minimalist_linux_distro/boot.txt

11. Log in to DPU using ``root`` user

    .. code-block::

      antelope login: root
      root@antelope:~#

Summary
-------
In this tutorial you've built minimal Linux distribution for Antelope DPU using Yocto and XSA file prepared with platform configuration. After copying build artifacts to EGSE Host you've written necessary boot firmware to DPU boot flash. You've also prepared U-Boot script for booting from network and observed boot process in ``minicom`` terminal. Finally you've logged in to DPU and verified that Linux is running.
