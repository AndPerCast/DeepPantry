"""

"""

from jetson.inference import detectNet
from jetson.utils import videoSource
from typing import Tuple, Dict


class ObjectType:
    """
    """
    def __init__(self,
                 name: str,
                 constraint: int = 0,
                 amount: int = 0,
                 price: float = 0.0) -> None:
        self.name = name
        self.constraint = constraint
        self.amount = amount
        self.price = price

    @property
    def demand(self) -> int:
        dif = self.amount - self.constraint
        return abs(dif) if dif < 0 else 0

    def __str__(self) -> str:
        return f"""\t{self.name.title()}
        Stored: {self.amount}
        Minimum units: {self.constraint}
        Needed: {self.demand}
        Total cost: {self.amount * self.price:.2f}$
        """


class InventoryManager:
    """
    """

    def __init__(self,
                 path2model: str,
                 path2labels: str,
                 sensitivity: float,
                 input_uri: str,
                 path2constraints: str) -> None:
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
            self.object_names: Tuple[str, ...] = tuple(label for label in labels_file if label != "BACKGROUND")

    @property
    def inventory(self) -> Dict[str, ObjectType]:
        """
        """
        result: Dict[str, ObjectType] = {name:ObjectType(name)
                                         for name in self.object_names}
        # Count occurrences of each type within list of detected objects.
        for class_index in self._network.Detect(self._camera.Capture()):
            result[self._network.GetClassDesc(class_index)].amount += 1
        return result

    @staticmethod
    def _update_prices(inventory_data: Dict[str, int]) -> None:
        """
        """
        pass
