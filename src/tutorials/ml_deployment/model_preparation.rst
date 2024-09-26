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
The model training process is flexible and can vary a lot depending on the use case. This tutorial covers a demonstrative task of land cover segmentation.

Prerequisites
-------------
1. Install `git-lfs <https://git-lfs.com>`_.
2. Clone the model repository:

   .. code-block:: shell-session

        git clone git@git.kplabs.pl:antelope/software/linux/reference-designs-ml.git

2. Setup an editor that supports running Jupyter Notebooks (for example Visual Studio Code or Jupyter Lab), set your notebook server root dir to the working directory of the ``reference-designs-ml`` repository.

   * If you use VS Code, setup the notebook dir with:

     .. code-block:: json

          "jupyter.notebookFileRoot": "${workspaceFolder}",

   * If you use VS Code with remote machine, setup the notebook dir with:

     .. code-block:: json

          "jupyter.runStartupCommands": [ "%cd ${workspaceFolder}" ],

3. Make sure Python is installed.
4. Create Python virtual environment:

   .. code-block:: shell-session

        pip install virtualenv && virtualenv venv && source venv/bin/activate

5. Install required Python packages:

   .. code-block:: shell-session

        pip install -r requirements.txt

.. _prepare_dataset:

Prepare the dataset
-------------------

1. Download the dataset

   .. note::
       In the current git-lfs-based setup the dataset is downloaded using LFS, in the future when the code is moved to public GitHub repository, provide information about downloading the dataset here.

   The dataset should reside in the ``deep_globe`` directory.

2. Preprocess the dataset

   Split satellite scenes into patches:

   .. code-block:: shell-session

        python preprocess.py

Train the model
---------------

1. Open the ``model_training.ipynb`` notebook and execute it if you wish to train the model from scratch, alternatively feel free to skip the model training process and use the model weights provided in the ``training_logs`` directory.

The training checkpoint containing model weights will be located at ``reference-designs-ml/training_logs/lightning_logs/version_XXX/checkpoints/epoch=XXX-step=XXX.ckpt``.

.. note::
    You can run the training notebook in a non-interactive way and leave it for some time with: ``SML_DEMO_NO_PROGRESS=1 nohup jupyter execute --inplace model_training.ipynb``.

    Enabling SML_DEMO_NO_PROGRESS variable will disable progress bars polluting the notebook while it's executed in the background. You can investigate the training by observing metrics log in the ``training_logs`` directory.

.. warning::
   Mind that training the model requires GPU support and will take time (depending on your GPU it will take up to several hours).

.. note::
   The model training code is dependent on given use case and dataset. You training code may differ a lot from the presented demo. Nevertheless feel encouraged to delve into the provided Jupyter Notebook and use it as a reference.

.. warning::
   If you develop your custom model in the future make sure to use only `Vitis AI supported layers <https://docs.amd.com/r/en-US/ug1414-vitis-ai/Operators-Supported-by-PyTorch>`_.
