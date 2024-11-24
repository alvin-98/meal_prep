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
                    name TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    unit TEXT NOT NULL,
                    expiry_date TEXT NOT NULL
                )
            ''')
            
            # Create recipes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    instructions TEXT NOT NULL,
                    nutrition TEXT NOT NULL,
                    prep_time INTEGER NOT NULL,
                    image_path TEXT
                )
            ''')
            
            # Create meal plans table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meal_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    recipe_id INTEGER NOT NULL,
                    meal_type TEXT NOT NULL,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
                )
            ''')
            
            conn.commit()
    
    def add_ingredient(self, ingredient) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO ingredients (name, quantity, unit, expiry_date) VALUES (?, ?, ?, ?)',
                (ingredient.name, ingredient.quantity, ingredient.unit, ingredient.expiry_date.isoformat())
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_ingredients(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ingredients')
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'unit': row[3],
                    'expiry_date': datetime.fromisoformat(row[4])
                }
                for row in rows
            ]
    
    def add_recipe(self, recipe) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipes (name, ingredients, instructions, nutrition, prep_time) VALUES (?, ?, ?, ?, ?)',
                (
                    recipe.name,
                    json.dumps(recipe.ingredients),
                    json.dumps(recipe.instructions),
                    json.dumps(recipe.nutrition),
                    recipe.prep_time
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
                    'name': row[1],
                    'ingredients': json.loads(row[2]),
                    'instructions': json.loads(row[3]),
                    'nutrition': json.loads(row[4]),
                    'prep_time': row[5],
                    'image_path': row[6] if len(row) > 6 else None
                }
                for row in rows
            ] 

            