Minimalist Linux distribution
=============================

Goal
----
In this tutorial you will:
  * create Linux distribution using Yocto (along with support firmware) based on Vivado project created earlier
  * boot Linux on Leopard DPU through EGSE Host

A bit of background
-------------------
Running Linux on device like Leopard DPU requires set of artifacts

* Boot firmware (in particular *first stage bootloader* and U-Boot)
* Linux kernel
* Device tree
* Root filesystem

Yocto can build these items automatically. Developers construct project using Yocto from **layers** coming from Yocto project itself, hardware manufactures and their own. Each layer contributes series of **recipes** that are describing how to build particular components of Linux distribution. **BitBake** tool manages all dependencies between recipes and hides build complexity.

After building all required artifacts you can use Leopard DPU boot capabilities to load boot firmware into persistent memory and load Linux kernel and root filesystem from network.

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

* :file:`Leopard/Zero-to-hero/02 Minimalist Linux distribution/boot-common.bin` - Boot firmware for Leopard
* :file:`Leopard/Zero-to-hero/02 Minimalist Linux distribution/dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot` - Root filesystem for Leopard
* :file:`Leopard/Zero-to-hero/02 Minimalist Linux distribution/Image` - Linux kernel
* :file:`Leopard/Zero-to-hero/02 Minimalist Linux distribution/system.dtb` - Device tree

Use these files if you want to skip building Yocto distribution by yourself.

Create project :tutorial-machine:`Yocto`
----------------------------------------
#. Create new directory for Yocto project and navigate to it.

   .. code-block:: shell-session

       machine:~$ mkdir ~/leopard-linux-1
       machine:~$ cd ~/leopard-linux-1
       machine:~/leopard-linux-1$

#. Clone Poky layer from Yocto project

   .. code-block:: shell-session

       machine:~/leopard-linux-1$ git clone -b nanbield https://git.yoctoproject.org/poky sources/poky

#. Create new build configuration

   .. code-block:: shell-session

       machine:~/leopard-linux-1$ source sources/poky/oe-init-build-env ./build
       You had no conf/local.conf file. This configuration file has therefore been
       created for you from ~/leopard-linux-1/sources/poky/meta-poky/conf/templates/default/local.conf.sample
       You may wish to edit it to, for example, select a different MACHINE (target
       hardware).

       You had no conf/bblayers.conf file. This configuration file has therefore been
       created for you from ~/leopard-linux-1/sources/poky/meta-poky/conf/templates/default/bblayers.conf.sample
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
       machine:~/leopard-linux-1/build$

Add layers :tutorial-machine:`Yocto`
------------------------------------
#. Clone Xilinx layers:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx.git ../sources/meta-xilinx
       machine:~/leopard-linux-1/build$ git clone -b nanbield https://github.com/Xilinx/meta-xilinx-tools.git ../sources/meta-xilinx-tools
       machine:~/leopard-linux-1/build$ git clone -b nanbield https://git.openembedded.org/meta-openembedded/ ../sources/meta-openembedded

#. Add set of required layers from Xilinx repositories:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-core
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-bsp
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx/meta-xilinx-standalone
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-xilinx-tools
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-openembedded/meta-oe/
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-openembedded/meta-networking/


   .. note::

        After adding Xilinx layers, BitBake might report warning

            The ZynqMP pmu-rom is not enabled (...) To enable this you must add 'xilinx' to the LICENSE_FLAGS_ACCEPTED to indicate you accept the software license.

        This is for informational purposes only and you can ignore it.

#. Clone KP Labs layers

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ git clone -b nanbield https://github.com/kplabs-pl/meta-kp-classes.git ../sources/meta-kp-classes
       machine:~/leopard-linux-1/build$ git clone -b nanbield https://github.com/kplabs-pl/meta-kp-leopard.git ../sources/meta-kp-leopard

#. Add set of required layers from KP Labs repositories:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-classes/
       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-kp-leopard

Create layer for customizations :tutorial-machine:`Yocto`
---------------------------------------------------------
#. Create empty layer

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ bitbake-layers create-layer ../sources/meta-local

#. Add newly created layer to project

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ bitbake-layers add-layer ../sources/meta-local

#. Verify set of layers enabled in project by opening :file:`~/leopard-linux-1/build/conf/bblayers.conf` and checking its contents:

   .. code-block:: bitbake

       # POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
       # changes incompatibly
       POKY_BBLAYERS_CONF_VERSION = "2"

       BBPATH = "${TOPDIR}"
       BBFILES ?= ""

       BBLAYERS ?= " \
       ~/leopard-linux-1/sources/poky/meta \
       ~/leopard-linux-1/sources/poky/meta-poky \
       ~/leopard-linux-1/sources/poky/meta-yocto-bsp \
       ~/leopard-linux-1/sources/meta-xilinx/meta-xilinx-core \
       ~/leopard-linux-1/sources/meta-xilinx/meta-xilinx-bsp \
       ~/leopard-linux-1/sources/meta-xilinx/meta-xilinx-standalone \
       ~/leopard-linux-1/sources/meta-xilinx-tools \
       ~/leopard-linux-1/sources/meta-openembedded/meta-oe \
       ~/leopard-linux-1/sources/meta-openembedded/meta-networking \
       ~/leopard-linux-1/sources/meta-kp-classes \
       ~/leopard-linux-1/sources/meta-kp-leopard \
       ~/leopard-linux-1/sources/meta-local \
       "

