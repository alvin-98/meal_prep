import sys
from pathlib import Path
from models.planner import MealPrepPlanner

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import streamlit as st

st.set_page_config(
    page_title="Meal Prep Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'planner' not in st.session_state:
        st.session_state.planner = MealPrepPlanner()
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None

def main():
    st.title("Meal Planner")
    st.write("Welcome to the Meal Planner!")
    initialize_session_state()

if __name__ == "__main__":
    main() 

