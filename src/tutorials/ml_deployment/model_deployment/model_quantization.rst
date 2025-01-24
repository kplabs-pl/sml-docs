Model quantization
==================

Goal
----
In this tutorial you will quantize a standard deep learning model into a format that operates on lower-bit data representation to achieve better inference performance.

A bit of background
-------------------
Quantization is the first step of the deployment process. Typically deep learning models operate on floating-point data. However, to improve inference performance it's necessary to convert them to work with lower-bit representation during the quantizaiton. Vitis AI provides a quantizer tool inside the deployment container. You can still run the quantized model on a standard PC, however, it's optimized towards deployment on the edge. Mind that this optimization process is mandatory to deploy the model to the target DPU in later steps.

Prerequisites
-------------
* `Docker <https://www.docker.com>`_ installed.
* Model repository and environment set up as described in :ref:`setup_project`.
* Dataset prepared as described in :ref:`prepare_dataset`.
* Model weights prepared as described in :ref:`train_model`.

Provided outputs
----------------
Following files (:ref:`tutorial_files`) are associated with this tutorial:

* :file:`ML deployment/02 Model quantization/quantization_test_preds.h5` - calibration data
* :file:`ML deployment/02 Model quantization/state_dict.pt` - model weights
* :file:`ML deployment/02 Model quantization/Unet_int.xmodel` - quantized
* :file:`ML deployment/02 Model quantization/Unet.py` - Python description of the model

Due to file size following files are available separately:

* :file:`ML deployment/02 Model quantization/quantization_samples.h5` - calibration data (TODO)

Prepare for deployment :tutorial-machine:`Machine learning workstation`
-----------------------------------------------------------------------
#. The quantization process requires model weights and a subset (100 to 1000 samples) of the training dataset to calibrate the model. To avoid preprocessing the dataset for quantization inside the container, run the following command to prepare the calibration samples and model weights in advance:

   Open and run the :file:`~/sml-tutorials/ml-deployment/tools/02-quantize/deployment_preparation.ipynb` Jupyter Notebook. At the end you should have two files:
     
   * :file:`output/03-quantize/quantization_samples.h5` - calibration data
   * :file:`output/03-quantize/quantization_test_preds.h5` - tests samples
   * :file:`output/03-quantize/state_dict.pt` - model weights

#. Enter the Vitis AI deployment container with the working directory volume mounted:

   .. code-block:: shell-session

        customer@ml-workstation:~/sml-tutorials/ml-deployment$ docker run \
            -it \
            -v "$(pwd)":/workspace \
            -e UID="$(id -u)" -e GID="$(id -g)" \
            xilinx/vitis-ai-pytorch-cpu:ubuntu2004-3.5.0.306

Model quantization :tutorial-machine:`Vitis AI deployment container`
--------------------------------------------------------------------

Run the following commands in the container environment.

#. Activate the desired conda environment for PyTorch models deployment:

   .. code-block:: shell-session

       vitis-ai-user@vitis-ai-container-id:/workspace/tools$ conda activate vitis-ai-wego-torch2

#. Install third-party modules required to run the model inside the container environment:

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace/tools$ pip install -r deployment/requirements-vitis-ai.txt


#. Quantize the model using Vitis AI Python libraries. The ``pytorch_nndct.apis.torch_quantizer`` function creates the quantizer which operates in two modes: ``"calib"`` and ``"test"``. The first one calibrates the model to work in lower-bit precision. The second one evaluates and exports the quantized model for further deployment.

   Perform quantization by running the following script (remember that the demo model works with 512 by 512 3-channel images and 7 output classes):

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace/tools$ python3 ./03-quantize/quantize_model.py \
            --input-size 3 512 512 \
            --num-classes 7 \
            --calib-batch-size 8 \
            --state-dict ../output/03-quantize/state_dict.pt \
            --quantization-samples ../output/03-quantize/quantization_samples.h5 \
            --test-samples ../output/03-quantize/quantization_test_preds.h5 \
            --output-dir ../output/03-quantize/ \

   The quantized model will appear in :file:`~/sml-tutorials/ml-deployment/output/03-quantize/`.

   .. warning::
       Mind that the quantization process is time consuming.

   .. note::
       The quantization process includes evaluation of the quantized model. If you wish to skip this step to speed up the process pass an extra flag that will limit the number of test samples.

       .. code-block:: shell-session

           (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace/tools$ python3 ./03-quantize/quantize_model.py --quantization-samples-num-limit 1 ...

   Walk through the quantization script to understand the process:

   1. Quantization requires to load the model from :file:`state_dict.pt` file first:

      .. code-block:: python3

          model = Unet(num_classes=NUM_CLASSES)
          model.load_state_dict(torch.load(state_dict))

   2. Use the quantizer in the ``"calib"`` mode to quantize the model. You have to pass a dummy sample with proper input shape (in this case it's ``[batch_size, 3, 512, 512]``) to initialize the quantizer:

      .. code-block:: python3

          dummy_input = torch.randn(batch_size, *input_shape)
          quantizer = torch_quantizer("calib", model, (dummy_input), output_dir=str(output_dir))
          quant_model = quantizer.quant_model

   3. The script performs the quantization by passing the calibration samples from :file:`quantization_samples.h5` to the model in a loop:

      .. code-block:: python3

          with h5py.File(data_h5_path, "r") as f_in:
              sample_names = list(f_in["calibration"].keys())[:samples_num_limit]
              for names_batch in tqdm(batched(sample_names, batch_size)):
                  input_batch = torch.stack([torch.as_tensor(f_in[f"calibration/{name}"]) for name in names_batch])
                  quant_model(input_batch)

   5. After calibration, export the quantized model parameters using:

      .. code-block:: python3

          quantizer.export_quant_model()

   6. However, Vitis AI requires to serialize the model before it can undergo compilation. Set up the quantizer in the ``"test"`` mode to enable model export. The test mode requires batch size equal to 1:

      .. code-block:: python3

          dummy_input = torch.randn(batch_size, *input_shape)
          quantizer = torch_quantizer("test", model, (dummy_input), output_dir=str(output_dir))
          quant_model = quantizer.quant_model

   7. Vitis AI quantizer requires to infer at least one sample from :file:`output/03-quantize/quantization_test_preds.h5` in the ``test`` mode before saving the model. You can also evaluate the quantized model in the test mode before it's serialized:

      .. code-block:: python3

          with h5py.File(test_data_h5_path, "r") as f_in, h5py.File(test_samples, "w") as f_out:
              sample_names = list(f_in["calibration"].keys())[:samples_num_limit]
              for sample_name in tqdm(sample_names):
                  input_image = torch.as_tensor(f_in[f"test/{sample_name}"])
                  input_batch = input_image.unsqueeze(0)
                  pred = quant_model(input_batch)
                  f_out.create_dataset(sample_name, data=pred.detach())

   8. Once the model performs inference in the test mode, the quantizer can export it to the ``.xmodel`` format for the further deployment:

      .. code-block:: python3

          quantizer.export_xmodel(str(output_dir))

#. Exit the Vitis AI container: ``exit``.

Evaluate the quantized model metrics :tutorial-machine:`Machine learning workstation`
-------------------------------------------------------------------------------------
#. The quantization script saves the calibrated model outputs in a file. Optionally you can evaluate metrics for these outputs and preview the results by running the :file:`~/sml-tutorials/ml-deployment/tools/03-quantize/calc_quantized_metrics.ipynb` notebook.
