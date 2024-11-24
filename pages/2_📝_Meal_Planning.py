import streamlit as st
from services.spoonacular import SpoonacularAPI
from models.planner import MealPrepPlanner  # Note: Changed from MealPlanner to MealPrepPlanner
from datetime import datetime, timedelta
import pandas as pd
from utils.styles import RECIPE_TILE_STYLE
from utils.defaults import MIN_CALORIES, MAX_CALORIES, MAX_TIME, MIN_CARBS, MAX_CARBS, MIN_PROTEIN, MAX_PROTEIN, MIN_FAT, MAX_FAT, MIN_FIBER, MAX_FIBER, MIN_SUGAR, MAX_SUGAR
from utils.config import initialize_session_state


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


def nutrition_goal_setting_widget():
    # Calories range
    calorie_range_goal = st.slider(
        "Select a calorie range (kcal):",
        min_value=MIN_CALORIES,
        max_value=MAX_CALORIES,
        value=(MIN_CALORIES, MAX_CALORIES),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="calorie_range"
    )
        
    # Carbs range
    carbs_range_goal = st.slider(
        "Select a carbs range (g):",
        min_value=MIN_CARBS,
        max_value=MAX_CARBS,
        value=(MIN_CARBS, MAX_CARBS),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="carbs_range"
    )

    # Protein range
    protein_range_goal = st.slider(
        "Select a protein range (g):",
        min_value=MIN_PROTEIN,
        max_value=MAX_PROTEIN,
        value=(MIN_PROTEIN, MAX_PROTEIN),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="protein_range"
    )

    # Fat range    
    fat_range_goal = st.slider(
        "Select a fat range (g):",
        min_value=MIN_FAT,
        max_value=MAX_FAT,
        value=(MIN_FAT, MAX_FAT),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="fat_range"
    )

    # Fiber range
    fiber_range_goal = st.slider(
        "Select a fiber range (g):",
        min_value=MIN_FIBER,
        max_value=MAX_FIBER,
        value=(MIN_FIBER, MAX_FIBER),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="fiber_range"
    )

    # Sugar range
    sugar_range_goal = st.slider(
        "Select a sugar range (g):",
        min_value=MIN_SUGAR,
        max_value=MAX_SUGAR,
        value=(MIN_SUGAR, MAX_SUGAR),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="sugar_range"
    )

    nutrition_goals = {
            'calories': calorie_range_goal,
            'carbs': carbs_range_goal,
            'protein': protein_range_goal,
            'fat': fat_range_goal,
            'fiber': fiber_range_goal,
        'sugar': sugar_range_goal
    }

    return nutrition_goals


def recipe_deep_dive():
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


def recipe_tile(recipe, nutrition_df, idx):
    return f"""
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
    """


def show_meal_planning():
    st.header("Meal Planning")
    
    # Add CSS for recipe tiles
    st.markdown(RECIPE_TILE_STYLE, unsafe_allow_html=True)
    
    with st.form("search_recipes"):
        search_query = st.text_input("Search for a recipe")
        
        nutrition_goals = nutrition_goal_setting_widget()

        # Max ready time
        max_ready_time = st.slider(
            "Select maximum preparation time (minutes):",
            max_value=MAX_TIME,
            value=30,  # Default value
            step=5,  # Increment step
            help="Adjust the slider to select the maximum time you're willing to wait for a meal to be ready.",
            key="max_ready_time"
        )

        sort = st.selectbox("Sort by", ["max-used-ingredients", "min-missing-ingredients", "time"])

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
                                {recipe_tile(recipe, nutrition_df, idx)}
                            
                        """, unsafe_allow_html=True)                    

                        if st.button("👀 Details", key=f"view_{idx}", use_container_width=True):
                            st.session_state.selected_recipe = idx
                            # Store the current recipe data
                            st.session_state.current_recipe = {
                                'recipe': recipes_df.loc[idx],
                                'ingredients': ingredients_df[ingredients_df['recipe_id'] == idx],
                                'nutrition': nutrition_df.loc[idx] if idx in nutrition_df.index else None
                            }

                        if st.button("➕ Add", key=f"add_{idx}", use_container_width=True):
                            st.session_state.meal_plan.append(recipe)
                            st.success(f"Added {recipe['name']} to meal plan!")

                        st.markdown("</div>", unsafe_allow_html=True)
            
            # Show recipe details if selected
            if st.session_state.selected_recipe is not None and hasattr(st.session_state, 'current_recipe'):
                recipe_deep_dive()
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
    initialize_session_state()
    show_meal_planning()


if __name__ == "__main__":
    main() 

