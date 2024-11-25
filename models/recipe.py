from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from services.database import Database

@dataclass
class Recipe:
    recipe_id: int
    recipe_name: str
    source_url: str
    prep_time: int
    image_url: str = ""
    servings: int = 1
    total_cost: float = 0.0
    
    def to_dict(self):
        return {
            'recipe_id': self.recipe_id,
            'recipe_name': self.recipe_name,
            'total_cost': self.total_cost,
            'prep_time': self.prep_time,
            'image_url': self.image_url,
            'servings': self.servings,
            'source_url': self.source_url
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data) 

    def add_recipe(self, db):
        db.add_recipe(self)

