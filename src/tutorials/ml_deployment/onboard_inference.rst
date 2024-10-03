Onboard inference
=================

Goal
----
In this tutorial you will:
    - Load the compiled model on the target device and prepare for inference acceleration
    - Delegate inference over a sample image to the FPGA-based accelerator onboard
    - Analyze the inference results and compare them with the ground truth

A bit of background
-------------------
After the model is first trained and then compiled for the target device, the final step is to run the inference on the target device. However, the compiled model isn't enough to run the inference. A runner program is necessary to load the model, prepare the input data, and delegate the inference to the FPGA-based accelerator. The runner can either be written in C++ or Python, either way it will leverage the Vitis AI libraries and runtime to interact with the accelerator. For demonstrative purposes, this tutorial uses a Python script for the onboard inference.

Prerequisites
-------------
1. Set up the target device with the Vitis AI runtime and libraries by following the :doc:`/tutorials/antelope/index` series of tutorials.
2. Model repository and environment set up as described in :ref:`setup_project`.
3. Dataset prepared as described in :ref:`prepare_dataset`.
4. Model compiled as described in the :doc:`/tutorials/ml_deployment/model_deployment/model_compilation` tutorial.
5. Ssh access to the target device via the EGSE system.

Deploy the model
----------------

Copy the necessary resources (a sample data piece for the inference, the compiled model, and the provided inference runner script) to the target device (remember to replace the egsee name and with proper values, Antelope IP address is ``172.20.200.100`` by default):

1. Copy the resources to the EGSE system:

   .. code-block:: shell-session

       customer@ml-workstation:~/reference-designs-ml$ scp \
           deep_globe_patched/data/test_data/images/207743_04_02_sat.jpg \
           deployment/deployment_artifacts/compilation_results/deep_globe_segmentation_unet_512_512.xmodel \
           onboard/model_runner.py \
           customer@egse-my-egse.egse.sml.lan:~/ml_workspace/

2. Log into the EGSE system:

   .. code-block:: shell-session

       customer@ml-workstation:~/reference-designs-ml$ ssh customer@egse-my-egse.egse.sml.lan

3. Copy the resources from the EGSE system to the DPU target device:

   .. code-block:: shell-session

       customer@egse-my-egse:~$ scp -r ml_workspace root@172.20.200.100:~

4. Log into the DPU target device:

   .. code-block:: shell-session

       customer@egse-my-egse:~$ ssh root@172.20.200.100

.. note::
    The provided inference runner script is a Python script that uses the Vitis AI libraries to load the model and delegate the inference to the FPGA-based accelerator. The script is provided in the model repository under ``reference-designs-ml/onboard/model_runner.py``. Feel free to delve into the script to understand how the inference is performed.

Run onboard inference :tutorial-machine:`DPU Board`
---------------------------------------------------

Make sure that you remain logged into the target DPU board.

1. Go to the workspace directory on the DPU board:

   .. code-block:: shell-session

       root@antelope:~# cd ml_workspace

