Model deployment
================

Goal
----
In the following tutorials you will:
    - Prepare a pre-trained model and data for the deployment process
    - Set up Vitis AI deployment container environment
    - Deploy a pre-trained PyTorch land cover segmentation model to a Vitis AI-compatible format by:
       - quantizing the model to work with efficient numeric representation
       - compiling the model to the format compatible with the given FPGA-based inference accelerator

.. note:
    The files used in these tutorials are mainly located in the ``deployment`` directory of the `reference-designs-ml` repository.

A bit of background
-------------------
A model trained using PyTorch or TensorFlow isn't suitable to be run on the edge out-of-the-box. It needs to undergo conversion process that will enable efficient inference on the target DPU platform. The deployment process contains two steps: quantization and compilation. Quantization converts model to work in efficient data representation. Compilation translates the model architecture into FPGA-based accelerator compatible format.

The deployment process differs a bit depending on the framework that was used for model training (PyTorch/Tensorflow). This tutorials covers deployment of a PyTorch-based land cover segmentation model for demonstrative purposes.

Model deployment steps
----------------------
Proceed to the following tutorials on quantization and compilation to learn how to deploy a deep learning model to a DPU.

.. toctree::
    :maxdepth: 1

    model_quantization
    model_compilation
