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
  * Yocto requirements (https://docs.yoctoproject.org/4.3/ref-manual/system-requirements.html#required-packages-for-the-build-host)
* At least 120GB free space for Yocto build

Provided outputs
----------------
Following files (:ref:`tutorial_files`) are associated with this tutorial:

* :file:`Antelope/Zero-to-hero/02 Minimalist Linux distribution/boot-firmware.bin` - Boot firmware for Antelope
* :file:`Antelope/Zero-to-hero/02 Minimalist Linux distribution/boot-pins.bin` - Boot script for Antelope
* :file:`Antelope/Zero-to-hero/02 Minimalist Linux distribution/antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot` - Root filesystem for Antelope
* :file:`Antelope/Zero-to-hero/02 Minimalist Linux distribution/Image` - Linux kernel
* :file:`Antelope/Zero-to-hero/02 Minimalist Linux distribution/system.dtb` - Device tree

Use these files if you want to skip building Yocto distribution by yourself.


Create project :tutorial-machine:`Yocto`
----------------------------------------
#. Create new directory for Yocto project and navigate to it.

   .. code-block:: shell-session

       machine:~$ mkdir ~/antelope-linux-1
       machine:~$ cd ~/antelope-linux-1
       machine:~/antelope-linux-1$

#. Clone Poky layer from Yocto project

   .. code-block:: shell-session

       machine:~/antelope-linux-1$ git clone -b nanbield https://git.yoctoproject.org/poky sources/poky

#. Create new build configuration

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

Add layers :tutorial-machine:`Yocto`
------------------------------------
#. Clone Xilinx layers:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx.git ../sources/meta-xilinx
       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx-tools.git ../sources/meta-xilinx-tools

#. Add set of required layers from Xilinx repositories:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-core
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-bsp
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-standalone
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx-tools


   .. note::

        After adding Xilinx layers, BitBake might report warning

            The ZynqMP pmu-rom is not enabled (...) To enable this you must add 'xilinx' to the LICENSE_FLAGS_ACCEPTED to indicate you accept the software license.

        This is for informational purposes only and you can ignore it.

#. Clone KP Labs layers

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/kplabs-pl/meta-kp-classes.git ../sources/meta-kp-classes
       machine:~/antelope-linux-1/build$ git clone -b nanbield https://github.com/kplabs-pl/meta-kp-antelope.git ../sources/meta-kp-antelope

#. Add set of required layers from KP Labs repositories:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-classes
       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-antelope

Create layer for customizations :tutorial-machine:`Yocto`
---------------------------------------------------------
#. Create empty layer

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers create-layer ../sources/meta-local

#. Add newly created layer to project

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake-layers add-layer ../sources/meta-local

#. Verify set of layers enabled in project by opening :file:`~/antelope-linux-1/build/conf/bblayers.conf` and checking its contents:

   .. code-block:: bitbake

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
       ~/antelope-linux-1/sources/meta-kp-classes \
       ~/antelope-linux-1/sources/meta-kp-antelope \
       ~/antelope-linux-1/sources/meta-local \
       "

Configure project :tutorial-machine:`Yocto`
-------------------------------------------
#. Edit :file:`~/antelope-linux-1/build/conf/local.conf` and add following lines at the beginning:

   .. code-block:: bitbake

       MACHINE = "antelope"
       DISTRO = "kplabs-dpu"
       INHERIT += "rm_work"

#. Create recipe append to set XSA file

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ recipetool newappend --wildcard-version ../sources/meta-local/ external-hdf

#. Create directory :file:`~/antelope-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf` and copy :file:`antelope_minimal.xsa` to it.
#. Edit recipe append :file:`~/antelope-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf_%.bbappend` and set path to XSA file

   .. code-block:: bitbake

       FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

       HDF_BASE = "file://"
       HDF_PATH = "antelope_minimal.xsa"


Build project :tutorial-machine:`Yocto`
---------------------------------------
#. Build project artifacts:

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake antelope-all

   .. warning:: First build might take a long time to complete. Be patient.

#. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/antelope-linux-1/build$ mkdir -p ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/bootbins/boot-firmware.bin ../build/egse-host-transfer/
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/u-boot-scripts/boot-script-pins/boot-pins.scr ../build/egse-host-transfer/
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/system.dtb ../build/egse-host-transfer/
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/Image ../build/egse-host-transfer/
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot ../build/egse-host-transfer/

#. Transfer content of :file:`~/antelope-linux-1/egse-host-transfer` directory to EGSE Host and place it in :file:`/var/tftp/tutorial` directory

Booting Linux on DPU :tutorial-machine:`EGSE Host`
--------------------------------------------------
#. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 30158
       -rw-rw-r-- 1 customer customer  22M Jul 10 08:38 Image
       -rw-rw-r-- 1 customer customer 1.6M Jul 10 08:35 boot-firmware.bin
       -rw-rw-r-- 1 customer customer 2.8K Jul 10 08:38 boot-pins.scr
       -rw-rw-r-- 1 customer customer  16M Jul 10 08:39 antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer  37K Jul 10 08:38 system.dtb

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot`` shall be about ~15MB)

