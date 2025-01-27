Onboard inference
=================

Goal
----
This tutorial shows how to run ground segementation on Leopard using previously prepared model and Deep learning Processor Unit accelerator.

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

* :file:`Leopard/Zero-to-hero/03 Enable programmable logic support/boot-common.bin` - Boot firmware for Leopard
* :file:`Leopard/Zero-to-hero/03 Enable programmable logic support/dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot` - Root filesystem for Leopard
* :file:`Leopard/Zero-to-hero/03 Enable programmable logic support/Image` - Linux kernel
* :file:`Leopard/Zero-to-hero/03 Enable programmable logic support/system.dtb` - Device tree

Use these files if you want to Yocto distribution by yourself.


Add inference tools to Yocto project :tutorial-machine:`Yocto`
--------------------------------------------------------------
#. Create directory :file:`~/leopard-linux-1/sources/meta-local/recipes-example/inference/inference/`
#. Copy ``model_runner.py`` to :file:`~/leopard-linux-1/sources/meta-local/recipes-example/inference/inference/`
#. Copy ``deep_globe_segmentation_unet_512_512.xmodel`` to :file:`~/leopard-linux-1/sources/meta-local/recipes-example/inference/inference/`

   This files in a quantized and compiled model from :doc:`/tutorials/ml_deployment/model_deployment/model_compilation`.

#. Create new recipe :file:`~/leopard-linux-1/sources/meta-local/recipes-example/inference/inference.bb`

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

            install -d ${D}/dpu-inference/data
            install -m 0644 ${WORKDIR}/207743_04_02_sat.jpg ${D}/dpu-inference/data
      }

      FILES:${PN} += "/dpu-inference/*"

#. Add new packages into Linux image by editing :file:`~/leopard-linux-1/sources/meta-local/recipes-leopard/images/dpu-leopard.bbappend`

   .. code-block:: bitbake

        IMAGE_INSTALL += "\
           fpga-manager-script \
           double-uart \
           dpu \
           vitis-ai-library \
           kernel-module-xlnx-dpu \
           inference \
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

Run inference on DPU :tutorial-machine:`EGSE Host`
--------------------------------------------------
#. Upload few images from DeepGlobe dataset (:ref:`tutorial_files`) to run inference on to EGSE Host and place them in :file:`~/inference-input` directory. Use patched files (512x512).

#. Verify that all necessary artifacts are present on EGSE Host:

   .. code-block:: shell-session

       customer@egse-host:~$ ls -lh /var/tftp/tutorial
       total 134M
       -rw-rw-r-- 1 customer customer  21M Jan 23 13:59 Image
       -rw-rw-r-- 1 customer customer 1.6M Jan 23 13:59 boot-common.bin
       -rw-rw-r-- 1 customer customer 121M Jan 23 13:59 dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot
       -rw-rw-r-- 1 customer customer  39K Jan 23 13:59 system.dtb

       customer@egse-host:~$ ls -lh ~/inference-input
       total 131K
       -rw-rw-r-- 1 customer customer 54K Jan 23 15:51 115444_02_02_sat.jpg
       -rw-rw-r-- 1 customer customer 42K Jan 23 15:52 140299_04_03_sat.jpg
       -rw-rw-r-- 1 customer customer 34K Jan 23 15:51 21023_01_04_sat.jpg

   .. note:: Exact file size might differ a bit but they should be in the same range (for example ``dpu-leopard-leopard-dpu.rootfs.cpio.gz.u-boot`` shall be about ~120MB)

   .. note:: You can choose different images to run inference on.

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

       customer@egse-host:~$ sml pn1 power on --nor-memory nor1
       Powering on processing node Node1...Success

#. DPU boot process should be visible in ``minicom`` terminal