2. Run the inference script:

   .. code-block:: shell-session

       root@antelope:~/ml_workspace# python3 -m model_runner

   The script will load the model, prepare the input data, delegate the inference to the FPGA-based accelerator, and save the results to the ``predictions`` directory as a ``.npy`` file. The ``.npy`` file will contain tensors with the inference results.

   .. warning::
       Make sure that the target device accelerator architecture matches the one used for model compilation.

       You can examine the accelerator architecture by running ``root@antelope:~/ml_workspace# xdputil xmodel -h``, and the model target architecture by running ``root@antelope:~/ml_workspace# xdputil xmodel -l deep_globe_segmentation_unet_512_512.xmodel``. Compare the values under ``DPU Arch`` in the outputs of both commands to double check that they're the same.

   Let's walk through the model runner script to understand the inference process:

   1. The script must define a model runner class that reads the ``.xmodel`` file and parses the model graph using Vitis AI provided ``xir`` and ``vart`` libraries:

      .. code-block:: python3

          def get_child_subgraph_dpu(graph: xir.Graph) -> list[xir.Subgraph]:
              assert graph is not None, "'graph' should not be None."
              root_subgraph = graph.get_root_subgraph()
              assert root_subgraph is not None, "Failed to get root subgraph of input Graph object."
              if root_subgraph.is_leaf:
                  return []
              child_subgraphs = root_subgraph.toposort_child_subgraph()
              assert child_subgraphs is not None and len(child_subgraphs) > 0
              return [cs for cs in child_subgraphs if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"]

          class Runner:
             def __init__(self, xmodel_path: str, dtype: type = np.float32):
                 self._graph = xir.Graph.deserialize(xmodel_path)
                 self._subgraph = get_child_subgraph_dpu(self._graph)
                 self._dpu_runner = vart.Runner.create_runner(self._subgraph[0], "run")

   2. The runner class must define buffers for holding model inputs and outputs. The buffers should hold the data in the format analogous to the one used during the model training and evaluation:

      .. code-block:: python3

          class Runner:
             def __init__(self, xmodel_path: str, dtype: type = np.float32):
                 ...
                 # Get input/output tensors (even if the model has only one input/output tensor, we still get them as a list)
                 self._input_tensors = self._dpu_runner.get_input_tensors()
                 self._output_tensors = self._dpu_runner.get_output_tensors()

                 # Prepare input/output buffers
                 # Notice that the buffers passed to execute_async must be in a list even though we have only one input/output
                 # tensor. If we had a model with more inputs/outputs the lists would have more elements.
                 self._input_buffers = [np.empty(t.dims, dtype=dtype, order="C") for t in self._input_tensors]
                 self._output_buffers = [np.empty(t.dims, dtype=dtype, order="C") for t in self._output_tensors]

      .. note::
          Vitis AI libraries will, by default, automatically convert the input/output data to the quantized format used internally by the model.

   3. The runner should also feature preprocessing and postprocessing methods that are analogous to the ones used during the model training and evaluation. The postprocessing method re-implements the softmax layer stripped down by the model compiler during the deployment:

      .. code-block:: python3

          class Runner:
              ...

              def preproc(self, img: np.ndarray) -> np.ndarray:
                  img = img / 255.0
                  img = img.astype(self._dtype)
                  # Our model has only one input/output so we index input buffers directly with 0 idx.
                  # Append batch dimension.
                  img.reshape(self._input_buffers[0].shape)
                  return img

              def postproc(self, img: np.ndarray) -> np.ndarray:
                  return softmax(img)

   4. Finally the main inference method runs can use the preprocessed image, place it into the input buffer, delegate the inference asynchronously to the DPU, and wait for the results:

      .. code-block:: python3

          class Runner:
              ...

              def infer(self, img: np.ndarray) -> np.ndarray:
                  img = self.preproc(img)
                  # Our model has only one input/output so we index input buffers directly with 0 idx.
                  # Place the preprocessed image into the input buffer.
                  self._input_buffers[0][:] = img[:]

                  print("Running...")
                  job_id = self._dpu_runner.execute_async(self._input_buffers, self._output_buffers)
                  self._dpu_runner.wait(job_id)
                  print("Done!")

                  out = self._output_buffers[0]
                  out = self.postproc(out)

                  return out

   5. The model can be fed with images loaded using OpenCV (mind that OpenCV defaults to BGR data layout, Vitis AI models expect RGB by default):

      .. code-block:: python3

          runner = Runner(xmodel_path, dtype)
          img = cv2.imread(str(img_path))
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          prediction = runner.infer(img)

2. You can now disconnect from the DPU board: ``exit``.

If you don't want to repeat this process, a sample output file is provided in the ``reference-designs-ml/onboard/onboard_results`` directory of the repository via git-lfs.

Download the inference results
------------------------------

After disconnecting from the DPU board, you should be back on the EGSE system.

1. Copy the inference results from the DPU board to the EGSE system:

   .. code-block:: shell-session

      customer@egse-my-egse:~$ scp -r root@172.20.200.100:~/ml_workspace/predictions ml_workspace

2. Disconnect from the EGSE system: ``exit``.

3. Copy the inference results from the EGSE system to the host machine:

   .. code-block:: shell-session

      customer@ml-workstation:~/reference-designs-ml$ scp customer@egse-my-egse:~/ml_workspace/predictions/207743_04_02_sat.npy onboard/onboard_results/

.. note::
    If you wish to simplify the DPU connection process, you can access the DPU directly by setting up :doc:`/how_to/egse_host/forwarding_ports_to_board`. After enabling forwarding, feel free to investigate and run the ``run_onboard_demo`` script to learn how to automate the inference process. Run ``customer@ml-workstation:~/reference-designs-ml$ ./onboard/run_onboard_demo`` on your host machine to deploy the model, perform the inference, and download the results in one step.

Analyze the results :tutorial-machine:`Machine Learning Workstation`
--------------------------------------------------------------------

1. Run the ``reference-designs-ml/onboard/preview_onboard_demo.ipynb`` notebook to visualize the inference results and compare them with the ground truth.
