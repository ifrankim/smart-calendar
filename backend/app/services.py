import json
import base64
import openai
from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def process_image(image):

    base64_image = base64.b64encode(image.read()).decode("utf-8")

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """You are an advanced food detection and analysis system. Given an image, your task is to:

1. Identify the food items present in the image.
2. Determine whether each food item is typically stored in a refrigerator or left outdoors.
3. Based on its visual appearance (e.g., color, texture, or visible condition in the image), estimate the number of days the food item is safe for consumption. 

Factors to consider:
- For food stored outdoors, assume a humid environment similar to Singapore.
- If the food item appears to be overripe (e.g., a banana with many black spots), its shelf life should be shorter than that of a fresh or unripe counterpart (e.g., a green or yellow banana).

Return the result in the following JSON format:

{
    "food": "<detected food item>",
    "is_refrigirated": "<iffood item is typically stored in a refrigerator or left outdoors>"
    "shelf_life": "<number of days as an integer>"
}

**Important Notes:**
- The "shelf_life" should be an integer representing the number of days the food is safe to consume based on its current state.
- Provide only the JSON response without any additional explanations or comments.

**Example Input:** An image of a banana with black spots.

**Expected Output:**
{
“food”: “banana”,
"is_refrigirated": "false",
“shelf_life”: “2”
}

Ensure the JSON is strictly formatted without additional comments or data. If multiple items are detected, return one JSON object for each food item.""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    content = response.choices[0].message.content
    #     content = """```json
    # {
    #     "food": "banana",
    #     "shelf_life": "7"
    # }
    # ```"""
    print(content.replace("\n", "").replace("```json", "").replace("```", "").strip())
    parsed_response = json.loads(
        content.replace("\n", "").replace("```json", "").replace("```", "").strip()
    )
    return parsed_response
