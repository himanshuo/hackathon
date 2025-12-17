import asyncio
from oagi import TaskerAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker
from datetime import date, timedelta
from google import genai
from google.genai import types

def call_gemini(query):
    client = genai.Client()
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=config,
    )

    print(response.text)
    return response.text



# items_to_buy = call_gemini("Plan an itinerary for a trip to Tokyo, Japan from December 16th to December 20th. For each item in the itinerary that requires a purchase, figure out the url to figure out the purchase details. The output is a list of purchase items and a url to get the purchase cost. Provide nothing but the purchase item, description, and url as output.")

items_to_buy = """
Here is a list of purchase items, their descriptions, and URLs to find purchase details for your trip to Tokyo from December 16th to December 20th:

*   **Purchase Item:** Accommodation in Tokyo
    *   **Description:** Hotel stay for 4 nights (December 16th - December 20th) in Tokyo.
    *   **URL to Purchase Details:** https://www.kayak.ie/hotels/Tokyo,Japan-p22200/2025-12-19/2025-12-20/2adults;map?ucs=1ickdw7&sort=rank_a

*   **Purchase Item:** Train Tickets
    *   Description: Round-trip express train ticket from Narita International Airport (NRT) to Shibuya.
    *   URL: https://japantravel.navitime.com/en/area/jp/route/calculator/?from=header-dropdown
"""

async def run_tasker():
    agent = TaskerAgent(model="lux-actor-1")
    
    city = "Tokyo"
    today = date.today()
    two_weeks_from_today = today + timedelta(days=14)

    # 1. Define the high-level task and breakdown
    agent.set_task(
        task=f"Figure out the cost of a trip to {city}",
        todos=[
          "There is a text editor open a file called total_cost.rtf.",
          f"For each purchase item listed in the `items_to_buy` string, extract the 'Purchase Item' name and the 'URL to Purchase Details'.",
          f"For each extracted URL, navigate to that URL using a web browser.",
          f"On each webpage, identify the numerical cost associated with the 'Purchase Item'.",
          f"Write the 'Purchase Item' name and its identified cost to the file total_cost.rtf.",
          f"After processing all items, calculate the sum of all identified costs and write the 'Total Estimated Cost' to total_cost.rtf.",
         #   f"Navigate to flights.google.com, set the arrival city to '{city}' and click the first one from the dropdown.",
        #   f"Set the departure date to today ({today}), then set the return date two weeks from today ({two_weeks_from_today})",
        #   "Click Search",
        #   "Click on the first flight of the 'Top departing flights' and click the first of the 'Top returning flights'",
        #   "In the top right of the page, the total cost of the flight is displayed. Save the cost in a text editor."
        ]
    )
    
    # 2. Execute the workflowflights.google.com
    await agent.execute(
        instruction="Find a flight", # Context for the agent
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

asyncio.run(run_tasker())