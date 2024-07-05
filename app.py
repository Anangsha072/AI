from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image
import io

app = Flask(__name__)

# Replace with your API key or authentication method for the nutrition API
API_KEY = 'dc0e3f40fec3e58c3531500e86aa4b65	—'

# Example function to process uploaded image
def process_image(image):
    # Placeholder function; replace with your actual image recognition code
    # Example: Convert image to numpy array, preprocess, and predict
    # img_array = preprocess_image(image)
    # predictions = model.predict(img_array)
    # return predictions
    return ["food1", "food2", "food3"]

# Example function to fetch nutrition data from Nutritionix API
def fetch_nutrition_data(food_items):
    url = 'https://api.nutritionix.com/v1_1/search'
    headers = {'x-app-key': API_KEY}
    nutrition_info = []

    for food in food_items:
        try:
            params = {'q': food, 'fields': 'item_name,nf_calories,nf_total_fat'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            data = response.json()
            nutrition_info.append({
                'name': food,
                'calories': data['hits'][0]['fields']['nf_calories'],
                'fat': data['hits'][0]['fields']['nf_total_fat']
            })
        except Exception as e:
            print(f"Error fetching nutrition data for {food}: {str(e)}")

    return nutrition_info

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        img = Image.open(io.BytesIO(file.read()))
        foods_detected = process_image(img)
        nutrition_data = fetch_nutrition_data(foods_detected)
        return jsonify({'foods_detected': foods_detected, 'nutrition_data': nutrition_data})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

