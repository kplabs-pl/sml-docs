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
* DeepGlobe dataset (:ref:`tutorial_files`)
* SML ML Deployment tutorial files (https://github.com/kplabs-pl/sml-ml-tutorial.git)
* Python with virtual environment support installed.
* An environment with Jupyter Notebook support (for example Visual Studio Code or Jupyter Lab).

Provided outputs
----------------
Following files (:ref:`tutorial_files`) are associated with this tutorial:

* :file:`ML deployment/01 Model training/model.ckpt` - model checkpoint

.. _setup_project:

Setup the project environment :tutorial-machine:`Machine learning workstation`
------------------------------------------------------------------------------

#. Download ML data set and unpack it to :file:`~/sml-tutorials/ml-deployment/dataset`.

#. Clone SML ML Tutorial repository to :file:`~/sml-tutorials/ml-deployment/tools`.

   .. code-block:: shell-session

      customer@ml-workstation:~/sml-tutorials/ml-deployment$ git clone https://github.com/kplabs-pl/sml-ml-tutorial.git tools

#. Create folder for output files: :file:`~/sml-tutorials/ml-deployment/output``

#. Create Python virtual environment:

   .. code-block:: shell-session

        customer@ml-workstation:~/sml-tutorials/ml-deployment$ python3 -m venv venv && source venv/bin/activate

#. Install Python packages required for the model training and evaluation:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/sml-tutorials/ml-deployment/tools$ pip install -r requirements.txt

#. At this point folder structure should look like this:

   .. code-block::

        .
        ├── dataset
        │   └── deep_globe
        │       ├── test_data
        │       └── training_data
        ├── output
        ├── tools
        │   ├── 01-prepare
        │   ├── 02-train
        │   ├── 03-quantize
        │   ├── pyproject.toml
        │   ├── requirements.txt
        │   ├── requirements-vitis-ai.txt
        │   └── src
        └── venv
        

.. _prepare_dataset:

Prepare the dataset :tutorial-machine:`Machine learning workstation`
--------------------------------------------------------------------

#. The dataset images are too large to process as a whole with deep learning models. To address this, split them into smaller 512x512 pixel patches by running:

   .. code-block:: shell-session

        (venv) customer@ml-workstation:~/sml-tutorials/ml-deployment/tools$ python3 ./01-prepare/split_to_patches.py --input-dir ../dataset/deep_globe/ --output-dir ../dataset/deep_globe_patched/

.. _train_model:

Train the model :tutorial-machine:`Machine learning workstation`
----------------------------------------------------------------

#. Open the :file:`~/sml-tutorials/ml-deployment/tools/02-train/model_training.ipynb` Jupyter Notebook.

#. Walk through the notebook cell-by-cell. You can either run all cells to reproduce the model training process, or just read the notebook to get accustomed with the demo use case. If you don't wish to rerun the training, feel free to use the model weights supplied in the :file:`~/sml-tutorials/ml-deployment/tools/training_logs` directory. Reading the notebook will provide you with insights into the dataset, model input output formats, metrics, and the training process.

   The training checkpoint containing model weights should reside at :file:`~/sml-tutorials/ml-deployment/tools/training_logs/lightning_logs/version_XXX/checkpoints/epoch=XXX-step=XXX.ckpt`.

   .. note::
       You can run the training notebook in a non-interactive way and leave it for some time with:

       .. code-block:: shell-session

           customer@ml-workstation:~/sml-tutorials/ml-deployment/tools$ SML_DEMO_NO_PROGRESS=1 nohup jupyter execute --inplace model_training.ipynb

       Enabling SML_DEMO_NO_PROGRESS variable will disable progress bars polluting the notebook while it's running in the background. You can investigate the training by observing metrics log in the :file:`~/sml-tutorials/ml-deployment/tools/training_logs` directory.

   .. warning::
      Mind that training the model requires GPU support and will take time (depending on your GPU it will take up to several hours).

   After you finished either executing or reading the notebook, you can proceed to the next tutorial.

#. Copy training checkpoint file :file:`~/sml-tutorials/ml-deployment/tools/training_logs/lightning_logs/version_XXX/checkpoints/epoch=XXX-step=XXX.ckpt` to :file:`~/sml-tutorials/ml-deployment/output/02-train/model.ckpt`