#. Transfer images from EGSE Host to Processing Node

   .. code-block:: shell-session

      customer@egse-host:~$ scp -r ~/inference-input pn1:/tmp/inference-input
      Warning: Permanently added '172.20.200.100' (ED25519) to the list of known hosts.
      21023_01_04_sat.jpg                   100%   34KB   9.3MB/s   00:00
      115444_02_02_sat.jpg                  100%   53KB  16.2MB/s   00:00
      140299_04_03_sat.jpg                  100%   42KB  15.5MB/s   00:00

#. Log in to DPU using ``root`` user

   .. code-block:: shell-session

      leopard login: root
      root@leopard:~#

#. Load DPU bitstream

   .. code-block:: shell-session

      root@leopard:~# fpgautil -o /lib/firmware/dpu/overlay.dtbo

#. Run inference. Runner creates output directory automatically.

   .. code-block:: shell-session

       root@leopard-dpu:~# python3 /dpu-inference/model_runner.py --input-dir /tmp/inference-input/ --output-dir /tmp/inference-output
       Input tensors shape: [[1, 512, 512, 3]]
       Output tensors shape: [[1, 512, 512, 7]]
       Input tensors dtype: ['xint8']
       Output tensors dtype: ['xint8']

       Processing image /tmp/inference-input/140299_04_03_sat.jpg
               Infering...
       /dpu-inference/model_runner.py:24: RuntimeWarning: overflow encountered in exp
       return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)
       /dpu-inference/model_runner.py:24: RuntimeWarning: invalid value encountered in divide
       return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)
               Rendering...
       Processing image /tmp/inference-input/115444_02_02_sat.jpg
               Infering...
               Rendering...
       Processing image /tmp/inference-input/21023_01_04_sat.jpg
               Infering...
               Rendering...

   .. note:: You can ignore "overflow encountered in exp" warning.

#. Verify that :file:`model_runner.py` produced results

   .. code-block:: shell-session

      root@leopard-dpu:~# ls -l /tmp/inference-output/
      -rw-r--r--    1 root     root         94206 Jan 23 16:04 115444_02_02_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 23 16:04 115444_02_02_sat.npy
      -rw-r--r--    1 root     root         77093 Jan 23 16:04 140299_04_03_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 23 16:04 140299_04_03_sat.npy
      -rw-r--r--    1 root     root         60820 Jan 23 16:04 21023_01_04_sat.jpg
      -rw-r--r--    1 root     root       7340160 Jan 23 16:04 21023_01_04_sat.npy

   Script has produced ``.npy`` and ``.jpg`` files for each input image.

#. Transfer inference results back to EGSE Host

   .. code-block:: shell-session

      customer@egse-host:~$ scp -r pn1:/tmp/inference-output ~/inference-output
      Warning: Permanently added '172.20.200.100' (ED25519) to the list of known hosts.
      21023_01_04_sat.jpg                      100%   59KB  21.6MB/s   00:00
      21023_01_04_sat.npy                      100% 7168KB  67.6MB/s   00:00
      115444_02_02_sat.jpg                     100%   92KB  36.8MB/s   00:00
      115444_02_02_sat.npy                     100% 7168KB  68.0MB/s   00:00
      140299_04_03_sat.jpg                     100%   75KB  36.9MB/s   00:00
      140299_04_03_sat.npy                     100% 7168KB  67.8MB/s   00:00

#. Download inference results from EGSE Host and review rendered images.

   .. figure:: dpu_inference/results/21023_01_04_sat.jpg
      :width: 300px

      21023_01_04_sat.jpg

   .. figure:: dpu_inference/results/115444_02_02_sat.jpg
      :width: 300px

      115444_02_02_sat.jpg

   .. figure:: dpu_inference/results/140299_04_03_sat.jpg
      :width: 300px

      140299_04_03_sat.jpg

Summary
-------
In this tutorial you've put together all pieces created in Zero to hero tutorial series. Using DPU accelerator and small Python script you've managed to run ground segementation on series of images. That involved trained, quantized and compiled model for specific architecture, Linux distribution with DPU support and Python script to run inference. You can use inference results to generate images or other processing.
