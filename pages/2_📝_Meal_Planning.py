import streamlit as st
from services.spoonacular import SpoonacularAPI
from datetime import datetime, timedelta
import pandas as pd
from utils.styles import RECIPE_TILE_STYLE
from utils.defaults import MIN_CALORIES, MAX_CALORIES, MAX_TIME, MIN_CARBS, MAX_CARBS, MIN_PROTEIN, MAX_PROTEIN, MIN_FAT, MAX_FAT, MIN_FIBER, MAX_FIBER, MIN_SUGAR, MAX_SUGAR
from utils.config import initialize_session_state
from models.ingredients import Ingredient
from models.meal_plan import MealPlan


def api_call(search_query, nutrition_goals, max_ready_time, sort):
    try:
        api = SpoonacularAPI()
        available_ingredients = Ingredient.get_ingredient_names(st.session_state.db)
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

    col1, col2 = st.columns(2)
    # Calories range
    calorie_range_goal = col1.slider(
        "Select a calorie range (kcal):",
        min_value=MIN_CALORIES,
        max_value=MAX_CALORIES,
        value=(MIN_CALORIES, MAX_CALORIES),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="calorie_range"
    )
        
    # Carbs range
    carbs_range_goal = col1.slider(
        "Select a carbs range (g):",
        min_value=MIN_CARBS,
        max_value=MAX_CARBS,
        value=(MIN_CARBS, MAX_CARBS),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="carbs_range"
    )

    # Protein range
    protein_range_goal = col1.slider(
        "Select a protein range (g):",
        min_value=MIN_PROTEIN,
        max_value=MAX_PROTEIN,
        value=(MIN_PROTEIN, MAX_PROTEIN),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="protein_range"
    )

    # Fat range    
    fat_range_goal = col2.slider(
        "Select a fat range (g):",
        min_value=MIN_FAT,
        max_value=MAX_FAT,
        value=(MIN_FAT, MAX_FAT),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="fat_range"
    )

    # Fiber range
    fiber_range_goal = col2.slider(
        "Select a fiber range (g):",
        min_value=MIN_FIBER,
        max_value=MAX_FIBER,
        value=(MIN_FIBER, MAX_FIBER),  # Default range
        step=10,  # Increment step
        help="Use the slider to select the minimum and maximum calorie values.",
        key="fiber_range"
    )

    # Sugar range
    sugar_range_goal = col2.slider(
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

    nutrition_goals_data = []
    date_str = st.session_state.get('date_input', datetime.now().date()).strftime("%Y-%m-%d")
    
    for nutrition_type, (min_val, max_val) in nutrition_goals.items():
        nutrition_goals_data.append({
            'date': date_str,
            'nutrition_type': nutrition_type,
            'minimum_requirement': min_val,
            'maximum_limit': max_val
        })
    
    nutrition_goals_df = pd.DataFrame(nutrition_goals_data)
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


def recipe_tile(recipe, nutrition_data):
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
        🔥 {nutrition_data['calories']:.0f} cal<br>
        🥩 {nutrition_data['protein']:.1f}g protein<br>
        🍚 {nutrition_data['carbs']:.1f}g carbs<br>
        🥑 {nutrition_data['fat']:.1f}g fat
    </div>
    """


def display_meal_schedule():
    st.subheader("Meal Plan")
    
    start_date = st.session_state.get('date_input', datetime.now().date())

    period_days = {
        "1 day": 1,
        "3 days": 3,
        "5 days": 5,
        "Weekly (7 days)": 7
    }

    num_days = period_days[st.session_state.get('meal_plan_period', "Weekly (7 days)")]
    meal_prep_period_dates = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # Display each day's meals
    for date in meal_prep_period_dates:
        date_str = date.strftime("%Y-%m-%d")
        with st.expander(date.strftime("%A, %B %d")):
            for meal_type in ["breakfast", "lunch", "dinner"]:
                st.subheader(meal_type.capitalize())
                
                # Display current meals for this slot
                daily_meals = st.session_state.meal_plan[
                    (st.session_state.meal_plan['date'] == date_str) & 
                    (st.session_state.meal_plan['meal_type'] == meal_type)
                ]
                if not daily_meals.empty:
                    for i, meal in daily_meals.iterrows():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"• {meal['recipe_name']}")
                        with col2:
                            if st.button("🗑️", key=f"remove_{date_str}_{meal_type}_{i}"):
                                # Remove the meal from the DataFrame
                                st.session_state.meal_plan = st.session_state.meal_plan.drop(index=i)
                                st.rerun()
                else:
                    st.write("No meals planned")


def show_meal_planning():
    st.header("Meal Planning")

    mean_plan_time_period = st.selectbox(
        "I want to Meal Prep for", 
        ["1 day", "3 days", "5 days", "Weekly (7 days)"],
        key="meal_plan_period"
    )

    st.date_input(
        "Starting from",
        value=datetime.now().date(),
        key="date_input",
        on_change=lambda: setattr(st.session_state, 'selected_date', st.session_state['date_input'].strftime("%Y-%m-%d"))
    )

    period_days = {
        "1 day": 1,
        "3 days": 3,
        "5 days": 5,
        "Weekly (7 days)": 7
    }

    start_date = st.session_state.get('date_input', datetime.now().date())
    num_days = period_days[st.session_state.get('meal_plan_period', "Weekly (7 days)")]
    meal_prep_period_dates = [start_date + timedelta(days=i) for i in range(num_days)]


    # Add CSS for recipe tiles
    st.markdown(RECIPE_TILE_STYLE, unsafe_allow_html=True)

    st.write("These are my nutrition goals for a day")
    servings_split = st.selectbox(
        "Split across servings", 
        options=range(2, 6),
        key="servings_split",
        help="Split daily nutrition goals across multiple servings",
    )
    #TODO: Incorporate servings split into nutrition goals

    nutrition_goals = nutrition_goal_setting_widget()
    
    with st.form("search_recipes"):
        
        search_query = st.text_input("I want to make recipes similar to")

        max_ready_time = st.slider(
            "That I can prepare within time period of x minutes",
            max_value=MAX_TIME,
            value=30,  # Default value
            step=5,  # Increment step
            help="Adjust the slider to select the maximum time you're willing to wait for a meal to be ready.",
            key="max_ready_time"
        )

        sort = st.selectbox("Sort recipes by", ["max-used-ingredients", "min-missing-ingredients", "time"])

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
            
            # Iterate through DataFrame
            for idx, row in enumerate(recipes_df.itertuples()):
                with cols[idx % 3]:
                    with st.container():
                        # Get nutrition data using loc once
                        nutrition_data = nutrition_df.loc[row.Index]
                        recipe_ingredients = ingredients_df[ingredients_df['recipe_id'] == row.Index]
                        
                        st.markdown(f"""
                            <div class="recipe-tile">
                                {recipe_tile(row._asdict(), nutrition_data)}                            
                        """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.selectbox(
                            "Meal Type",
                            ["breakfast", "lunch", "dinner"],
                            key=f"meal_type_{row.Index}",
                            format_func=lambda x: x.capitalize()
                        )

                        if st.button("👀 Details", key=f"view_{row.Index}", use_container_width=True):
                            st.session_state.selected_recipe = row.Index                            
                            st.session_state.current_recipe = {
                                'recipe': row._asdict(),
                                'ingredients': recipe_ingredients,
                                'nutrition': nutrition_data
                            }

                        if st.button("➕ Add", key=f"add_{row.Index}", use_container_width=True):
                            meal_type = st.session_state[f"meal_type_{row.Index}"].lower()
                            
                            # Create dates DataFrame for more efficient operations
                            dates = pd.date_range(start=start_date, periods=num_days)
                            for date in dates:
                                date_str = date.strftime("%Y-%m-%d")
                                # Create a new row for the DataFrame
                                new_row = {
                                    'date': date_str,
                                    'num_days': num_days,
                                    'meal_type': meal_type,
                                    'recipe_id': row.Index,
                                    'recipe_name': row.name
                                }
                                # Append the new row to the DataFrame
                                st.session_state.meal_plan = pd.concat([
                                    st.session_state.meal_plan,
                                    pd.DataFrame([new_row])
                                ], ignore_index=True)
                            
                            st.success(f"Added {row.name} to {meal_type} for {num_days} days starting {start_date}!")

            # Show recipe details if selected
            if st.session_state.selected_recipe is not None and hasattr(st.session_state, 'current_recipe'):
                recipe_deep_dive()
        else:
            st.warning("No recipes found matching your criteria.")
    
    # Weekly meal plan view
    st.subheader("Weekly Meal Plan")
    today = datetime.now().date()
    week_dates = [today + timedelta(days=i) for i in range(7)]
    
    display_meal_schedule()


    if st.button("💾 Save Meal Plan", type="primary", use_container_width=True):
        try:
            # Filter DataFrames based on recipe_ids in meal_plan
            recipe_ids = st.session_state.meal_plan['recipe_id'].unique()
            recipes_df, ingredients_df, nutrition_df = st.session_state.search_results
            
            st.session_state.recipes = recipes_df[recipes_df.index.isin(recipe_ids)]
            st.session_state.ingredients = ingredients_df[ingredients_df['recipe_id'].isin(recipe_ids)]
            st.session_state.nutrition = nutrition_df[nutrition_df.index.isin(recipe_ids)]
            
            # Create and save meal plan
            meal_plan = MealPlan.from_dataframe(st.session_state.meal_plan)
            meal_plan.add_meal_plan(st.session_state.db, st.session_state.recipes, st.session_state.nutrition, st.session_state.ingredients)
            st.success("Meal plan saved successfully!")
        except Exception as e:
            st.error(f"Error saving meal plan: {str(e)}")


def main():
    initialize_session_state()
    show_meal_planning()


if __name__ == "__main__":
    main() 

