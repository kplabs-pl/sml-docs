Model deployment
================

.. toctree::
    :hidden:

    model_quantization
    model_compilation


Goal
----
In the following tutorials you will:
    - Prepare a pre-trained model and data for the deployment process
    - Set up Vitis AI deployment container environment
    - Deploy a pre-trained PyTorch land cover segmentation model to a Vitis AI-compatible format by:
       - quantizing the model to work with efficient numeric representation
       - compiling the model to the format compatible with the given FPGA-based inference accelerator

A bit of background
-------------------
A model trained using PyTorch or TensorFlow isn't suitable for running on a DPU unit out-of-the-box. It needs to undergo conversion process that will enable efficient inference on the target DPU platform. The deployment process contains two steps: quantization and compilation. Quantization converts model to work in efficient data representation. Compilation translates the model architecture into FPGA-based accelerator compatible format.

The deployment process differs a bit depending on the framework used for model training (PyTorch/Tensorflow). This tutorials covers deployment of a PyTorch-based land cover segmentation model for demonstrative purposes.

Model deployment steps
----------------------
Proceed to the :doc:`model_quantization` and :doc:`model_compilation` tutorials to learn how to deploy a deep learning model to a DPU.
