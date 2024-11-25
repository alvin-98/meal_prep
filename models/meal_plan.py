from dataclasses import dataclass
from typing import List, Dict
from models.recipe import Recipe
import pandas as pd
from services.database import Database
from models.ingredients import Ingredient
from models.nutrition import Nutrition

@dataclass
class MealPlan:
    start_date: str
    num_days: int
    breakfast: List[int]
    lunch: List[int]
    dinner: List[int]

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'MealPlan':
        """Create a MealPlan instance from a DataFrame"""
        # Get unique dates to determine start_date and num_days
        dates = pd.to_datetime(df['date'].unique())
        
        # Drop unwanted columns and filter by meal type
        recipe_df = df.drop(columns=['date', 'num_days', 'meal_type'])
        
        return cls(
            start_date=dates[0].strftime('%Y-%m-%d'),
            num_days=len(dates),
            breakfast=[row['recipe_id'] for _, row in recipe_df[df['meal_type'] == 'breakfast'].iterrows()],
            lunch=[row['recipe_id'] for _, row in recipe_df[df['meal_type'] == 'lunch'].iterrows()],
            dinner=[row['recipe_id'] for _, row in recipe_df[df['meal_type'] == 'dinner'].iterrows()]
        )

    def to_dict(self):
        return {
            'meal_plan_id': self.meal_plan_id,
            'start_date': self.start_date,
            'num_days': self.num_days,
            'breakfast': self.breakfast,
            'lunch': self.lunch,
            'dinner': self.dinner
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert meal plan to a pandas DataFrame with recipe attributes as columns and meals as rows."""
        rows = []
        dates = pd.date_range(self.start_date, periods=self.num_days)
        
        for date in dates:
            for meal_type, recipes in [('breakfast', self.breakfast), 
                                     ('lunch', self.lunch), 
                                     ('dinner', self.dinner)]:
                recipe_idx = (date - pd.Timestamp(self.start_date)).days
                recipe = recipes[recipe_idx]
                
                # Get all attributes from the recipe object
                row = vars(recipe)
                # Add date and meal_type
                row.update({
                    'date': date,
                    'meal_type': meal_type
                })
                rows.append(row)
        
        return pd.DataFrame(rows)

    def add_meal_plan(self, db, recipes_df: pd.DataFrame, nutrition_df: pd.DataFrame, ingredients_df: pd.DataFrame) -> None:
        """Save meal plan and its recipes to SQLite database"""
        # First add all recipes to the database
        for recipe_id in self.breakfast + self.lunch + self.dinner:
            if recipe_id in recipes_df.index:
                # Add recipe
                recipe_data = recipes_df.loc[recipe_id]
                recipe = Recipe(
                    recipe_id=recipe_id,
                    recipe_name=recipe_data['name'],
                    source_url=recipe_data['source_url'],
                    total_cost=recipe_data['total_cost'],
                    prep_time=recipe_data['prep_time'],
                    image_url=recipe_data['image_url'],
                    servings=recipe_data['servings']
                )
                db.add_recipe(recipe)
                
                # Add ingredients for this recipe
                recipe_ingredients = ingredients_df[ingredients_df['recipe_id'] == recipe_id]
                for _, ing_data in recipe_ingredients.iterrows():
                    ingredient = Ingredient(
                        ingredient_id=ing_data['ingredient_id'],
                        name=ing_data['name'],
                        amount=ing_data['amount'],
                        unit=ing_data['unit'],
                        original_string=ing_data['original_string'],
                        aisle=ing_data['aisle'],
                        recipe_id=recipe_id,
                        expiry_date=None
                    )
                    db.add_ingredient(ingredient)
                
                # Add nutrition data
                nutrition_data = nutrition_df.loc[recipe_id]
                nutrition = Nutrition(
                    recipe_id=recipe_id,
                    calories=nutrition_data['calories'],
                    protein=nutrition_data['protein'],
                    carbs=nutrition_data['carbs'],
                    fat=nutrition_data['fat'],
                    fiber=nutrition_data['fiber'],
                    sodium=nutrition_data['sodium'],
                    cholesterol=nutrition_data['cholesterol'],
                )
                db.add_nutrition(nutrition)
        
        # Then add the meal plan
        db.add_meal_plan(self)
