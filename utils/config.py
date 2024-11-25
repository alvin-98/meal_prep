import streamlit as st
from services.database import Database
import pandas as pd

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None
    if 'meal_plan' not in st.session_state:
        columns = ['date', 'num_days', 'meal_type', 'recipe_id', 'recipe_name']
        st.session_state.meal_plan = pd.DataFrame(columns=columns)
    if 'meal_plan_recipes' not in st.session_state:
        columns = ['recipe_id', 'recipe_name', 'servings', 'prep_time', 'total_cost', 'source_url', 'image_url']
        st.session_state.meal_plan_recipes = pd.DataFrame(columns=columns)
    if 'meal_plan_ingredients' not in st.session_state:
        columns = ['recipe_id', 'ingredient_id', 'name', 'amount', 'unit', 'expiry_date', 'original_string', 'aisle']
        st.session_state.meal_plan_ingredients = pd.DataFrame(columns=columns)
    if 'meal_plan_nutrition' not in st.session_state:
        columns = ['recipe_id', 'calories', 'protein', 'carbs', 'fiber', 'sodium', 'sugar', 'fat', 'cholesterol']
        st.session_state.meal_plan_nutrition = pd.DataFrame(columns=columns)
        
