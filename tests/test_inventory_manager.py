"""Unit Testing for inventory_manager module.

Author:
    Andrés Pérez
"""

import unittest
from unittest.mock import patch
from random import randint
import csv
import sys
from os.path import join, dirname, isfile
from os import remove

# Add tested modules to Python path.
sys.path.insert(0, join(dirname(dirname(__file__)), "src"))

from inventory_manager import ProductType, InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Tests inventory_manager functionality"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory_data = {
            "honey": ProductType("honey"),
            "water": ProductType("water"),
        }
        cls.classes = tuple(cls.inventory_data.keys()) 
        cls.path2labels: str = join(dirname(__file__), "labels.txt")
        with open(cls.path2labels, "w", newline="") as labels_file:
            labels_file.write("BACKGROUND\n")
            labels_file.writelines(cls.classes)
        InventoryManager._PATH2CONSTRAINTS = join(dirname(__file__),
                                                  ".constraints.csv")

    @classmethod
    def tearDownClass(cls) -> None:
        remove(cls.path2labels)
        remove(InventoryManager._PATH2CONSTRAINTS)

    def setUp(self) -> None:
        mocket_detect = patch("inventory_manager.detectNet")
        self.addCleanup(mocket_detect.stop)
        mocket_detect = mocket_detect.start()

        mocket_video = patch("inventory_manager.videoSource")
        self.addCleanup(mocket_video.stop)
        mocket_video = mocket_video.start()

        self.manager = InventoryManager("", self.path2labels, "")

    def test_inventory(self) -> None:
        pass

    def test_update_constraints(self) -> None:
        sample_data1 = self.inventory_data.copy()
        for product in sample_data1.values():
            product.constraint = randint(1, 5)
        
        self.assertTrue(isfile(InventoryManager._PATH2CONSTRAINTS))
        with open(InventoryManager._PATH2CONSTRAINTS, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Class", "Constraint"])
            csv_writer.writerows([[key, value.constraint]
                                  for key, value in sample_data1.items()])

        sample_data2 = self.inventory_data.copy()
        self.manager._update_constraints(sample_data2)
        self.assertDictEqual(sample_data1, sample_data2)


if __name__ == "__main__":
    unittest.main()
