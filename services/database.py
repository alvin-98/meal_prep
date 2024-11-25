import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

class Database:
    def __init__(self, db_path: str = "meal_prep.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create ingredients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ingredient_id INTEGER,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    unit TEXT NOT NULL,
                    expiry_date TEXT,
                    original_string TEXT,
                    aisle TEXT,
                    recipe_id INTEGER
                )
            ''')
            
            # Create recipes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    recipe_id INTEGER PRIMARY KEY NOT NULL,
                    recipe_name TEXT NOT NULL,
                    source_url TEXT,
                    total_cost REAL NOT NULL,
                    prep_time INTEGER NOT NULL,
                    image_url TEXT,
                    servings INTEGER NOT NULL
                )
            ''')
            
            # Create meal plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meal_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_date TEXT NOT NULL,
                    num_days INTEGER NOT NULL,
                    breakfast TEXT NOT NULL,
                    lunch TEXT NOT NULL,
                    dinner TEXT NOT NULL
                )
            ''')

            # Add nutrition table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nutrition (
                    recipe_id INTEGER PRIMARY KEY NOT NULL,
                    calories REAL,
                    protein REAL,
                    carbs REAL,
                    fat REAL,
                    fiber REAL,
                    cholesterol REAL,
                    sodium REAL,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id)
                )
            ''')
            
            conn.commit()
    
    def add_ingredient(self, ingredient) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO ingredients (ingredient_id, name, amount, unit, expiry_date, original_string, aisle, recipe_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (ingredient.ingredient_id, ingredient.name, ingredient.amount, ingredient.unit, ingredient.expiry_date, ingredient.original_string, ingredient.aisle, ingredient.recipe_id)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_ingredients(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get column names
            cursor.execute('PRAGMA table_info(ingredients)')
            columns = [column[1] for column in cursor.fetchall()]
            
            cursor.execute('SELECT * FROM ingredients')
            rows = cursor.fetchall()
            
            return [
                {
                    'ingredient_id': row[columns.index('ingredient_id')],
                    'name': row[columns.index('name')],
                    'amount': row[columns.index('amount')],
                    'unit': row[columns.index('unit')],
                    'expiry_date': datetime.fromisoformat(row[columns.index('expiry_date')]) if row[columns.index('expiry_date')] else None,
                    'original_string': row[columns.index('original_string')],
                    'aisle': row[columns.index('aisle')],
                    'recipe_id': row[columns.index('recipe_id')]
                }
                for row in rows
            ]

    def add_nutrition(self, nutrition) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO nutrition (recipe_id, calories, protein, carbs, fat, fiber, cholesterol, sodium) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    nutrition.recipe_id,
                    nutrition.calories,
                    nutrition.protein,
                    nutrition.carbs,
                    nutrition.fat,
                    nutrition.fiber,
                    nutrition.cholesterol,
                    nutrition.sodium
                )
            )
            conn.commit()
            return cursor.lastrowid
    
    def add_recipe(self, recipe) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipes (recipe_id, recipe_name, source_url, total_cost, prep_time, image_url, servings) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (
                    recipe.recipe_id,
                    recipe.recipe_name,
                    recipe.source_url,
                    recipe.total_cost,
                    recipe.prep_time,
                    recipe.image_url,
                    recipe.servings
                )
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_recipes(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes')
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'recipe_name': row[1],
                    'source_url': row[2],
                    'total_cost': row[3],
                    'prep_time': row[4],
                    'image_url': row[5],
                    'servings': row[6]
                }
                for row in rows
            ] 

    def add_meal_plan(self, meal_plan):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO meal_plans (start_date, num_days, breakfast, lunch, dinner) VALUES (?, ?, ?, ?, ?)', (meal_plan.start_date, meal_plan.num_days, json.dumps(meal_plan.breakfast), json.dumps(meal_plan.lunch), json.dumps(meal_plan.dinner)))
            conn.commit()   
            return cursor.lastrowid
            

    def clear_database(self):
        """Clear all data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript('''
                DELETE FROM meal_plans;
                DELETE FROM recipes;
                DELETE FROM ingredients;
                DELETE FROM nutrition;
                DELETE FROM sqlite_sequence;  -- This resets auto-increment counters
            ''')            