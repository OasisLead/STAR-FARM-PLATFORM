"""
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: GEMINI_API_KEY' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'

  """

"""
from google import genai

client = genai.Client(api_key="AIzaSyAb69U5N43OzOdkVDVnHD_73egy1A3pn3Y")

response = client.models.generate_content(
    model="gemini-2.5-pro", contents="Explain how AI works in a few words"
)
print(response.text)

"""

"""
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
"""



from google import genai
from google.genai import types

# Configure the client
client = genai.Client(api_key="AIzaSyAb69U5N43OzOdkVDVnHD_73egy1A3pn3Y")

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Describe me from research papers what is the latest evolution and main trends and numbers of rice shrimp farming in the Mékong delta in Vietnam in one paragraph.",
    config=config,
)

# Print the grounded response
print(response.text)