#. Ensure that Antelope is powered off

   .. code-block:: shell-session

       customer@egse-host:~$ sml power off
       Powering off...Success

#. Power on Antelope

   .. code-block:: shell-session

       customer@egse-host:~$ sml power on
       Powering on...Success

#. Power on DPU

   .. code-block:: shell-session

       customer@egse-host:~$ sml dpu power on
       Powering on...Success

#. Write boot firmware to DPU boot flash

   .. code-block:: shell-session

       customer@egse-host:~$ sml dpu boot-flash write 0 /var/tftp/tutorial/boot-firmware.bin
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 43.1 MB/s
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 383.9 kB/s
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 13.1 kB/s

#. Write U-Boot boot script to DPU boot flash

   .. code-block:: shell-session

       customer@egse-host:~$ sml dpu boot-flash write 0x4E0000 /var/tftp/tutorial/boot-pins.scr
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 55.9 MB/s

#. Prepare U-Boot script for booting from network by writing following content to :file:`/var/tftp/antelope-boot.cmd`

   .. code-block:: bash

       dhcp ${kernel_addr_r} /tutorial/Image
       dhcp ${ramdisk_addr_r} /tutorial/antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot
       dhcp ${fdt_addr_r} /tutorial/system.dtb
       booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}

#. Compile U-Boot script

   .. code-block:: shell-session

       customer@egse-host:~$ mkimage -A arm64 -O U-Boot -T script -C none -d /var/tftp/antelope-boot.cmd /var/tftp/antelope-boot.scr
       Image Name:
       Created:      Wed Jul 10 08:50:54 2024
       Image Type:   AArch64 U-Boot Script (uncompressed)
       Data Size:    216 Bytes = #.21 KiB = #.00 MiB
       Load Address: 00000000
       Entry Point:  00000000
       Contents:
           Image 0: 208 Bytes = #.20 KiB = #.00 MiB

#. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/antelope-dpu-uart

   Leave this terminal open and get back to SSH connection used in previous steps.

#. Release DPU from reset

   .. code-block:: shell-session

      customer@egse-host:~$ sml dpu reset off 7

#. DPU boot process should be visible in ``minicom`` terminal

   .. include:: ./minimalist_linux_distro/boot.txt

#. Log in to DPU using ``root`` user

   .. code-block:: shell-session

      antelope login: root
      root@antelope:~#

Summary
-------
In this tutorial you've built minimal Linux distribution for Antelope DPU using Yocto and XSA file prepared with platform configuration. After copying build artifacts to EGSE Host you've written necessary boot firmware to DPU boot flash. You've also prepared U-Boot script for booting from network and observed boot process in ``minicom`` terminal. Finally you've logged in to DPU and verified that Linux is running.
