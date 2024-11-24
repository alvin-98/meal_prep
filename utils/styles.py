RECIPE_TILE_STYLE = """
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
        div[data-testid="column"]:first-child .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        div[data-testid="column"]:last-child .stButton > button {
            background-color: #2196F3;
            color: white;
        }
        </style>
    """