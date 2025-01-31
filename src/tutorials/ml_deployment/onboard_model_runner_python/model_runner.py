from pathlib import Path

import xir
import vart
import numpy as np
import cv2
import argparse


XMODEL_PATH = Path(__file__).parent / "deep_globe_segmentation_unet_512_512.xmodel"

def softmax(image: np.ndarray, classes_axis: int = -1) -> np.ndarray:
    return np.exp(image) / np.sum(np.exp(image), axis=classes_axis, keepdims=True)

class Runner:
    def __init__(self) -> None:
        self._graph = xir.Graph.deserialize(str(XMODEL_PATH))
        self._subgraph = self._get_child_subgraph_dpu()
        self._dpu_runner = vart.Runner.create_runner(self._subgraph[0], "run")

        # Get input/output tensors (even if the model has only one input/output tensor, we still get them as a list)
        self._input_tensors = self._dpu_runner.get_input_tensors()
        self._output_tensors = self._dpu_runner.get_output_tensors()

        print(
            f"Input tensors shape: {[t.dims for t in self._input_tensors]}\n",
            f"Output tensors shape: {[t.dims for t in self._output_tensors]}\n",
            f"Input tensors dtype: {[t.dtype for t in self._input_tensors]}\n",
            f"Output tensors dtype: {[t.dtype for t in self._output_tensors]}\n",
        )

    def _get_child_subgraph_dpu(self) -> list[xir.Subgraph]:
        root_subgraph = self._graph.get_root_subgraph()
        assert root_subgraph is not None, "Failed to get root subgraph of input Graph object."
        if root_subgraph.is_leaf:
            return []
        child_subgraphs = root_subgraph.toposort_child_subgraph()
        assert child_subgraphs is not None and len(child_subgraphs) > 0
        return [cs for cs in child_subgraphs if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"]
    
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        img = img / 255.0
        img = img.astype(np.float32)
        # Our model has only one input/output so we index input buffers directly with 0 idx.
        # Append batch dimension.
        img.reshape(self._input_tensors[0].dims)
        return img
    
    def _postprocess(self, data: np.ndarray) -> np.ndarray:
        return softmax(data)
    
    def infer(self, img: np.ndarray) -> np.ndarray:
        img = self._preprocess(img)
        output = np.empty(self._output_tensors[0].dims, dtype=np.float32, order="C")
        job_id = self._dpu_runner.execute_async([img], [output])
        self._dpu_runner.wait(job_id)

        return self._postprocess(output)


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
    output_dir.mkdir(exist_ok=True, parents=True)
    runner = Runner()

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--input-glob", type=str, default="*.jpg")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    main(args.input_dir, args.input_glob, args.output_dir)
