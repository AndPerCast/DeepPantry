"""AI-powered food inventory tracker.

This module is designed to analyze a food inventory via object recognition
techniques. Resulting data can be easily used by other applications.

Author:
    Andrés Pérez
"""

from jetson.inference import detectNet
from jetson.utils import videoSource
from os.path import join, dirname, isfile
import csv
from price_scraper import scrape_price
from dataclasses import dataclass
from typing import Tuple, Dict, List


@dataclass
class ProductType:
    """Stores information about a certain type of product.

    Attributes:
        name: Common name for a type product.
        amount: Number of available product units.
        constraint: Minimum units that should be available constantly.
        link: Purchase url.
        price: Price value.
        currency: Currency symbol.
    """

    name: str
    amount: int = 0
    constraint: int = 0
    link: str = ""
    price: float = 0.0
    currency: str = ""

    @property
    def demand(self) -> int:
        """Number of units needed to fulfill established contraint."""
        dif = self.amount - self.constraint
        return abs(dif) if dif < 0 else 0

    @property
    def total_cost(self) -> float:
        """Total cost of demanded product units."""
        return round(self.demand * self.price, 2)

    def __str__(self) -> str:
        return (f"\t{self.name.title()}\n"
                f"Stored: {self.amount}\n"
                f"Minimum units: {self.constraint}\n"
                f"Needed: {self.demand}\n"
                f"Current price: {self.price}{self.currency}\n"
                f"Total cost: {self.total_cost}{self.currency}\n"
                f"Purchase link: {self.link}\n")


class UnkownClassNameError(Exception):
    """Product class with such name is not supported."""


class InvalidConstraintError(Exception):
    """Product unit constraint value is wrong."""


class InventoryManager:
    """Analyzes a food inventory with the help of object recognition.
    
    Product data is collected from a real-time image.

    Note:
        You can get a deeper understsanding about
        class settings format under `CONFIG.md`.

        Internet connection is required to obtain real-time product prices.

    Args:
        path2model: Path to a file that contains a machine learning model.
        path2labels: Path to a file that contains class labels to be recognized.
        input_uri: Resource id for an image/camera input.
        sensitivity: Minimum confidence for an object to be detected.

    Attributes:
        classes: Names of each kind of product that might be detected.

    Example::

        >>> man = InventoryManager("../models/model.onnx", "../models/labels.txt", "/dev/video0")
        >>> print(man.inventory())
        {'honey': ProductType(name='honey', amount=3, constraint=1, link='https://shop.com/honey', price=0.73, currency='$')}

    See Also:
        https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md#input-streams
    """

    # A csv file that stores minimum number of units per product.
    _PATH2CONSTRAINTS: str = join(dirname(dirname(__file__)),
                                  "config", ".constraints.csv")

    def __init__(self,
                 path2model: str,
                 path2labels: str,
                 input_uri: str,
                 sensitivity: float = 0.5) -> None:
        self._network = detectNet(threshold=sensitivity, argv=[
            "--model=" + path2model,
            "--labels=" + path2labels,
            "--input-blob=" + "input_0",
            "--output-cvg=" + "scores",
            "--output-bbox=" + "boxes",
        ])

        self._camera = videoSource(input_uri)

        # Get available objects from labels file, skip BACKGROUND class.
        with open(path2labels, "r") as labels_file:
            classes: List[str] = []
            for line in labels_file:
                label: str = line.rstrip("\n")
                if label != "BACKGROUND":
                    classes.append(label.lower())

        self.classes: Tuple[str, ...] = tuple(classes)

        if not isfile(self._PATH2CONSTRAINTS):
            # Create default constraints for each object class.
            with open(self._PATH2CONSTRAINTS, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Class", "Constraint"])
                csv_writer.writerows([[class_name, 0]
                                      for class_name in self.classes])

    def inventory(self) -> Dict[str, ProductType]:
        """Extracts inventory information from a real-time image.

        Returns:
            Information about products which can be accessed by their name.

        Raises:
            KeyError: If internal constraints loading fails.
        """
        result: Dict[str, ProductType] = {class_name:ProductType(class_name)
                                          for class_name in self.classes}
        try:
            self._load_constraints(result)
        except KeyError:
            raise InvalidConstraintError("Invalid constraint on file.")
        self._update_prices(result)
        # Count occurrences of each type within list of detected objects.
        for obj in self._network.Detect(self._camera.Capture()):
            result[self._network.GetClassDesc(obj.ClassID)].amount += 1
        return result

    def update_constraint(self, product_name: str, constraint: int = 0) -> None:
        """
        """

        if product_name not in self.classes:
            raise UnkownClassNameError("")

        if constraint < 0:
            raise InvalidConstraintError(f"Negative constraint: {constraint}")

        with open(self._PATH2CONSTRAINTS, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            target: List[str] = [product_name, str(constraint)]
            new_data: List[List[str]] = []
            for row in csv_reader:
                new_data.append(target if target[0] == row[0] else row)
        #
        with open(self._PATH2CONSTRAINTS, "w", newline="") as csv_file:
            csv.writer(csv_file).writerows(new_data)

    def _load_constraints(self, inventory_data: Dict[str, ProductType]) -> None:
        with open(self._PATH2CONSTRAINTS, "r", newline="") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # Get column headers and update constraint field for each product.
            class_h, constraint_h = next(csv_reader)
            for row in csv_reader:
                inventory_data[row[class_h]].constraint = int(row[constraint_h])

    @staticmethod
    def _update_prices(inventory_data: Dict[str, ProductType]) -> None:
        # Get real-time prices and purchase links for each product.
        for name, product in inventory_data.items():
            product.link, product.price, product.currency = scrape_price(name)
