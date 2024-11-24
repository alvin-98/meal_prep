import streamlit as st
from models.planner import MealPrepPlanner

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'planner' not in st.session_state:
        st.session_state.planner = MealPrepPlanner()
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = {}
