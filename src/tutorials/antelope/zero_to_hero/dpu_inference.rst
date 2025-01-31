Onboard inference
=================

Goal
----
This tutorial shows how to run ground segementation on Antelope using previously prepared model and Deep learning Processor Unit accelerator.

A bit of background
-------------------
Running inference requires building Linux distribution with DPU support, prepared model, runner script and input data. You've already prepared all these components in different tutorials, this one puts everything together. Runner in this tutorial will perform ground segmentation and output numeric predictions results for each input image along with visualization of segmentation by overlying classes on top of input images.

Prerequisites
-------------
* Yocto project with Deep learning Processor Unit (:doc:`./dpu`)
* Quantized model (:doc:`/tutorials/ml_deployment/model_deployment/model_compilation`)
* Python tool for running inference (:doc:`/tutorials/ml_deployment/onboard_model_runner_python`)
* 3-4 test images from ML dataset in form of 512x512 patches (:ref:`tutorial_files`)

Provided outputs
----------------
Following files (:ref:`tutorial_files`) are associated with this tutorial:

* :file:`Antelope/Zero-to-hero/05 Onboard inference/boot-firmware.bin` - Boot firmware for Antelope
* :file:`Antelope/Zero-to-hero/05 Onboard inference/boot-pins.bin` - Boot script for Antelope
* :file:`Antelope/Zero-to-hero/05 Onboard inference/antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot` - Root filesystem for Antelope
* :file:`Antelope/Zero-to-hero/05 Onboard inference/Image` - Linux kernel
* :file:`Antelope/Zero-to-hero/05 Onboard inference/system.dtb` - Device tree

Use these files if you don't want to build Yocto distribution by yourself.


Add inference tools to Yocto project :tutorial-machine:`Yocto`
--------------------------------------------------------------
#. Create directory :file:`~/antelope-linux-1/sources/meta-local/recipes-example/inference/inference/`
#. Copy ``model_runner.py`` to :file:`~/antelope-linux-1/sources/meta-local/recipes-example/inference/inference/`
#. Copy ``deep_globe_segmentation_unet_512_512.xmodel`` to :file:`~/antelope-linux-1/sources/meta-local/recipes-example/inference/inference/`
#. Create new recipe :file:`~/antelope-linux-1/sources/meta-local/recipes-example/inference/inference.bb`

   .. code-block:: bitbake

      LICENSE = "CLOSED"

      SRC_URI = "\
         file://model_runner.py \
         file://deep_globe_segmentation_unet_512_512.xmodel \
      "

      RDEPENDS:${PN} = "\
         python3-opencv \
         xir \
         vart \
      "

      do_install() {
            install -d ${D}/dpu-inference
            install -m 0644 ${WORKDIR}/model_runner.py ${D}/dpu-inference
            install -m 0644 ${WORKDIR}/deep_globe_segmentation_unet_512_512.xmodel ${D}/dpu-inference
      }

      FILES:${PN} += "/dpu-inference/*"

#. Add new packages into Linux image by editing :file:`~/antelope-linux-1/sources/meta-local/recipes-antelope/images/antelope-minimal-image.bbappend`

   .. code-block:: bitbake

        IMAGE_INSTALL += "\
           fpga-manager-script \
           double-uart \
           antelope-dpu \
           vitis-ai-library \
           kernel-module-xlnx-dpu \
           inference \
        "

#. Build firmware and image

   .. code-block:: shell-session

       machine:~/antelope-linux-1/build$ bitbake antelope-all

#. Prepare build artifacts for transfer to EGSE Host

   .. code-block:: shell-session

        machine:~/antelope-linux-1/build$ mkdir -p ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/bootbins/boot-firmware.bin ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/u-boot-scripts/boot-script-pins/boot-pins.scr ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/system.dtb ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/Image ../egse-host-transfer
        machine:~/antelope-linux-1/build$ cp tmp/deploy/images/antelope/antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot ../egse-host-transfer

#. Transfer content of :file:`egse-host-transfer` directory to EGSE Host and place it in :file:`/var/tftp/tutorial` directory

Run inference on DPU :tutorial-machine:`EGSE Host`
--------------------------------------------------
#. Upload few images from DeepGlobe dataset (:ref:`tutorial_files`) to run inference on to EGSE Host and place them in :file:`~/inference-input` directory. Use patched files (512x512).

#. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 128M
       -rw-rw-r-- 1 customer customer  22M Jan 29 08:19 Image
       -rw-rw-r-- 1 customer customer 114M Jan 29 08:20 antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer 1.6M Jan 29 08:20 boot-firmware.bin
       -rw-rw-r-- 1 customer customer 2.8K Jan 29 08:20 boot-pins.scr
       -rw-rw-r-- 1 customer customer  37K Jan 29 08:20 system.dtb

       customer@egse-host:~$ ls -lh ~/inference-input
       total 225K
       -rw-rw-r-- 1 customer customer 71K Jan 30 07:58 207743_04_02_sat.jpg
       -rw-rw-r-- 1 customer customer 77K Jan 30 07:58 207743_04_03_sat.jpg
       -rw-rw-r-- 1 customer customer 76K Jan 30 07:58 21717_04_02_sat.jpg

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``antelope-minimal-image-antelope.rootfs.cpio.gz.u-boot`` shall be about ~110MB)

   .. note:: You can choose different images to run inference on.

