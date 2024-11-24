import requests
import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

class SpoonacularAPI:
    def __init__(self, api_key: Optional[str] = None):
        # Load environment variables from .env file
        load_dotenv()
        
        self.api_key = api_key or os.getenv('SPOONACULAR_API_KEY')
        if not self.api_key:
            raise ValueError("SPOONACULAR_API_KEY not found in environment variables")
        self.base_url = "https://api.spoonacular.com"

    def find_nutrient(self, nutrients: List[Dict], nutrient_name: str) -> float:
        """Helper function to extract nutrient value from nutrients list"""
        for nutrient in nutrients:
            if nutrient.get('name', '').lower() == nutrient_name.lower():
                return nutrient.get('amount', 0)
        return 0.0

    def parse_recipe_data(self, recipes_data: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Convert raw recipe API data into three organized DataFrames:
        - recipes_df: Basic recipe information
        - ingredients_df: Detailed ingredients information
        - nutrition_df: Nutritional information
        """
        if not recipes_data:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        # Process basic recipe information
        recipes_list = []
        ingredients_list = []
        nutrition_list = []

        for recipe in recipes_data:
            # Basic recipe information
            recipe_basic = {
                'recipe_id': recipe['id'],
                'name': recipe['title'],
                'servings': recipe['servings'],
                'prep_time': recipe.get('readyInMinutes', 0),
                'total_cost': recipe.get('pricePerServing', 0) * recipe['servings'],
                'source_url': recipe.get('sourceUrl', ''),
                'image_url': recipe.get('image', '')
            }
            recipes_list.append(recipe_basic)

            # Process ingredients
            for ingredient in recipe['extendedIngredients']:
                ingredient_data = {
                    'recipe_id': recipe['id'],
                    'ingredient_id': ingredient.get('id', 0),
                    'name': ingredient.get('name', ''),
                    'amount': ingredient.get('amount', 0),
                    'unit': ingredient.get('unit', ''),
                    'original_string': ingredient.get('original', ''),
                    'aisle': ingredient.get('aisle', '')
                }
                ingredients_list.append(ingredient_data)

            # Process nutrition
            if 'nutrition' in recipe:
                nutrients = recipe['nutrition'].get('nutrients', [])
                nutrition_data = {
                    'recipe_id': recipe['id'],
                    'calories': self.find_nutrient(nutrients, 'Calories'),
                    'protein': self.find_nutrient(nutrients, 'Protein'),
                    'carbs': self.find_nutrient(nutrients, 'Carbohydrates'),
                    'fat': self.find_nutrient(nutrients, 'Fat'),
                    'fiber': self.find_nutrient(nutrients, 'Fiber'),
                    'sugar': self.find_nutrient(nutrients, 'Sugar'),
                    'sodium': self.find_nutrient(nutrients, 'Sodium'),
                    'cholesterol': self.find_nutrient(nutrients, 'Cholesterol')
                }
                nutrition_list.append(nutrition_data)

        # Create DataFrames
        recipes_df = pd.DataFrame(recipes_list)
        ingredients_df = pd.DataFrame(ingredients_list)
        nutrition_df = pd.DataFrame(nutrition_list)

        # Set index
        if not recipes_df.empty:
            recipes_df.set_index('recipe_id', inplace=True)
        if not nutrition_df.empty:
            nutrition_df.set_index('recipe_id', inplace=True)

        return recipes_df, ingredients_df, nutrition_df

    def search_recipes(self,query: str, ingredients: str, nutrition_goals, max_ready_time: int, sort: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:


        endpoint = f"{self.base_url}/recipes/complexSearch"
        params = {
            "query": query,
            "ingredients": ingredients,
            "fillIngredients": True,
            "minCalories": nutrition_goals['calories'][0],
            "maxCalories": nutrition_goals['calories'][1],
            "minCarbs": nutrition_goals['carbs'][0],
            "maxCarbs": nutrition_goals['carbs'][1],
            "minProtein": nutrition_goals['protein'][0],
            "maxProtein": nutrition_goals['protein'][1],
            "minFat": nutrition_goals['fat'][0],
            "maxFat": nutrition_goals['fat'][1],
            "minFiber": nutrition_goals['fiber'][0],
            "maxFiber": nutrition_goals['fiber'][1],
            "minSugar": nutrition_goals['sugar'][0],
            "maxSugar": nutrition_goals['sugar'][1],
            "number": 5,
            "addRecipeInformation": True,
            "addRecipeNutrition": True,
            "instructionsRequired": True,
            "sort": sort,
            "apiKey": self.api_key
        }
        
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            results = response.json()["results"]
            # Convert API response to DataFrames
            recipes_df, ingredients_df, nutrition_df = self.parse_recipe_data(results)
            return recipes_df, ingredients_df, nutrition_df
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
