import streamlit as st
import plotly.graph_objects as go

st.title("User Dashboard")

col1, col2 = st.columns(2)

with col1:
    height = st.number_input("Height (cm)", value=170, step=1)
    age = st.number_input("Age", value=30, step=1)

with col2:
    weight = st.number_input("Weight (kg)", value=70, step=1)
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"])

# Calculate BMI
height_m = height / 100  # convert cm to meters
bmi = weight / (height_m ** 2)


def get_bmi_category_and_color(bmi_value):
    if bmi_value <= 18.5:
        return "Underweight", "#FFB6C1"
    elif bmi_value <= 24.9:
        return "Normal", "#90EE90"
    elif bmi_value <= 29.9:
        return "Overweight", "#FFD700"
    else:
        return "Obese", "#FF6B6B"


# Create a gauge chart for BMI
def create_bmi_gauge(bmi_value):
    category, color = get_bmi_category_and_color(bmi_value)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"BMI - {category}", 'font': {'size': 24}},
        delta = {'reference': 21.7, 'position': "top"},  # Reference is middle of normal range
        number = {'suffix': " kg/m²", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color, 'thickness': 0.6},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 18.5], 'color': "#FFB6C1"},    # Light pink
                {'range': [18.5, 24.9], 'color': "#90EE90"}, # Light green
                {'range': [24.9, 29.9], 'color': "#FFD700"}, # Gold
                {'range': [29.9, 40], 'color': "#FF6B6B"}    # Coral red
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': bmi_value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "white", 'family': "Arial"},
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# Display BMI gauge
st.plotly_chart(create_bmi_gauge(bmi), use_container_width=True)



