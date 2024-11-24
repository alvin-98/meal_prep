import sys
from pathlib import Path
from utils.config import initialize_session_state
import streamlit as st

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))



st.set_page_config(
    page_title="Meal Prep Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.title("Meal Planner")
    st.write("Welcome to the Meal Planner!")
    initialize_session_state()

if __name__ == "__main__":
    main() 