Configure project :tutorial-machine:`Yocto`
-------------------------------------------
#. Edit :file:`~/leopard-linux-1/build/conf/local.conf` and add following lines at the beginning:

   .. code-block:: bitbake

        MACHINE = "leopard-dpu"
        DISTRO = "kplabs-dpu"
        INHERIT += "rm_work"
        PROJECT_NAME = "leopard-dpu-minimal-linux"


#. Create recipe append to set XSA file

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ recipetool newappend --wildcard-version ../sources/meta-local/ external-hdf

#. Create directory :file:`~/leopard-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf` and copy :file:`minimal-leopard.xsa` to it.
#. Edit recipe append :file:`~/leopard-linux-1/sources/meta-local/recipes-bsp/hdf/external-hdf_%.bbappend` and set path XSA file

   .. code-block:: bitbake

       FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

       HDF_BASE = "file://"
       HDF_PATH = "leopard-minimal.xsa"


Build project :tutorial-machine:`Yocto`
---------------------------------------
#. Build project artifacts:

   .. code-block:: shell-session

       machine:~/leopard-linux-1/build$ bitbake leopard-all

   .. warning:: First build might take a long time to complete. Be patient.


#. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/leopard-linux-1/build$ mkdir -p ../build/egse-host-transfer/
        machine:~/leopard-linux-1/build$ cp tmp/deploy/images/leopard-dpu/bootbins/boot-common.bin ../build/egse-host-transfer/
        machine:~/leopard-linux-1/build$ cp tmp/deploy/images/leopard-dpu/system.dtb ../build/egse-host-transfer/
        machine:~/leopard-linux-1/build$ cp tmp/deploy/images/leopard-dpu/dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot ../build/egse-host-transfer/
        machine:~/leopard-linux-1/build$ cp tmp/deploy/images/leopard-dpu/Image ../build/egse-host-transfer/

#. Transfer content of :file:`~/leopard-linux-1/egse-host-transfer` directory to EGSE Host and place it in :file:`/var/tftp/tutorial` directory


Booting Linux on DPU :tutorial-machine:`EGSE Host`
--------------------------------------------------
#. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

        customer@egse-host:~$ ls -lh /var/tftp/tutorial
        total 48M
        -rw-rw-r-- 1 customer customer  21M Jan 22 07:55 Image
        -rw-rw-r-- 1 customer customer 1.6M Jan 22 07:55 boot-common.bin
        -rw-rw-r-- 1 customer customer  35M Jan 22 07:55 dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot
        -rw-rw-r-- 1 customer customer  39K Jan 22 07:55 system.dtb

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot`` shall be about ~40MB)

#. Ensure that Leopard is powered off

   .. code-block:: shell-session

       customer@egse-host:~$ sml power off
       Powering off...Success

#. Prepare U-Boot script for booting from network by writing following content to :file:`/var/tftp/leopard-boot.cmd`

   .. code-block:: bash

        dhcp

        tftpboot ${kernel_addr_r} /tutorial/Image
        tftpboot ${fdt_addr_r} /tutorial/system.dtb
        tftpboot ${ramdisk_addr_r} /tutorial/dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot

        booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}

#. Compile U-Boot script

   .. code-block:: shell-session

        customer@egse-host:~$ mkimage -A arm64 -O U-Boot -T script -C none -d /var/tftp/leopard-boot.cmd /var/tftp/leopard-boot.scr
        Image Name:
        Created:      Wed Jan 22 08:31:23 2025
        Image Type:   AArch64 U-Boot Script (uncompressed)
        Data Size:    240 Bytes = 0.23 KiB = 0.00 MiB
        Load Address: 00000000
        Entry Point:  00000000
        Contents:
           Image 0: 232 Bytes = 0.23 KiB = 0.00 MiB

#. Power on Leopard

   .. code-block:: shell-session

       customer@egse-host:~$ sml power on
       Powering on...Success

#. Write boot firmware to DPU boot flash

   .. code-block:: shell-session

       customer@egse-host:~$ sml boot-flash write --nor-memory nor1 0 /var/tftp/tutorial/boot-common.bin
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 48.6 MB/s
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 553.3 kB/s
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 13.5 kB/s

#. Write U-Boot boot script to DPU boot flash

   .. code-block:: shell-session

       customer@egse-host:~$ sml boot-flash write --nor-memory nor1 0x380000 /var/tftp/leopard-boot.scr
       Uploading   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Erasing     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 ?
       Programming ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 30.7 MB/s

#. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/leopard-pn1-uart

   Leave this terminal open and get back to SSH connection used in previous steps.

#. Power on Processing Node 1

   .. code-block:: shell-session

       customer@egse-host:~$ sml pn1 power on --nor-memory nor1
       Powering on processing node Node1...Success

#. DPU boot process should be visible in ``minicom`` terminal

   .. note:: It might take ~20 seconds to get first line of output

   .. include:: ./minimalist_linux_distro/boot.txt

#. Log in to DPU using ``root`` user

   .. code-block:: shell-session

      leopard-dpu login: root
      root@leopard-dpu:~#

Summary
-------
In this tutorial you've built minimal Linux distribution for Leopard DPU using Yocto and XSA file prepared with platform configuration. After copying build artifacts to EGSE Host you've written necessary boot firmware to DPU boot flash. You've also prepared U-Boot script for booting from network and observed boot process in ``minicom`` terminal. Finally you've logged in to DPU and verified that Linux is running.
