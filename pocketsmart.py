import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


# --------------------------------------------------
# COMMON GEMINI FUNCTION
# --------------------------------------------------

def generate_ai_response(prompt):
    """
    Sends a prompt to Gemini and returns the generated text.
    """

    try:

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text

        return "No recommendation was generated."

    except Exception as e:

        print("Gemini API Error:", e)

        return (
            "Sorry, PocketSmart AI could not generate "
            "recommendations at this time."
        )


# --------------------------------------------------
# HOME INTERIOR RECOMMENDATIONS
# --------------------------------------------------

def get_home_recommendations(data):

    budget = data.get("budget", 0)
    room = data.get("room", "Not specified")
    items = data.get("items", "Not specified")
    style = data.get("style", "Not specified")

    prompt = f"""
You are PocketSmart AI, a smart budget planning
and recommendation assistant.

The user wants to plan their home interior.

USER INFORMATION
----------------
Total Budget: ₹{budget}
Room: {room}
Required Items: {items}
Preferred Style: {style}

YOUR TASK
---------
Create a practical home interior recommendation.

Requirements:

1. Stay within the user's budget.
2. Divide the budget sensibly between the requested items.
3. Suggest suitable products for the room.
4. Consider the user's preferred style.
5. Provide estimated prices.
6. Mention suitable platforms such as Amazon or IKEA
   where appropriate.
7. Calculate an approximate total cost.
8. Mention the remaining budget.
9. Do not exceed the user's total budget.

Return the answer using this structure:

HOME INTERIOR PLAN
==================

Room:
Style:

Budget Allocation:
- Item 1:
- Item 2:
- Item 3:

Recommended Products:
1. Product:
   Category:
   Estimated Price:
   Platform:
   Reason:

2. Product:
   Category:
   Estimated Price:
   Platform:
   Reason:

TOTAL ESTIMATED COST:
REMAINING BUDGET:

FINAL SUGGESTION:
"""

    return generate_ai_response(prompt)


# --------------------------------------------------
# PARTY RECOMMENDATIONS
# --------------------------------------------------

def get_party_recommendations(data):

    budget = data.get("budget", 0)
    guests = data.get("guests", 0)
    event_type = data.get("event_type", "Not specified")
    venue = data.get("venue", "Not specified")

    prompt = f"""
You are PocketSmart AI, a smart event budget
planning assistant.

The user wants to organize an event.

EVENT INFORMATION
-----------------
Total Budget: ₹{budget}
Number of Guests: {guests}
Event Type: {event_type}
Venue Preference: {venue}

YOUR TASK
---------
Create a practical party plan.

Divide the budget between:

1. Food / Catering
2. Venue
3. Decoration
4. Entertainment
5. Other necessary expenses

Requirements:

- Stay within the total budget.
- Consider the number of guests.
- Provide estimated costs.
- Suggest suitable services/platforms where appropriate,
  such as Swiggy, Zomato or OYO.
- Calculate the approximate total.
- Show the remaining budget.
- Avoid exceeding the user's budget.

Return the answer using this format:

PARTY BUDGET PLAN
=================

Event:
Guests:
Venue:

BUDGET ALLOCATION

Food:
Venue:
Decoration:
Entertainment:
Other:

RECOMMENDATIONS

1. Category:
   Suggestion:
   Estimated Cost:
   Platform:
   Reason:

2. Category:
   Suggestion:
   Estimated Cost:
   Platform:
   Reason:

TOTAL ESTIMATED COST:
REMAINING BUDGET:

FINAL EVENT PLAN:
"""

    return generate_ai_response(prompt)


# --------------------------------------------------
# JEWELRY RECOMMENDATIONS
# --------------------------------------------------

def get_jewelry_recommendations(data):

    budget = data.get("budget", 0)
    occasion = data.get("occasion", "Not specified")
    style = data.get("style", "Not specified")

    prompt = f"""
You are PocketSmart AI, a jewelry recommendation
assistant.

USER INFORMATION
-----------------
Budget: ₹{budget}
Occasion: {occasion}
Preferred Style: {style}

YOUR TASK
---------
Recommend jewelry that matches the user's occasion,
style and budget.

Consider:

- Necklace
- Earrings
- Bracelet
- Ring
- Other suitable accessories

Requirements:

1. Stay within the user's budget.
2. Match the occasion.
3. Match the preferred style.
4. Provide estimated prices.
5. Suggest suitable platforms such as Amazon or Flipkart
   where appropriate.
6. Explain why each recommendation is suitable.
7. Calculate the approximate total cost.

Return the answer using this structure:

JEWELRY PLAN
============

Occasion:
Style:
Budget:

RECOMMENDATIONS

1. Jewelry Type:
   Design:
   Estimated Price:
   Platform:
   Why it matches:

2. Jewelry Type:
   Design:
   Estimated Price:
   Platform:
   Why it matches:

TOTAL ESTIMATED COST:
REMAINING BUDGET:

FINAL SUGGESTION:
"""

    return generate_ai_response(prompt)


# --------------------------------------------------
# IMAGE + JEWELRY RECOMMENDATIONS
# --------------------------------------------------

def get_jewelry_image_recommendations(
    data,
    image_path
):

    budget = data.get("budget", 0)
    occasion = data.get("occasion", "Not specified")
    style = data.get("style", "Not specified")

    try:

        # Upload image to Gemini
        uploaded_image = genai.upload_file(
            image_path
        )

        prompt = f"""
You are PocketSmart AI.

Analyze the uploaded outfit image and recommend
jewelry that visually matches the outfit.

USER INFORMATION
-----------------
Budget: ₹{budget}
Occasion: {occasion}
Preferred Style: {style}

Analyze:

- Outfit color
- General outfit style
- Suitable jewelry color
- Suitable jewelry type
- Suitable jewelry design
- Occasion compatibility

Requirements:

1. Stay within the user's budget.
2. Recommend matching jewelry.
3. Explain why the jewelry matches the outfit.
4. Provide estimated prices.
5. Mention suitable platforms where appropriate.
6. Give the total estimated cost.
7. Show remaining budget.

Return:

OUTFIT ANALYSIS
===============

Outfit Colors:
Outfit Style:

JEWELRY RECOMMENDATIONS

1. Type:
   Design:
   Color:
   Estimated Price:
   Platform:
   Reason:

2. Type:
   Design:
   Color:
   Estimated Price:
   Platform:
   Reason:

TOTAL ESTIMATED COST:
REMAINING BUDGET:

FINAL SUGGESTION:
"""

        response = model.generate_content([
            prompt,
            uploaded_image
        ])

        if response and response.text:
            return response.text

        return "No jewelry recommendation generated."

    except Exception as e:

        print("Image processing error:", e)

        return (
            "Unable to analyze the outfit image. "
            "Please try another image."
        )


# --------------------------------------------------
# GENERIC RECOMMENDATION FUNCTION
# --------------------------------------------------

def get_recommendations(
    planner_type,
    data
):

    planner_type = planner_type.lower()

    if planner_type == "home":

        return get_home_recommendations(data)

    elif planner_type == "party":

        return get_party_recommendations(data)

    elif planner_type == "jewelry":

        return get_jewelry_recommendations(data)

    else:

        return (
            "Invalid planner type. "
            "Choose Home, Party or Jewelry."
        )s