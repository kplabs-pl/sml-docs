ML deployment
=============

The model development and deployment process is flexible, supports both PyTorch and TensorFlow. The deployment process varies depending on the model framework, and the onboard inference program can be written either in C++ or Python. The general flow of the deployment process is shown below:

.. figure:: ./deployment_flow.png
    :align: center

The following tutorials demonstrate deploying a PyTorch-based land cover segmentation model to Antelope, with the inference program written in Python.

.. toctree::
    :maxdepth: 1

    model_training
    model_deployment/index
    onboard_inference
