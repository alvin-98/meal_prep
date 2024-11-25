from dataclasses import dataclass

@dataclass
class Nutrition:
    recipe_id: int
    calories: int
    protein: int
    carbs: int
    fiber: int
    sodium: int
    fat: int
    cholesterol: int
    
