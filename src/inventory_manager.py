"""

"""

from jetson.inference import detectNet
from jetson.utils import videoSource
from typing import Tuple, Dict


class InventoryManager:
    """
    """

    def __init__(self,
                 path2model: str,
                 path2labels: str,
                 sensitivity: float,
                 input_uri: str) -> None:
        """
        """
        self._network = detectNet(threshold=sensitivity, argv=[
            "--model=" + path2model,
            "--labels=" + path2labels,
            "--input-blob=" + "input_0",
            "--output-cvg=" + "scores",
            "--output-bbox=" + "boxes",
        ])

        self._camera = videoSource(input_uri)

        with open(path2labels, "r", newline="") as labels_file:
            self._object_names: Tuple[str, ...] = tuple(label for label in labels_file if label != "BACKGROUND")

    @property
    def inventory(self) -> Dict[str, int]:
        """
        """
        result: Dict[str, int] = {name:0 for name in self._object_names}
        # Count occurrences of each type within list of detected objects.
        for class_index in self._network.Detect(self._camera.Capture()):
            result[self._network.GetClassDesc(class_index)] += 1
        return result
