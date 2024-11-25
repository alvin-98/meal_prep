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

def clear_database():
    if st.button("🗑️ Clear Database", type="primary"):
        if st.session_state.get('confirm_delete', False):
            # Clear the database
            st.session_state.db.clear_database()
            # Reset session state
            initialize_session_state()
            st.success("Database cleared successfully!")
            st.session_state.confirm_delete = False
            st.rerun()
        else:
            st.session_state.confirm_delete = True
            st.error("⚠️ Are you sure? Click the button again to confirm deletion.")

def main():
    st.title("Meal Planner")
    st.write("Welcome to the Meal Planner!")
    initialize_session_state()
    clear_database()



if __name__ == "__main__":
    main() 

