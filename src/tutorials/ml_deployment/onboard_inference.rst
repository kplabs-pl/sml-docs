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
After the model is first trained and then compiled for the target device, the final step is to run the inference on the target device. This process utilizes the compiled model, the FPGA accelerator, Vitis AI runtime, and a custom inference program created by the user. The inference program is responsible for loading the compiled model, preparing the input data, and delegating the inference to the FPGA-based accelerator. The program can either be written in C++ or Python, either way it will leverage the Vitis AI libraries and runtime to interact with the accelerator. For demonstrative purposes, this tutorial uses a Python script for the onboard inference.

Prerequisites
-------------
1. Set up the target device with the Vitis AI runtime and libraries by following the :doc:`/tutorials/antelope/index` series of tutorials.
2. Model repository and environment set up as described in :ref:`setup_project`
3. Dataset prepared as described in :ref:`prepare_dataset`
4. Model compiled as described in the :doc:`/tutorials/ml_deployment/model_deployment` tutorial.

5. Ssh access to the target device via the EGSE system.

Deploy the model
----------------

Copy the necessary resources (a sample data piece for the inference, the compiled model, and the provided inference runner script) to the target device (remember to replace the egsee name and ``<ANTELOPE_IP>`` with proper values):

1. Copy the resources to the EGSE system:

   .. code-block:: shell-session

       customer@ml-workstation:~/reference-designs-ml$ scp deep_globe_preprocessed/data/test_data/images/207743_04_02_sat.jpg \
           deployment/deployment_artifacts/compilation_results/deep_globe_segmentation_unet_512_512.xmodel \
           onboard/model_runner.py \
           customer@egse-my-egse.egse.sml.lan:~

2. Log into the EGSE system:

   .. code-block:: shell-session

       customer@ml-workstation:~/reference-designs-ml$ ssh customer@egse-my-egse.egse.sml.lan

3. Copy the resources from the EGSE system to the DPU target device:

   .. code-block:: shell-session

       customer@egse-my-egse:~$ scp deep_globe_preprocessed/data/test_data/images/207743_04_02_sat.jpg \
           deployment/deployment_artifacts/compilation_results/deep_globe_segmentation_unet_512_512.xmodel \
           onboard/model_runner.py \
           root@<ANTELOPE_IP>:~

4. Log into the DPU target device:

   .. code-block:: shell-session

       customer@egse-my-egse:~$ ssh root@<ANTELOPE_IP>

.. note::
    The provided inference runner script is a Python script that uses the Vitis AI libraries to load the model and delegate the inference to the FPGA-based accelerator. The script is provided in the model repository under ``reference-designs-ml/onboard/model_runner.py``. Feel free to delve into the script to understand how the inference is performed.

Run onboard inference :tutorial-machine:`DPU Board`
---------------------------------------------------

Make sure that you remain logged into the target DPU board.

1. Run the inference script:

.. code-block:: shell-session

    root@antelope:~# python -m model_runner

The script will load the model, prepare the input data, delegate the inference to the FPGA-based accelerator, and save the results as a ``.npy`` file. The ``.npy`` file will contain tensors with the inference results.

.. warning::
    Make sure that the target device accelerator architecture matches the one used for model compilation (TODO: maybe add inspect commands here).

2. You can now disconnect from the DPU board: ``exit``.

If you don't want to repeat this process, a sample output file is provided in the ``onboard/onboard_results`` directory of the repository via git-lfs.

Download the inference results
------------------------------

After disconnecting from the DPU board, you should be back on the EGSE system.

1. Copy the inference results from the DPU board to the EGSE system:

   .. code-block:: shell-session

      customer@egse-my-egse:~$ scp root@<ANTELOPE_IP>:~/207743_04_02_sat.npy .

2. Disconnect from the EGSE system: ``exit``.

3. Copy the inference results from the EGSE system to the host machine:

   .. code-block:: shell-session

      customer@ml-workstation:~/reference-designs-ml$ scp customer@egse-my-egse:~/207743_04_02_sat.npy onboard/onboard_results/

.. note::
    If you wish to simplify the DPU connection process, you can access the DPU directly by setting up :doc:`/how_to/egse_host/forwarding_ports_to_board`. After enabling forwarding, feel free to investigate and run the ``run_onboard_demo`` script (use the ``.env.example`` file to provide the Antelope IP to the script) to learn how to automate the inference process. Run ``customer@ml-workstation:~/reference-designs-ml$ ./onboard/run_onboard_demo`` on your host machine to deploy the model, perform the inference, and download the results in one step.

Analyze the results :tutorial-machine:`Machine Learning Workstation`
--------------------------------------------------------------------

1. Run the ``reference-designs-ml/onboard/preview_onboard_demo.ipynb`` notebook to visualize the inference results and compare them with the ground truth.
