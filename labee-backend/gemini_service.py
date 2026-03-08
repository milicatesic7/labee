from google import genai
from google.genai import types
import os

def apikey():
    return  genai.Client(api_key=os.getenv("GEMINI_API_KEY"))   

config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

