import json
from pathlib import Path
from typing import List, Dict


class StoreData:

    def __init__(self, users_path: Path, inventory_path: Path) -> None:
        self.users_path = users_path
        self.inventory_path = inventory_path

    def load_users(self) -> List[Dict]:
        if self.users_path.exists():
            with open(self.users_path, "r") as f:
                return json.load(f)
        return []

    def save_users(self, users: List[Dict]) -> None:
        with open(self.users_path, "w") as f:
            json.dump(users, f)

    def load_inventory(self) -> List[Dict]:
        if self.inventory_path.exists():
            with open(self.inventory_path, "r") as f:
                return json.load(f)
        return []

    def save_inventory(self, inventory: List[Dict]) -> None:
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f)