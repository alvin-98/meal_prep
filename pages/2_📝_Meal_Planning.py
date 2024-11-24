import streamlit as st
from services.spoonacular import SpoonacularAPI
from models.planner import MealPrepPlanner  # Note: Changed from MealPlanner to MealPrepPlanner
from datetime import datetime, timedelta
import pandas as pd

# Initialize session state at the very beginning
if 'planner' not in st.session_state:
    st.session_state.planner = MealPrepPlanner()
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None

def api_call(search_query, nutrition_goals, max_ready_time, sort):
    try:
        api = SpoonacularAPI()
        available_ingredients = st.session_state.planner.get_ingredient_names()
        available_ingredients = ",".join(available_ingredients) if available_ingredients else ""
        
        recipes_df, ingredients_df, nutrition_df = api.search_recipes(
            search_query, 
            available_ingredients, 
            nutrition_goals, 
            max_ready_time, 
            sort
        )
        return recipes_df, ingredients_df, nutrition_df
    except Exception as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def show_meal_planning():
    st.header("Meal Planning")
    
    # Add CSS for recipe tiles
    st.markdown("""
        <style>
        .recipe-tile {
        display: inline-block; /* Align tiles side by side */
            vertical-align: top; 
            width: 300px; /* Set consistent width for the tiles */
            margin: 10px; /* Add spacing between tiles */
            padding: 15px; /* Add internal spacing */
            border: 1px solid #ddd; /* Optional: Add a border for better separation */
            border-radius: 10px; /* Rounded corners */
            background-color: #f9f9f9; /* Light background */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            text-align: center; /* Center-align text inside tiles */
        }
        .recipe-image {
            max-width: 100%; /* Make images responsive */
            height: auto;
            border-radius: 10px; /* Match the tile's rounded corners */
        }
        .recipe-title {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            color: #333; /* Dark text for visibility */
        }
        .recipe-info {
            font-size: 14px;
            margin: 5px 0;
            color: #555; /* Slightly lighter text */
        }
        .recipe-nutrition {
            font-size: 14px;
            margin: 10px 0;
            color: #444; /* Ensure nutrition text is visible */
        }
        button-container {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .button-container button {
            flex: 1;
            padding: 8px 16px;
            border-radius: 5px;
        }
        /* Style specific buttons */
        div[data-testid="column"]:first-child .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        div[data-testid="column"]:last-child .stButton > button {
            background-color: #2196F3;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.form("search_recipes"):
        search_query = st.text_input("Search for a recipe")
        
        min_calories = 0
        max_calories = 2000
        
        # Calories range
        calorie_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_calories,
            max_value=max_calories,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="calorie_range"
        )
        min_calories, max_calories = calorie_range
        
        max_time = 120  # Assume meals take between 0 and 120 minutes

        # Max ready time
        max_ready_time = st.slider(
            "Select maximum preparation time (minutes):",
            max_value=max_time,
            value=30,  # Default value
            step=5,  # Increment step
            help="Adjust the slider to select the maximum time you're willing to wait for a meal to be ready.",
            key="max_ready_time"
        )

        min_carbs = 0
        max_carbs = 2000
        
        # Carbs range
        carbs_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_carbs,
            max_value=max_carbs,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="carbs_range"
        )
        min_carbs, max_carbs = carbs_range

        # Protein range
        min_protein = 0
        max_protein = 2000
        
        protein_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_protein,
            max_value=max_protein,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="protein_range"
        )
        min_protein, max_protein = protein_range

        # Fat range
        min_fat = 0
        max_fat = 2000
        
        fat_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_fat,
            max_value=max_fat,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="fat_range"
        )
        min_fat, max_fat = fat_range

        # Fiber range
        min_fiber = 0
        max_fiber = 2000
        
        fiber_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_fiber,
            max_value=max_fiber,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="fiber_range"
        )
        min_fiber, max_fiber = fiber_range

        # Sugar range
        min_sugar = 0
        max_sugar = 2000
        
        sugar_range = st.slider(
            "Select a calorie range (kcal):",
            min_value=min_sugar,
            max_value=max_sugar,
            value=(500, 1500),  # Default range
            step=10,  # Increment step
            help="Use the slider to select the minimum and maximum calorie values.",
            key="sugar_range"
        )
        min_sugar, max_sugar = sugar_range

        sort = st.selectbox("Sort by", ["max-used-ingredients", "min-missing-ingredients", "time"])

        nutrition_goals = {
            'calories': calorie_range,
            'carbs': carbs_range,
            'protein': protein_range,
            'fat': fat_range,
            'fiber': fiber_range,
            'sugar': sugar_range
        }

        search_submitted = st.form_submit_button("Search Recipes")
        if search_submitted:
            results = api_call(search_query, nutrition_goals, max_ready_time, sort)
            if results[0] is not None:  # Check if recipes_df exists
                st.session_state.search_results = results
    
    # Display results outside the form
    if st.session_state.search_results:
        recipes_df, ingredients_df, nutrition_df = st.session_state.search_results
        
        if not recipes_df.empty:
            # Display recipes in a grid
            cols = st.columns(3)
            for idx, recipe in recipes_df.iterrows():
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"""
                            <div class="recipe-tile">
                                <img src="{recipe['image_url']}" class="recipe-image" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                                <div class="recipe-title">{recipe['name']}</div>
                                <div class="recipe-info">
                                    ⏱️ {recipe['prep_time']} minutes<br>
                                    👥 {recipe['servings']} servings<br>
                                    💰 ${recipe['total_cost']:.2f}
                                </div>
                                <div class="recipe-nutrition">
                                    Nutrition per serving:<br>
                                    🔥 {nutrition_df.loc[idx, 'calories']:.0f} cal<br>
                                    🥩 {nutrition_df.loc[idx, 'protein']:.1f}g protein<br>
                                    🍚 {nutrition_df.loc[idx, 'carbs']:.1f}g carbs<br>
                                    🥑 {nutrition_df.loc[idx, 'fat']:.1f}g fat
                                </div>
                            
                        """, unsafe_allow_html=True)                    

                        # Modify the button handling
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("👀 Details", key=f"view_{idx}", use_container_width=True):
                                st.session_state.selected_recipe = idx
                                # Store the current recipe data
                                st.session_state.current_recipe = {
                                    'recipe': recipes_df.loc[idx],
                                    'ingredients': ingredients_df[ingredients_df['recipe_id'] == idx],
                                    'nutrition': nutrition_df.loc[idx] if idx in nutrition_df.index else None
                                }

                        with c2:
                            if st.button("➕ Add", key=f"add_{idx}", use_container_width=True):
                                st.success(f"Added {recipe['name']} to meal plan!")
            
            # Show recipe details if selected
            if st.session_state.selected_recipe is not None and hasattr(st.session_state, 'current_recipe'):
                with st.expander("Recipe Details", expanded=True):
                    recipe = st.session_state.current_recipe['recipe']
                    recipe_ingredients = st.session_state.current_recipe['ingredients']
                    nutrition = st.session_state.current_recipe['nutrition']
                    
                    st.image(recipe['image_url'])
                    st.title(recipe['name'])
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.subheader("Ingredients")
                        for _, ing in recipe_ingredients.iterrows():
                            st.write(f"• {ing['amount']} {ing['unit']} {ing['name']}")
                    
                    with col2:
                        if nutrition is not None:
                            st.subheader("Nutrition")
                            st.write(f"🔥 Calories: {nutrition['calories']:.0f}")
                            st.write(f"🥩 Protein: {nutrition['protein']:.1f}g")
                            st.write(f"🍚 Carbs: {nutrition['carbs']:.1f}g")
                            st.write(f"🥑 Fat: {nutrition['fat']:.1f}g")
                            st.write(f"📊 Fiber: {nutrition['fiber']:.1f}g")
                            st.write(f"🍯 Sugar: {nutrition['sugar']:.1f}g")
                    
                    if st.button("Close Details"):
                        st.session_state.selected_recipe = None
                        if 'current_recipe' in st.session_state:
                            del st.session_state.current_recipe
        else:
            st.warning("No recipes found matching your criteria.")
    
    # Weekly meal plan view
    st.subheader("Weekly Meal Plan")
    today = datetime.now().date()
    week_dates = [today + timedelta(days=i) for i in range(7)]
    
    # Create weekly schedule
    schedule_data = []
    for date in week_dates:
        schedule_data.append({
            "Date": date.strftime("%A, %B %d"),
            "Breakfast": "Not planned",
            "Lunch": "Not planned",
            "Dinner": "Not planned"
        })
    
    st.table(pd.DataFrame(schedule_data))

def main():
    show_meal_planning()

if __name__ == "__main__":
    main() 

