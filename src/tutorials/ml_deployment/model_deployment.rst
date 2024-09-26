Model deployment
================

Goal
----
In this tutorial you will:
    - Prepare a pretrained model and data for the deployment process
    - Set up Vitis AI deployment container environment
    - Deploy a pretrained PyTorch land cover segmentation model to a Vitis AI-compatible format by:
      - Quantizing the model to work with efficient numeric representation
      - Compiling the model to the format compatible with the given FPGA-based inference accelerator

A bit of background
-------------------
The deployment process differs a bit depending on the framework that was used for model training (PyTorch/Tensorflow). In this tutorial we are going to deploy a PyTorch-based land cover segmentation model for demonstrative purposes.

Prerequisites
-------------
1. Install `docker <https://www.docker.com>`_.
2. Clone the model repository: 

   .. code-block:: shell-session

        git clone git@git.kplabs.pl:antelope/software/linux/reference-designs-ml.git

3. Obtain the model and data as described in the :doc:`/tutorials/ml_deployment/model_preparation` tutorial.
4. Obtain the `arch.json` file for the desired target accelerator architecture. A sample arch file is contained within the ``reference-designs-ml`` repository.

Model quantization and compilation
----------------------------------
1. Open and run the ``deployment/deployment_preparation.ipynb`` notebook to prepare the quantization calibration subset and extract model weights from the checkpoint. Feel free to delve into the notebook and the provided code.
2. Run Vitis AI deployment container with the working directory volume mounted:

   .. code-block:: shell-session

        docker run \
            -it \
            -v "$(pwd)":/workspace \
            -e UID="$(id -u)" -e GID="$(id -g)" \
            xilinx/vitis-ai-pytorch-cpu:ubuntu2004-3.5.0.306

   Run the following commands in the container environment.

   1. Navigate to the workspace directory inside the docker container:

      .. code-block:: shell-session

          cd /workspace

   2. Activate the desired conda environment for PyTorch models deployment:

      .. code-block:: shell-session

          conda activate vitis-ai-wego-torch2

   3. Install necessary third-party requirements inside the conda environment:

      .. code-block:: shell-session

          pip install -r deployment/requirements-vitis-ai.txt


   4. Run the quantization script. Feel free to delve into the script to learn more about quantizing PyTorch model for Vitis AI.

      .. code-block:: shell-session

          python3 -m deployment.quantize_model

      The quantized model will appear in ``reference-designs-ml/deployment/deployment_artifacts/quantization_results``. If you wish to speed up the process, you can skip this step and use the quantized model provided via git-lfs.

      .. warning::
          Mind that the quantization process is time consuming.

      .. note::
          The quantization process includes evaluation of the quantized model. If you wish to skip tis step to speed up the process pass an extra flag that will limit the number of test samples.

          .. code-block:: shell-session

              python3 -m deployment.quantize_model --quantization-samples-num-limit 1

   5. Run the compiler command on the quantized model to produce the FPGA-acceleration-compatible model based on the provided ``arch.json``:

      .. code-block:: shell-session

          vai_c_xir \
              --xmodel deployment/deployment_artifacts/quantization_results/Unet_int.xmodel \
              --arch deployment/arch.json \
              --output_dir deployment/deployment_artifacts/compilation_results \
              --net_name deep_globe_segmentation_unet_512_512

      For your convinience this command is also provided in the ``deployment/compile_model`` script. The compiled model should appear in the ``deployment/deployment_artifacts/compilation_results`` directory. If you wish to skip this step it is also avilable via git-lfs.

   6. Exit the Vitis AI container (e.g. type ``exit``).

3. Optionally you can evaluate the quantized model metrics by running the ``deployment/calc_quantized_metrics.ipynb`` notebook.
