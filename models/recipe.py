from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Recipe:
    name: str
    ingredients: List[Dict]
    instructions: List[str]
    nutrition: Dict
    prep_time: int
    image_url: str = ""
    servings: int = 4
    
    def to_dict(self):
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'nutrition': self.nutrition,
            'prep_time': self.prep_time,
            'image_url': self.image_url,
            'servings': self.servings
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data) 

