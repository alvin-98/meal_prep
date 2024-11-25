from datetime import datetime
from dataclasses import dataclass
from typing import List
from services.database import Database

@dataclass
class Ingredient:
    name: str
    amount: float
    unit: str
    expiry_date: datetime | None = None
    original_string: str | None = None
    aisle: str | None = None
    ingredient_id: int | None = None
    recipe_id: int | None = None

    
    def days_until_expiry(self) -> int:
        return (self.expiry_date - datetime.now()).days
    
    def to_dict(self):
        return {
            'ingredient_id': self.ingredient_id,
            'name': self.name,
            'amount': self.amount,
            'unit': self.unit,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date is not None else None,
            'original_string': self.original_string,
            'aisle': self.aisle,
            'recipe_id': self.recipe_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        expiry_date = data['expiry_date']
        if isinstance(expiry_date, str):
            expiry_date = datetime.fromisoformat(expiry_date)
        elif not isinstance(expiry_date, datetime):
            raise ValueError(f"Unexpected expiry_date type: {type(expiry_date)}")
        
        return cls(
            ingredient_id=data.get('ingredient_id'),
            name=data['name'],
            amount=data['amount'],
            unit=data['unit'],
            expiry_date=expiry_date,
            original_string=data.get('original_string'),
            aisle=data.get('aisle')
        ) 

    @classmethod
    def load_inventory(cls, db) -> list['Ingredient']:
        return [
            cls(
                name=ing['name'],
                amount=ing['amount'],
                unit=ing['unit'],
                expiry_date=ing['expiry_date'],
                original_string=ing.get('original_string'),
                aisle=ing.get('aisle')
            )
            for ing in db.get_ingredients()
        ]

    @classmethod
    def get_ingredient_names(cls, db) -> List[str]:
        """
        Returns a list of all unique ingredient names currently in the inventory.
        
        Args:
            db: Database instance to fetch ingredients from
            
        Returns:
            List[str]: A sorted list of unique ingredient names
        """
        ingredients = cls.load_inventory(db)
        return sorted(list({ingredient.name.lower() for ingredient in ingredients}))
