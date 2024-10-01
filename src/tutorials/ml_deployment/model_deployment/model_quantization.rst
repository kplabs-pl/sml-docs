Model quantization
==================

Goal
----
In this tutorial you will quantize a standard deep learning model into a format that operates on lower-bit data representation to achieve better inference performance.

A bit of background
-------------------
Quantization is the first step of the deployment process. Typically deep learning models operate on floating-point data, however, to improve inference performance they must be converted to work with lower-bit representation in the quantization process. A Vitis AI compatible quantizer is provided within Vitis AI deployment container. The quantied model can still be run on a standard PC machine, however, it is optimized towards deployment on the edge. Mind that this optimization process is mandatory to deploy the model to the target DPU in later steps.

Prerequisites
-------------
1. `Docker <https://www.docker.com>`_ installed.
2. Model repository and environment set up as described in :ref:`setup_project`.
3. Dataset prepared as described in :ref:`prepare_dataset`.
4. Model weights prepared as descibed in :ref:`train_model`.

Prepare for deployment :tutorial-machine:`Machine Learning Workstation`
-----------------------------------------------------------------------
1. Open and run the ``reference-designs-ml/deployment/deployment_preparation.ipynb`` notebook to prepare the quantization calibration subset and extract model weights from the checkpoint.

   The notebook will prepare model weights and a subset of train samples necessary for the quantization step of the deployment. The weights and calibration subset will be saved into ``reference-designs-ml/deployment/deployment_artifacts/deployment_inputs`` directory. Feel free to delve into the notebook and the provided code.

2. Enter the Vitis AI deployment container with the working directory volume mounted:

   .. code-block:: shell-session

        customer@ml-workstation:~/reference-designs-ml$ docker run \
            -it \
            -v "$(pwd)":/workspace \
            -e UID="$(id -u)" -e GID="$(id -g)" \
            xilinx/vitis-ai-pytorch-cpu:ubuntu2004-3.5.0.306

Model quantization :tutorial-machine:`Vitis AI Deployment Container`
--------------------------------------------------------------------

Run the following commands in the container environment.

1. Activate the desired conda environment for PyTorch models deployment:

   .. code-block:: shell-session

       vitis-ai-user@vitis-ai-container-id:/workspace$ conda activate vitis-ai-wego-torch2

2. Install necessary third-party requirements inside the conda environment:

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ pip install -r deployment/requirements-vitis-ai.txt


3. Run the quantization script. Feel free to delve into the script to learn more about quantizing PyTorch model for Vitis AI.

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ python3 -m deployment.quantize_model

   The quantized model will appear in ``reference-designs-ml/deployment/deployment_artifacts/quantization_results``. If you wish to speed up the process, you can skip this step and use the quantized model provided via git-lfs.

   .. warning::
       Mind that the quantization process is time consuming.

   .. note::
       The quantization process includes evaluation of the quantized model. If you wish to skip this step to speed up the process pass an extra flag that will limit the number of test samples.

       .. code-block:: shell-session

           (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ python3 -m deployment.quantize_model --quantization-samples-num-limit 1

Evaluate the quantized model metrics :tutorial-machine:`Machine Learning Workstation`
-------------------------------------------------------------------------------------
1. Optionally you can evaluate the quantized model metrics by running the ``reference-designs-ml/deployment/calc_quantized_metrics.ipynb`` notebook (outside of the docker environment).

