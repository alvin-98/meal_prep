from typing import List, Dict, Optional
from datetime import datetime, date, timedelta

from .recipe import Recipe
from .ingredients import Ingredient
from services.database import Database

class MealPrepPlanner:
    def __init__(self):
        self.db = Database()
        self.load_data()
        self.nutrition_goals = {}
    
    def load_data(self):
        self.inventory = [
            Ingredient(
                name=ing['name'],
                quantity=ing['quantity'],
                unit=ing['unit'],
                expiry_date=ing['expiry_date']
            )
            for ing in self.db.get_ingredients()
        ]
        
        self.known_recipes = [
            Recipe(
                name=recipe['name'],
                ingredients=recipe['ingredients'],
                instructions=recipe['instructions'],
                nutrition=recipe['nutrition'],
                prep_time=recipe['prep_time']
            )
            for recipe in self.db.get_recipes()
        ]
    
    def add_ingredient(self, ingredient: Ingredient):
        self.db.add_ingredient(ingredient)
        self.load_data()
    
    def add_recipe(self, recipe: Recipe):
        self.db.add_recipe(recipe)
        self.load_data()

    def get_ingredient_names(self) -> List[str]:
        """
        Returns a list of all unique ingredient names currently in the inventory.
        
        Returns:
            List[str]: A sorted list of unique ingredient names
        """
        return sorted(list({ingredient.name.lower() for ingredient in self.inventory}))

