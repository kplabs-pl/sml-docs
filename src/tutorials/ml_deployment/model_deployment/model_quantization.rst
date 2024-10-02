Model quantization
==================

Goal
----
In this tutorial you will quantize a standard deep learning model into a format that operates on lower-bit data representation to achieve better inference performance.

A bit of background
-------------------
Quantization is the first step of the deployment process. Typically deep learning models operate on floating-point data, however, to improve inference performance they must be converted to work with lower-bit representation in the quantization process. A Vitis AI compatible quantizer is provided within Vitis AI deployment container. The quantized model can still be run on a standard PC machine, however, it's optimized towards deployment on the edge. Mind that this optimization process is mandatory to deploy the model to the target DPU in later steps.

Prerequisites
-------------
1. `Docker <https://www.docker.com>`_ installed.
2. Model repository and environment set up as described in :ref:`setup_project`.
3. Dataset prepared as described in :ref:`prepare_dataset`.
4. Model weights prepared as described in :ref:`train_model`.

Prepare for deployment :tutorial-machine:`Machine Learning Workstation`
-----------------------------------------------------------------------
1. The quantization process requires model weights and a subset (100 to 1000 samples) of the training dataset to calibrate the model. This process is done in the Vitis AI deployment container which is a constrained environment. To simplify this step, the fully preprocessed calibration subset and model weights are prepared in advance.

   Open and run the ``reference-designs-ml/deployment/deployment_preparation.ipynb`` Jupyter Notebook to save calibration data and weights to ``reference-designs-ml/deployment/deployment_artifacts/deployment_inputs`` directory.

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

2. Install third-party modules required to run the model inside the container environment:

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ pip install -r deployment/requirements-vitis-ai.txt


3. Quantize the model using Vitis AI Python libraries. The quantizer is created using ``pytorch_nndct.apis.torch_quantizer``, which operates in two modes: ``"calib"`` and ``"test"``. The first one is used to calibrate the model to work in lower-bit precision. The second one is used to evaluate and export the quantized model for further deployment.

   This process is performed by running the quantization script (remember that the demo model works with 512 by 512 3-channel images and 7 output classes):

   .. code-block:: shell-session

       (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ python3 -m deployment.quantize_model \
           --input-size 3 512 512 \
           --num-classes 7 \
           --calib-batch-size 8 \
           --input-dir deployment/deployment_artifacts/deployment_inputs \
           --output-dir deployment/deployment_artifacts/quantization_results

   The quantized model will appear in ``reference-designs-ml/deployment/deployment_artifacts/quantization_results``. If you wish to speed up the process, you can skip this step and use the quantized model provided via git-lfs.

   .. warning::
       Mind that the quantization process is time consuming.

   .. note::
       The quantization process includes evaluation of the quantized model. If you wish to skip this step to speed up the process pass an extra flag that will limit the number of test samples.

       .. code-block:: shell-session

           (vitis-ai-wego-torch2) vitis-ai-user@vitis-ai-container-id:/workspace$ python3 -m deployment.quantize_model --quantization-samples-num-limit 1

   Let's walk through the quantization script to understand the process:

   1. Quantization requires to load the model first:

      .. code-block:: python3

          model = Unet(num_classes=NUM_CLASSES)
          model.load_state_dict(torch.load(input_dir / "state_dict.pt"))

   2. Then the quantizer is set up in the ``"calib"`` mode using dummy input with the same shape as the model input (in this case it's ``[3, 512, 512]``):

      .. code-block:: python3

          dummy_input = torch.randn(batch_size, *input_shape)
          quantizer = torch_quantizer("calib", model, (dummy_input), output_dir=str(output_dir))
          quant_model = quantizer.quant_model

   3. The calibration is performed by passing the calibration samples to the quantized model in a loop and the quantization results are exported:

      .. code-block:: python3

          with h5py.File(calibration_data_h5_path, "r") as f_in:
              sample_names = list(f_in["calibration"].keys())[:samples_num_limit]
              for names_batch in tqdm(batched(sample_names, batch_size)):
                  input_batch = torch.stack([torch.as_tensor(f_in[f"calibration/{name}"]) for name in names_batch])
                  quant_model(input_batch)

          quantizer.export_quant_config()

   4. After calibration the quantized model parameters can be exported with:

      .. code-block:: python3

          quantizer.export_quant_model()

   5. However, the quantized model needs to be serialized before we compile it in the next tutorial. This is done by instantiating the quantizer in the ``"test"`` mode. Test mode requires batch size to be set to 1:

      .. code-block:: python3

          dummy_input = torch.randn(batch_size, *input_shape)
          quantizer = torch_quantizer("test", model, (dummy_input), output_dir=str(output_dir))
          quant_model = quantizer.quant_model

   6. Before the model is exported, at least one sample must be passed through it in the test mode. This mode can also be used to evaluate the quantized model before it's serialized. Once the test samples are passed through, the model can finally be exported for the further deployment:

      .. code-block:: python3

          with h5py.File(test_data_h5_path, "r") as f_in, h5py.File(output_dir / "quantization_test_preds.h5", "w") as f_out:
              sample_names = list(f_in["calibration"].keys())[:samples_num_limit]
              for sample_name in tqdm(sample_names):
                  input_image = torch.as_tensor(f_in[f"test/{sample_name}"])
                  input_batch = input_image.unsqueeze(0)
                  pred = quant_model(input_batch)
                  f_out.create_dataset(sample_name, data=pred.detach())

          quantizer.export_xmodel(str(output_dir))

Evaluate the quantized model metrics :tutorial-machine:`Machine Learning Workstation`
-------------------------------------------------------------------------------------
1. The quantization script saves the calibrated model outputs in a file. Optionally you can evaluate metrics for these outputs and preview the results by running the ``reference-designs-ml/deployment/calc_quantized_metrics.ipynb`` notebook (outside of the docker environment).
