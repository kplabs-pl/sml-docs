Onboard inference
=================

Goal
----
In this tutorial you will:
    - Load the compiled model on the target device and prepare for inference acceleration
    - Delegate inference over a sample image to the FPGA-based accelerator onboard
    - Analyze the inference results and compare them with the ground truth

A bit of background
-------------------
The inference program that runs on the target device is responsible for loading the compiled model, preparing the input data, and delegating the inference to the FPGA-based accelerator. The program can either be written in C++ or Python, either way it will leverage the Vitis AI libraries and runtime to interact with the accelerator. For demonstrative purposes, this tutorial uses a Python script for the onboard inference.

Prerequisites
-------------
1. Set up the target device with the Vitis AI runtime and libraries by following the :doc:`/tutorials/antelope/index` series of tutorials.
2. Clone the model repository:

   .. code-block:: shell-session

        git clone git@git.kplabs.pl:antelope/software/linux/reference-designs-ml.git

   The files used in this tutorial are mainly located in the ``onboard`` directory of the repository.

3. Obtain the dataset as described in the :ref:`prepare_dataset` tutorial.
4. Obtain the compiled model and data as described in the :doc:`/tutorials/ml_deployment/model_deployment` tutorial.

.. warning::
    Make sure that the target device accelerator architecture matches the one used for model compilation (TODO: maybe add inspect commands here).

5. Make sure that you have direct access to the target device with ssh, follow the :doc:`/how_to/egse_host/forwarding_ports_to_board` tutorial to set up port forwarding.

Deploy the model
----------------

1. Copy the necessary resources (a sample data piece for the inference, the compiled model, and the provided inference runner script) to the target device (remember to replace ``<ANTELOPE_IP>`` with the IP of the target device):

   .. code-block:: shell-session
       :emphasize-lines: 4

       scp deep_globe_preprocessed/data/test_data/images/207743_04_02_sat.jpg \
           deployment/deployment_artifacts/compilation_results/deep_globe_segmentation_unet_512_512.xmodel \
           onboard/model_runner.py \
           root@<ANTELOPE_IP>:~

   .. note::
       The provided inference runner script is a Python script that uses the Vitis AI libraries to load the model and delegate the inference to the FPGA-based accelerator. The script is provided in the model repository under ``onboard/model_runner.py`` . Feel free to delve into the script to understand how the inference is performed.

Run onboard inference
---------------------

1. SSH into the target device (remember to replace ``<ANTELOPE_IP>`` with the IP of the target device):

   .. code-block:: shell-session

       ssh root@<ANTELOPE_IP>

   1. Run the inference script:

   .. code-block:: shell-session

        python model_runner.py

   The script will load the model, prepare the input data, delegate the inference to the FPGA-based accelerator, and save the results as a ``.npy`` file.

.. note::
    The inference process can be automated. Feel free to investigate and run the ``run_onboard_demo`` script (use the ``.env.example`` file to provide the Antelope IP to the script).

2. You can now disconnect from the target device (type ``exit``).

You you don't wish to repeat this process, a sample output file is provided in the ``onboard/onboard_results`` directory of the repository via git-lfs.

Analyze the results
-------------------

1. Copy the inference results back to the host machine (remember to replace ``<ANTELOPE_IP>`` with the IP of the target device):

   .. code-block:: shell-session

       scp root@<ANTELOPE_IP>:~/207743_04_02_sat.npy onboard/onboard_results/

2. Run the ``reference-designs-ml/onboard/preview_onboard_demo.ipynb`` notebook to visualize the inference results and compare them with the ground truth.
