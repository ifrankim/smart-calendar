import json
import base64
import openai
from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def process_image(image):
    # return [{"name": "Apple", "shelf_life": 7}, {"name": "Milk", "shelf_life": 5}]

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
                        "text": """Analyze the image provided to detect the food items it contains. For each detected food item, determine whether it is typically stored in a refrigerator or in an open-air environment. If the food is stored in an open-air environment, assume a humid climate similar to Singapore when estimating its safety for consumption. Based on this, provide the estimated shelf life of the food in days as an integer.

The response should only return a JSON object with the following format:

{
    "food": "<detected food item>",
    "shelf_life": "<estimated days>"
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
