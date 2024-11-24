from datetime import datetime
from dataclasses import dataclass

@dataclass
class Ingredient:
    name: str
    quantity: float
    unit: str
    expiry_date: datetime
    
    def days_until_expiry(self) -> int:
        return (self.expiry_date - datetime.now()).days
    
    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'expiry_date': self.expiry_date.isoformat() if isinstance(self.expiry_date, datetime) else self.expiry_date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        expiry_date = data['expiry_date']
        if isinstance(expiry_date, str):
            expiry_date = datetime.fromisoformat(expiry_date)
        elif not isinstance(expiry_date, datetime):
            raise ValueError(f"Unexpected expiry_date type: {type(expiry_date)}")
        
        return cls(
            name=data['name'],
            quantity=data['quantity'],
            unit=data['unit'],
            expiry_date=expiry_date
        ) 