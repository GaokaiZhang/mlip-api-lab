import json
import os
from typing import Any, Dict
from litellm import completion

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

# api_key = "hardcoded API_KEY HERE"
api_key = os.environ.get("GROQ_API_KEY", "")


def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    # implement litellm call here to generate a structured travel itinerary for the given destination

    # See https://docs.litellm.ai/docs/ for reference.

    response = completion(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
              "role": "system", "content": "You are a travel assistant, responding with valid JSON only."
            },
            {
              "role": "user", 
              "content": f"""Generate a travel itinerary for {destination}. Return ONLY a JSON object with these exact keys:                                                                                    
                          - "destination": the destination name (string)                                                                                      
                          - "price_range": estimated budget range (string, e.g., "$1000-$2000")                                                               
                          - "ideal_visit_times": array of best times to visit (array of strings)                                                              
                          - "top_attractions": array of must-see attractions (array of strings)"""   
            }
        ],
    )
    data = json.loads(response.choices[0].message.content)

    required_keys = {"destination", "price_range", "ideal_visit_times", "top_attractions"}
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key in response: {key}")  
    return data

  # 1. Get a Groq API key at: https://console.groq.com/keys                                                 
  # 2. Set the environment variable: export GROQ_API_KEY="your-api-key-here"                                                                                             
  # 3. Install dependencies: pip install -r requirements.txt                                                                                                     
  # 4. Run the Flask server: python3 app.py                                                                                                                      
  # 5. Test the API: curl "http://localhost:8000/api/v1/itinerary?destination=<place>

  # Why hardcoding credentials is bad:                                                                                                                                                                                      
  # Secrets can leak through logs, error messages, or backups                                                                         
  # No separation between code and configuration (different users)                                                                                   
                                                                                                                                      
  # Remedial steps if credentials leak:                                                                                                 
  # Immediately revoke/rotate the leaked credential                                                                                                                                                                            
  # Use tools like git filter-branch or BFG Repo-Cleaner to remove from Git history                                                   



# example from https://docs.litellm.ai/docs/completion/json_mode
# response = completion(
#   model="gpt-4o-mini",
#   response_format={ "type": "json_object" },
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
#     {"role": "user", "content": "Who won the world series in 2020?"}
#   ]
# )
# print(response.choices[0].message.content)