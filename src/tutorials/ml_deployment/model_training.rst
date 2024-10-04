Model training
==============

Goal
----
In this tutorial you will:
    - Obtain and prepare satellite data for machine learning training and evaluation
    - Familiarize yourself with leveraging PyTorch to define, train, and evaluate a Vitis AI-compatible deep learning model
    - Train a deployable demo model for multiclass satellite imagery land cover segmentation

A bit of background
-------------------
It's common to develop and train deep learning models on GPU-enabled workstations using PyTorch or TensorFlow libraries workflow. These models aren't optimized for inference on the edge devices that differ from standard desktop computers. However, using Vitis AI you can convert deep learning models into a format that's suitable for running on the edge with FPGA-based hardware acceleration. Before deploying the model to the edge, train it on a PC machine using either PyTorch or TensorFlow.

This tutorial demonstrates training of a land cover segmentation UNet model with ResNet encoder implemented in PyTorch. If you are a seasoned machine learning engineer, the process presented in this tutorial step will be familiar to you. After training the model, you can proceed to the next tutorial to deploy it to the edge.

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

3. Install Python packages required for the model training and evaluation:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/reference-designs-ml$ pip install -r requirements.txt

.. _prepare_dataset:

Prepare the dataset :tutorial-machine:`Machine Learning Workstation`
--------------------------------------------------------------------

1. Download the dataset

   .. note::
      TODO: Now the repository contains the dataset using git-lfs. Consider moving it to a normal storage and provide a download link.

   The dataset should reside in the ``reference-designs-ml/deep_globe`` directory.

2. The dataset images are too large to process as a whole with deep learning models. To address this, split them into smaller 512x512 pixel patches by running:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/reference_designs_ml$ python3 -m split_to_patches --patch-size 512 --input-dir deep_globe --output-dir deep_globe_patched

.. _train_model:

Train the model :tutorial-machine:`Machine Learning Workstation`
----------------------------------------------------------------

1. Open the ``reference-designs-ml/model_training.ipynb`` Jupyter Notebook.

2. Walk through the notebook cell-by-cell. You can either execute all cells to reproduce the model training process, or just read the notebook to get accustomed with the demo use case. If you don't wish to rerun the training, feel free to use the model weights supplied in the ``reference-designs-ml/training_logs`` directory. Reading the notebook will provide you with insights into the dataset, model input output formats, metrics, and the training process.

   The training checkpoint containing model weights should reside at ``reference-designs-ml/training_logs/lightning_logs/version_XXX/checkpoints/epoch=XXX-step=XXX.ckpt``.

   .. note::
       You can run the training notebook in a non-interactive way and leave it for some time with:

       .. code-block:: shell-session

           customer@ml-workstation:~/reference_designs_ml$ SML_DEMO_NO_PROGRESS=1 nohup jupyter execute --inplace model_training.ipynb

       Enabling SML_DEMO_NO_PROGRESS variable will disable progress bars polluting the notebook while it's executed in the background. You can investigate the training by observing metrics log in the ``reference-designs-ml/training_logs`` directory.

   .. warning::
      Mind that training the model requires GPU support and will take time (depending on your GPU it will take up to several hours).

   After you finished either executing or reading the notebook, you can proceed to the next tutorial.
