import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def process_image(image):
    # Simulação de retorno para teste
    return [{"name": "Apple", "shelf_life": 7}, {"name": "Milk", "shelf_life": 5}]

    image = request.files["image"]
    response = requests.post(
        "https://api.openai.com/v1/images:analyze",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        files={"file": image},
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to process image."}), 500

    result = response.json()
    food_items = result.get("detected_items", [])
    return jsonify({"detected_items": food_items})
