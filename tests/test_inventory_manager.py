"""Unit Testing for inventory_manager module.

Author:
    Andrés Pérez
"""

import unittest
from unittest.mock import patch
import sys
from os.path import join, dirname
from os import remove

# Add tested modules to Python path.
sys.path.insert(0, join(dirname(dirname(__file__)), "src"))

from inventory_manager import ProductType, InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Tests inventory_manager functionality"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.classes = ("honey", "water")
        cls.path2labels: str = join(dirname(__file__), "labels.txt")
        with open(cls.path2labels, "w", newline="") as labels_file:
            labels_file.write("BACKGROUND\n")
            labels_file.writelines(cls.classes)
        InventoryManager._PATH2CONSTRAINTS = join(dirname(__file__),
                                                  ".constraints.csv")
        cls.inventory_data = {
            "honey": ProductType("honey"),
            "water": ProductType("water")
        }

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




if __name__ == "__main__":
    unittest.main()
