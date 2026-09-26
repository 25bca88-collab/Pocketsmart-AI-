import os
from dotenv import load_dotenv
load_dotenv(override=True)
from google import genai
API_KEY = os.getenv("GEMINI_API_KEY","").strip()
MODEL = os.getenv("GEMINI_MODEL","gemini-3.6-flash").strip()
def _generate(prompt):
    if not API_KEY:
        return "Gemini API key is missing. Please check your .env file."
    try:
        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        return response.text or "No recommendation was returned."

    except Exception as error:
        return f"Gemini error: {error}"


def get_home_recommendations(
    budget,
    room,
    items,
    style,
    preferences,
    platforms,
):
    prompt = f"""
You are PocketSmart AI, a smart and practical home decor recommendation assistant.

The user wants help planning their home decor.

Budget: {budget}
Room: {room}
Items needed: {items}
Style: {style}
Preferences: {preferences}
Shopping platforms: {platforms}

Create a useful recommendation.

Include:
1. Room concept
2. Recommended items
3. Suggested colors and materials
4. Budget breakdown
5. Shopping tips

Keep the answer clear, practical, and easy to understand.
"""

    return _generate(prompt)


def get_party_recommendations(
    budget,
    guests,
    party_type,
    venue,
    food,
    decorations,
    platforms,
    preferences,
):
    prompt = f"""
You are PocketSmart AI, a smart and practical party planning assistant.

Plan an event using:

Budget: {budget}
Number of guests: {guests}
Party type: {party_type}
Venue: {venue}
Food: {food}
Decorations: {decorations}
Shopping platforms: {platforms}
Preferences: {preferences}

Include:
1. Party theme
2. Budget breakdown
3. Food plan
4. Decoration checklist
5. Event timeline
6. Shopping tips

Keep the answer practical and easy to follow.
"""

    return _generate(prompt)


def get_jewelry_recommendations(
    budget,
    occasion,
    outfit_style,
    jewelry_type,
    material,
    preferences,
):
    prompt = f"""
You are PocketSmart AI, a smart jewelry shopping assistant.

Recommend jewelry based on:

Budget: {budget}
Occasion: {occasion}
Outfit style: {outfit_style}
Jewelry type: {jewelry_type}
Preferred material: {material}
Preferences: {preferences}

Include:
1. Suitable jewelry styles
2. Material suggestions
3. Outfit matching advice
4. Budget allocation
5. Shopping considerations

Keep the answer practical and easy to understand.
Do not claim that a specific product is available unless the user provides a product or store.
"""

    return _generate(prompt)