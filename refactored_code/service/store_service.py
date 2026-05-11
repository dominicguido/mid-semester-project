import uuid
from typing import List, Dict
import os

from openai import OpenAI


class StoreService:

    def __init__(self, data_layer) -> None:
        self.data = data_layer
        self.users = self.data.load_users()
        self.inventory = self.data.load_inventory()
        self.client = None

    def all_users(self) -> List[Dict]:
        return list(self.users)

    def all_inventory(self) -> List[Dict]:
        return list(self.inventory)

    def login(self, email: str, password: str) -> Dict:
        for user in self.users:
            if user["email"] == email and user["password"] == password:
                return user
        return {}

    def register(self, email: str, password: str) -> Dict:
    
        new_user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password": password,
            "role": "Employee"
        }

        self.users.append(new_user)
        self.data.save_users(self.users)
        return new_user

    def add_product(self, name: str, description: str, stock: int, price: float) -> Dict:

        new_product = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "stock": stock,
            "price": price
        }

        self.inventory.append(new_product)
        self.data.save_inventory(self.inventory)
        return new_product

    def delete_product(self, product_name: str):
        self.inventory = [item for item in self.inventory if item["name"] != product_name]
        self.data.save_inventory(self.inventory)

    def update_product(self, product_name: str, new_price: float, new_stock: int):
        for item in self.inventory:
            if item["name"] == product_name:
                item["price"] = new_price
                item["stock"] = new_stock
                self.data.save_inventory(self.inventory)
                return item
        return {}

    def log_sale(self, product_name: str, quantity: int) -> Dict:
        for item in self.inventory:
            if item["name"] == product_name:
                if quantity > item["stock"]:
                    return None
                item["stock"] -= quantity
                self.data.save_inventory(self.inventory)
                return item
        return {}
        
    def build_prompt(self):

        return (
            "You are an inventory assistant for a small business. "
            "Help the owner and employees manage stock, sales, and product decisions. "
            "Use simple language and give practical advice. "
            "Do not use negative words."
        )

    def ask_ai(self, messages):
        
        inventory = self.data.load_inventory()

        system_prompt = {
            "role": "system",
            "content": self.build_prompt()
        }

        full_messages = messages + [system_prompt]

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=full_messages,
            temperature=1
        )

        return response.choices[0].message.content