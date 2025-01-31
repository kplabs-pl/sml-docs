Onboard model runner in Python
==============================

Goal
----
This tutorial will guide you through creating inference model runner in Python. You can later use it to run inference on data processing unit like Leopard or Antelope.

A bit of background
-------------------
Script running inference have to perform series of steps to get final result:

1. Load model graph
2. Instantiate VART runner with correct subgraph
3. Load input data
4. Preprocess input data (for example: normalize)
5. Reshape data to match input tensor
6. Run inference
7. Post-process output data (for example: apply softmax)
8. Save predictions for further processing.

Usage of VART runner means that final script will run **only** on machine w Deep-learning Processor Unit.

Create runner object
--------------------
#. Create empty file :file:`model_runner.py`. All steps in this tutorial will add pieces of code to that file.
#. Add ``Runner`` class that will wrap entire inference process.

   .. code-block:: python

        class Runner:
            def __init__(self) -> None:
                pass

#. Load compiler model

   .. code-block:: python

        from pathlib import Path

        import xir

        XMODEL_PATH = Path(__file__).parent / "deep_globe_segmentation_unet_512_512.xmodel"


        class Runner:
            def __init__(self) -> None:
                self._graph = xir.Graph.deserialize(str(XMODEL_PATH))

#. Locate subgraph that represent inference performed on Deep learning Processor Unit

   .. code-block:: python

        class Runner:
            def __init__(self) -> None:
                self._graph = xir.Graph.deserialize(str(XMODEL_PATH))
                self._subgraph = self._get_child_subgraph_dpu()

            def _get_child_subgraph_dpu(self) -> list[xir.Subgraph]:
                root_subgraph = self._graph.get_root_subgraph()
                assert root_subgraph is not None, "Failed to get root subgraph of input Graph object."
                if root_subgraph.is_leaf:
                    return []
                child_subgraphs = root_subgraph.toposort_child_subgraph()
                assert child_subgraphs is not None and len(child_subgraphs) > 0
                return [cs for cs in child_subgraphs if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"]

#. Create VART Runner object capable of interacting with Deep learning Processor Unit

   .. code-block:: python

        ...

        import vart

        ...

        class Runner:
            def __init__(self) -> None:
                ...

                self._dpu_runner = vart.Runner.create_runner(self._subgraph[0], "run")

#. Check shape of input and output tensors

   .. code-block:: python

        class Runner:
            def __init__(self) -> None:
                ...

                # Get input/output tensors (even if the model has only one input/output tensor, we still get them as a list)
                self._input_tensors = self._dpu_runner.get_input_tensors()
                self._output_tensors = self._dpu_runner.get_output_tensors()

                print(
                    f"Input tensors shape: {[t.dims for t in self._input_tensors]}\n",
                    f"Output tensors shape: {[t.dims for t in self._output_tensors]}\n",
                    f"Input tensors dtype: {[t.dtype for t in self._input_tensors]}\n",
                    f"Output tensors dtype: {[t.dtype for t in self._output_tensors]}\n",
                )

Add pre- and post processing
----------------------------
#. Preprocess input data by scaling it to range [0, 1] and reshaping to match input tensor shape.

   .. code-block:: python

        ...

        import numpy as np

        ...

        class Runner:
            ...

            def _preprocess(self, img: np.ndarray) -> np.ndarray:
                img = img / 255.0
                img = img.astype(np.float32)
                # Our model has only one input/output so we index input buffers directly with 0 idx.
                # Append batch dimension.
                img.reshape(self._input_tensors[0].dims)
                return img

#. Post process output data by applying softmax function

   .. code-block::  python

        ...

        def softmax(image: np.ndarray, classes_axis: int = -1) -> np.ndarray:
            return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)

        class Runner:
            ...

            def _postprocess(self, data: np.ndarray) -> np.ndarray:
                return softmax(data)

Run inference
-------------
#. Run inference using VART runner applying pre- and post processing functions.

   .. code-block:: python

        ...

        class Runner:
            ...

            def infer(self, img: np.ndarray) -> np.ndarray:
                img = self._preprocess(img)

                output = np.empty(self._output_tensors[0].dims, dtype=np.float32, order="C")
                job_id = self._dpu_runner.execute_async([img], [output])
                self._dpu_runner.wait(job_id)

                output = self._postprocess(output)
                return output

Process input files and generate output
---------------------------------------
#. Iterate over each file in input directory

   .. code-block:: python

        ...

        def main(input_dir: Path, input_glob: str, output_dir: Path) -> None:
            output_dir.mkdir(exist_ok=True, parents=True)
            runner = Runner()

            for img_path in input_dir.glob(input_glob):
                print(f'Processing image {img_path}')

#. Load each image and convert color scheme to RGB

   .. code-block:: python

        ...
        import cv2
        ...

        def main(input_dir: Path, input_glob: str, output_dir: Path) -> None:
            ...
            for img_path in input_dir.glob(input_glob):
                print(f'Processing image {img_path}')
                img = cv2.imread(str(img_path))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#. Run inference on each image and save prediction to output file

   .. code-block:: python

        ...

        def main(input_dir: Path, input_glob: str, output_dir: Path) -> None:
            ...
            for img_path in input_dir.glob(input_glob):
                print(f'Processing image {img_path}')
                img = cv2.imread(str(img_path))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                print('\tInfering...')
                prediction = runner.infer(img)
                np.save(output_dir / img_path.stem, prediction)

#. Generate output image with highlighted segmentation results

   .. code-block:: python

        ...

        COLOR_MAP = np.array([
            (0, 255, 255),    # Urban land
            (255, 255, 0),    # Agriculture land
            (255, 0, 255),    # Rangeland
            (0, 255, 0),      # Forest land
            (0, 0, 255),      # Water
            (255, 255, 255),  # Barren land
            (0, 0, 0)         # Unknown
        ], dtype=np.uint8)

        def main(input_dir: Path, input_glob: str, output_dir: Path) -> None:
            ...
            for img_path in input_dir.glob(input_glob):
                print(f'Processing image {img_path}')
                img = cv2.imread(str(img_path))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                print('\tInfering...')
                prediction = runner.infer(img)
                np.save(output_dir / img_path.stem, prediction)

                print('\tRendering...')
                classes = np.argmax(prediction[0], axis=2)
                colors = COLOR_MAP[classes]
                colored_image = (img * 0.7 + colors * 0.3).astype(np.uint8)
                colored_image = cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(output_dir / img_path.with_suffix('.jpg').name), colored_image)

#. Add command line arguments parsing

   .. code-block:: python

        ...

        import argparse

        ...

        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("--input-dir", type=Path)
            parser.add_argument("--input-glob", type=str, default="*.jpg")
            parser.add_argument("--output-dir", type=Path)
            args = parser.parse_args()
            main(args.input_dir, args.input_glob, args.output_dir)

#. You can review entire script in :download:`model_runner.py<onboard_model_runner_python/model_runner.py>`.

Summary
-------
You've created script that reads image files, runs necessary processing and pushes data to Deep learning Processor Unit. To actually use this script, go to :doc:`Leopard: Onbooard inference</tutorials/leopard/zero_to_hero/dpu_inference>` to learn how to deploy it on target device.