#. Power on Antelope

   .. code-block:: shell-session

       customer@egse-host:~$ sml power on
       Powering on...Success

#. Power on DPU

   .. code-block:: shell-session

       customer@egse-host:~$ sml dpu power on
       Powering on...Success

#. Open second SSH connection to EGSE Host and start ``minicom`` to observe boot process

   .. code-block:: shell-session

       customer@egse-host:~$ minicom -D /dev/sml/antelope-dpu-uart

   Leave this terminal open and get back to SSH connection used in previous steps.

#. Release DPU from reset

   .. code-block:: shell-session

      customer@egse-host:~$ sml dpu reset off 7

   .. note:: Boot firmware is the same as in :doc:`enable_pl_support`.

#. DPU boot process should be visible in ``minicom`` terminal

#. Transfer images from EGSE Host to DPU

   .. code-block:: shell-session

      customer@egse-host:~$ scp -r ~/inference-input dpu:/tmp/inference-input
      Warning: Permanently added '172.20.200.100' (ED25519) to the list of known hosts.
      21717_04_02_sat.jpg                100%   76KB  16.1MB/s   00:00
      207743_04_03_sat.jpg               100%   77KB  27.1MB/s   00:00
      207743_04_02_sat.jpg               100%   70KB  29.4MB/s   00:00

#. Log in to DPU using ``root`` user

   .. code-block:: shell-session

      antelope login: root
      root@antelope:~#

#. Load DPU bitstream

   .. code-block:: shell-session

      root@antelope:~# fpgautil -o /lib/firmware/antelope-dpu/overlay.dtbo

#. Run inference. Runner creates output directory automatically.

   .. code-block:: shell-session

       root@antelope:~# python3 /dpu-inference/model_runner.py --input-dir /tmp/inference-input/ --output-dir /tmp/inference-output
       Input tensors shape: [[1, 512, 512, 3]]
       Output tensors shape: [[1, 512, 512, 7]]
       Input tensors dtype: ['xint8']
       Output tensors dtype: ['xint8']

       Processing image /tmp/inference-input/21717_04_02_sat.jpg
               Infering...
       /dpu-inference/model_runner.py:24: RuntimeWarning: overflow encountered in exp
       return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)
       /dpu-inference/model_runner.py:24: RuntimeWarning: invalid value encountered in divide
       return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)
               Rendering...
       Processing image /tmp/inference-input/207743_04_03_sat.jpg
               Infering...
               Rendering...
       Processing image /tmp/inference-input/207743_04_02_sat.jpg
               Infering...
               Rendering...

   .. note:: You can ignore "overflow encountered in exp" warning.

#. Verify that :file:`model_runner.py` produced results

   .. code-block:: shell-session

      root@antelope:~# ls -l /tmp/inference-output/
      -rw-r--r--    1 root     root         73077 Jan 30 08:17 207743_04_02_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 30 08:17 207743_04_02_sat.npy
      -rw-r--r--    1 root     root         78363 Jan 30 08:17 207743_04_03_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 30 08:17 207743_04_03_sat.npy
      -rw-r--r--    1 root     root         77827 Jan 30 08:17 21717_04_02_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 30 08:17 21717_04_02_sat.npy

   Script has produced ``.npy`` and ``.jpg`` files for each input image.

#. Transfer inference results back to EGSE Host

   .. code-block:: shell-session

      customer@egse-host:~$ scp -r dpu:/tmp/inference-output/* ~/inference-output/
      Warning: Permanently added '172.20.200.100' (ED25519) to the list of known hosts.
      207743_04_02_sat.jpg                         100%   71KB  16.2MB/s   00:00
      207743_04_02_sat.npy                         100% 7168KB  53.3MB/s   00:00
      207743_04_03_sat.jpg                         100%   77KB  32.7MB/s   00:00
      207743_04_03_sat.npy                         100% 7168KB  53.4MB/s   00:00
      21717_04_02_sat.jpg                          100%   76KB  32.9MB/s   00:00
      21717_04_02_sat.npy                          100% 7168KB  53.4MB/s   00:00

#. Download inference results from EGSE Host and review rendered images.

   .. figure:: dpu_inference/results/21717_04_02_sat.jpg
      :width: 300px

      21717_04_02_sat.jpg

   .. figure:: dpu_inference/results/207743_04_02_sat.jpg
      :width: 300px

      207743_04_02_sat.jpg

   .. figure:: dpu_inference/results/207743_04_03_sat.jpg
      :width: 300px

      207743_04_03_sat.jpg

Summary
-------
In this tutorial you've put together all pieces created in Zero to hero tutorial series. Using DPU accelerator and small Python script you've managed to run ground segementation on series of images. That involved trained, quantized and compiled model for specific architecture, Linux distribution with DPU support and Python script to run inference. You can use inference results to generate images or other processing.
