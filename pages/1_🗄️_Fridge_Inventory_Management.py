import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import List, Dict
import requests
from services.database import Database
import plotly.express as px
from PIL import Image
import io
import os
from services.spoonacular import SpoonacularAPI
from models.ingredients import Ingredient


def show_inventory_management():
    st.header("Inventory Management")
    
    # Add new ingredient form
    with st.form("add_ingredient"):
        name = st.text_input("Ingredient Name")
        quantity = st.number_input("Quantity", min_value=0.0)
        unit = st.selectbox("Unit", ["g", "kg", "ml", "l", "pieces"])
        expiry_date = st.date_input("Expiry Date")
        
        if st.form_submit_button("Add Ingredient"):
            new_ingredient = Ingredient(
                name=name,
                amount=quantity,
                unit=unit,
                expiry_date=datetime.combine(expiry_date, datetime.min.time())
            )
            st.session_state.db.add_ingredient(new_ingredient)
            st.success(f"Added {name} to inventory!")
    

    # Load inventory once and reuse it
    inventory = Ingredient.load_inventory(st.session_state.db)
    if inventory:
        # Create single data structure for both displays
        data = [
            {
                "Name": ing.name,
                "Quantity": f"{ing.amount} {ing.unit}",
                "Days until expiry": ing.days_until_expiry()
            }
            for ing in inventory
        ]

        # Display current inventory using the same data
        st.table(pd.DataFrame(data))

def main():
    show_inventory_management()

if __name__ == "__main__":
    main()
