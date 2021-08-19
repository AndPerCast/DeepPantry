"""

"""

from jetson.inference import detectNet
from jetson.utils import videoSource
from os.path import join, dirname, isfile
import csv
from price_scraper import scrape_price
from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass
class ProductType:
    """
    """

    name: str
    amount: int = 0
    constraint: int = 0
    link: str = ""
    price: float = 0.0
    currency: str = ""

    @property
    def demand(self) -> int:
        dif = self.amount - self.constraint
        return abs(dif) if dif < 0 else 0

    @property
    def total_cost(self) -> float:
        return round(self.demand * self.price, 2)

    def __str__(self) -> str:
        return (f"\t{self.name.title()}\n"
                f"Stored: {self.amount}\n"
                f"Minimum units: {self.constraint}\n"
                f"Needed: {self.demand}\n"
                f"Current price: {self.price}{self.currency}\n"
                f"Total cost: {self.total_cost}{self.currency}\n"
                f"Purchase link: {self.link}\n")


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
            self.classes: Tuple[str, ...] = tuple(label for label in labels_file
                                                  if label != "BACKGROUND")

        self._path2constraints: str = join(dirname(dirname(__file__)),
                                           "config", ".constraints.csv")
        if not isfile(self._path2constraints):
            with open(self._path2constraints, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Class", "Constraint"])
                csv_writer.writerows([[class_name, 0]
                                      for class_name in self.classes])

    @property
    def inventory(self) -> Dict[str, ProductType]:
        """
        """
        result: Dict[str, ProductType] = {class_name:ProductType(class_name)
                                          for class_name in self.classes}
        self._update_constraints(result)
        self._update_prices(result)
        # Count occurrences of each type within list of detected objects.
        for class_index in self._network.Detect(self._camera.Capture()):
            result[self._network.GetClassDesc(class_index)].amount += 1
        return result

    def _update_constraints(self,
                            inventory_data: Dict[str, ProductType]) -> None:
        """
        """
        with open(self._path2constraints, "r", newline="") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            class_h, constraint_h = next(csv_reader)
            for row in csv_reader:
                inventory_data[row[class_h]].constraint = int(row[constraint_h])

    def _update_prices(self, inventory_data: Dict[str, ProductType]) -> None:
        """
        """
        for name, product in inventory_data.items():
            product.link, product.price, product.currency = scrape_price(name)
