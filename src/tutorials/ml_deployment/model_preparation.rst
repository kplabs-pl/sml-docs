Model preparation
=================

Goal
----
In this tutorial you will:
    - Obtain and prepare satellite data for machine learning training and evaluation
    - Familiarize yourself with leveraging PyTorch to define, train, and evaluate a Vitis AI-compatible deep learning model
    - Train a deployable demo model for multiclass satellite imagery land cover segmentation

A bit of background
-------------------
Typically deep learning models are defined and trained on GPU-enabled workstations using PyTorch or TensorFlow libraries workflow. These models are suboptimal for inference on the edge, however, using Vitis AI they can be converted into a format that's suitable for running on the edge with FPGA-based hardware acceleration.

Before we deploy and run any model on an edge device, we first need to develop and train it on a PC machine using either PyTorch or TensorFlow.

This tutorial demonstrates training of a land cover segmentation UNet model with ResNet encoder implemented in PyTorch. The model produced in this step is later used for deployment to the edge.

Prerequisites
-------------
* Git with `git-lfs <https://git-lfs.github.com>`_ installed.
* Python installed.
* An environment with Jupyter Notebook support (for example Visual Studio Code or Jupyter Lab).

.. _setup_project:

Setup the project environment :tutorial-machine:`Machine Learning Workstation`
------------------------------------------------------------------------------

1. Clone the model repository and enter it:

   .. code-block:: shell-session

        customer@ml-workstation:~$ git clone git@git.kplabs.pl:antelope/software/linux/reference-designs-ml.git && cd reference-designs-ml

2. Create Python virtual environment:

   .. code-block:: shell-session

        customer@ml-workstation:~/reference-designs-ml$ python3 -m venv venv && source venv/bin/activate

3. Install required Python packages:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/reference-designs-ml$ pip install -r requirements.txt

.. _prepare_dataset:

Prepare the dataset :tutorial-machine:`Machine Learning Workstation`
--------------------------------------------------------------------

1. Download the dataset

   .. note::
       In the current git-lfs-based setup the dataset is downloaded using LFS, in the future when the code is moved to public GitHub repository, provide information about downloading the dataset here.

   The dataset should reside in the ``reference-designs-ml/deep_globe`` directory.

2. Split the satellite scenes in the dataset into patches by running the preprocessing script:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/reference_designs_ml$ python3 -m preprocess

.. _train_model:

Train the model :tutorial-machine:`Machine Learning Workstation`
----------------------------------------------------------------

1. Open the ``reference-designs-ml/model_training.ipynb`` Jupyter Notebook.

2. Walk through the notebook cell-by-cell. You can either execute all cells to reproduce the model training process, or just read the notebook to get accustomed with the demo use case. If you don't wish to rerun the training, feel free to use the model weights supplied in the ``reference-designs-ml/training_logs`` directory. Reading the notebook will provide you with insights into the dataset, model input output formats, metrics, and the training process.

The training checkpoint containing model weights should be located at ``reference-designs-ml/training_logs/lightning_logs/version_XXX/checkpoints/epoch=XXX-step=XXX.ckpt``.

.. note::
    You can run the training notebook in a non-interactive way and leave it for some time with:

    .. code-block:: shell-session

        customer@ml-workstation:~/reference_designs_ml$ SML_DEMO_NO_PROGRESS=1 nohup jupyter execute --inplace model_training.ipynb

    Enabling SML_DEMO_NO_PROGRESS variable will disable progress bars polluting the notebook while it's executed in the background. You can investigate the training by observing metrics log in the ``reference-designs-ml/training_logs`` directory.

.. warning::
   Mind that training the model requires GPU support and will take time (depending on your GPU it will take up to several hours).
