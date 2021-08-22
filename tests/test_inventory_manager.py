"""Unit Testing for inventory_manager module.

Author:
    Andrés Pérez
"""

import unittest
from unittest.mock import patch
from random import randint
from jetson.inference import detectNet
import csv
from typing import List
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
            labels_file.writelines("\n".join(cls.classes))
        InventoryManager._PATH2CONSTRAINTS = join(dirname(__file__),
                                                  ".constraints.csv")

    @classmethod
    def tearDownClass(cls) -> None:
        if isfile(cls.path2labels):
            remove(cls.path2labels)
        if isfile(InventoryManager._PATH2CONSTRAINTS):
            remove(InventoryManager._PATH2CONSTRAINTS)

    def setUp(self) -> None:
        self.mocket_detectnet = patch("inventory_manager.detectNet")
        self.addCleanup(self.mocket_detectnet.stop)
        self.mocket_detectnet = self.mocket_detectnet.start()

        self.mocket_video = patch("inventory_manager.videoSource")
        self.addCleanup(self.mocket_video.stop)
        self.mocket_video = self.mocket_video.start()

        self.manager = InventoryManager("", self.path2labels, "")

    def test_inventory(self) -> None:
        with patch("inventory_manager.InventoryManager._update_constraints"), \
             patch("inventory_manager.InventoryManager._update_prices"):
            # Generate an inventory with random number of product units.
            sample_data = self.inventory_data.copy()
            for product in sample_data.values():
                product.amount = randint(1, 5)

            # Generate a sample list of objects detected by an AI model.
            detections: List[detectNet.Detection] = []
            for index, class_name in enumerate(self.classes):
                obj = detectNet.Detection()
                obj.ClassID = index
                product = sample_data[class_name]
                detections.extend([obj] * product.amount)

            # Set up mocks' behaviour, note "()" to use upper level mocks.
            self.mocket_detectnet().Detect.return_value = detections
            self.mocket_detectnet().GetClassDesc.side_effect = lambda id: self.classes[id]
            self.assertDictEqual(sample_data, self.manager.inventory)

    def test_update_constraints(self) -> None:
        # Check if a default constraints file was created.
        self.assertTrue(isfile(InventoryManager._PATH2CONSTRAINTS))
        # Check if default constraint are loaded correctly.
        sample_data1 = self.inventory_data.copy()
        self.manager._update_constraints(sample_data1)
        self.assertDictEqual(self.inventory_data, sample_data1)

        # Generate a file with random constraints per product.
        sample_data2 = self.inventory_data.copy()
        for product in sample_data2.values():
            product.constraint = randint(1, 5)
        with open(InventoryManager._PATH2CONSTRAINTS, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Class", "Constraint"])
            csv_writer.writerows([[key, value.constraint]
                                  for key, value in sample_data2.items()])

        # Check if non-default constraints are loaded correctly.
        sample_data3 = self.inventory_data.copy()
        self.manager._update_constraints(sample_data3)
        self.assertDictEqual(sample_data2, sample_data3)

        # Reset constraints file.
        remove(InventoryManager._PATH2CONSTRAINTS)


if __name__ == "__main__":
    unittest.main()
