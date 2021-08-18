"""

"""

from jetson.inference import detectNet
from jetson.utils import videoSource
from os.path import join, dirname, isfile
import csv
from price_scraper import scrape_price
from typing import Tuple, Dict


class ObjectType:
    """
    """
    def __init__(self,
                 class_name: str,
                 amount: int = 0,
                 constraint: int = 0,
                 price: float = 0.0) -> None:
        # TODO additional fields, class name refactoring
        self.class_name = class_name
        self.constraint = constraint
        self.amount = amount
        self.price = price

    @property
    def demand(self) -> int:
        dif = self.amount - self.constraint
        return abs(dif) if dif < 0 else 0

    def __str__(self) -> str:
        return f"""\t{self.class_name.title()}
        Stored: {self.amount}
        Minimum units: {self.constraint}
        Needed: {self.demand}
        Total cost: {round(self.demand * self.price, 2) if self.price else ""}$
        """


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
            self.classes: Tuple[str, ...] = tuple(label for label in labels_file if label != "BACKGROUND")

        self._path2constraints: str = join(dirname(dirname(__file__)),
                                           "config", ".constraints.csv")
        if not isfile(self._path2constraints):
            with open(self._path2constraints, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Class", "Constraint"])
                csv_writer.writerows([[class_name, 0] for class_name in self.classes])

    @property
    def inventory(self) -> Dict[str, ObjectType]:
        """
        """
        result: Dict[str, ObjectType] = {class_name:ObjectType(class_name)
                                         for class_name in self.classes}
        self._update_constraints(result)
        self._update_prices(result)
        # Count occurrences of each type within list of detected objects.
        for class_index in self._network.Detect(self._camera.Capture()):
            result[self._network.GetClassDesc(class_index)].amount += 1
        return result

    def _update_constraints(self, inventory_data: Dict[str, ObjectType]) -> None:
        """
        """
        with open(self._path2constraints, "r", newline="") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            class_header, constraint_header = next(csv_reader)
            for row in csv_reader:
                inventory_data[row[class_header]].constraint = int(row[constraint_header])

    def _update_prices(self, inventory_data: Dict[str, ObjectType]) -> None:
        """
        """
        for class_name, obj in inventory_data.items():
            try:
                # TODO check empty tuple
                _, obj.price, _ = scrape_price(class_name)
            except:
                # TODO handle requests connection error
                pass
