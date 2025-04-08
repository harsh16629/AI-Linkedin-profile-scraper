import os
import json
import asyncio
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller, Browser, BrowserConfig
from collections import deque

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Cache config
CACHE_FILE = "profile_cache.json"

# Output model definitions
class Profile(BaseModel):
    profile_name: str
    profile_url: str

class Profiles(BaseModel):
    profiles: List[Profile]

# Controller for final output parsing
controller = Controller(output_model=Profiles)

# Browser setup
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    )
)

# ------------ Context Management Tools ------------
def summarize_text(text: str, max_chars: int = 1000) -> str:
    return text[:max_chars] + "..." if len(text) > max_chars else text

# ------------ Cache Utilities ------------
def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {"visited_urls": [], "profiles": []}

def update_cache(profile: dict, cache: dict):
    if profile['profile_url'] not in cache["visited_urls"]:
        cache["visited_urls"].append(profile["profile_url"])
        cache["profiles"].append(profile)

def save_cache(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

# ------------ Infinite Loop Detection Tools ------------
action_history = deque(maxlen=5)

def detect_loop(action_key: str):
    action_history.append(action_key)
    # If all recent actions are the same, we’re looping
    if len(set(action_history)) <= 1 and len(action_history) == action_history.maxlen:
        raise RuntimeError("Infinite loop detected: Repeating same action")
    
# ------------ Profile URL Normalization ------------
def normalize_profile_url(url: str) -> str:
    if url.startswith("/in/"):
        url = "https://www.linkedin.com" + url        # for eg. /in/rohit -> https://www.linkedin.com/in/rohit
    if not url.startswith("https://www.linkedin.com/in/"):
        return url  
    return url.rstrip("/")


# ------------ Main Async Function ------------
async def main():
    cache = load_cache()
    visited_urls = set(cache["visited_urls"])  # Use a set for fast lookup

    try:
        task = (
            "Go to the first profile's page."
            "Extract the full name and profile URL."
            "Locate and visit the first visible profile page and extract the full name and profile URL."
            "Repeat for 200 profiles."
        )

        llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            api_key=SecretStr(GEMINI_API_KEY)
        )


        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            initial_actions=[
                {'open_tab': {'url': 'https://www.linkedin.com/mynetwork/'}}
            ],
            controller=controller
        )

        # Limit number of steps to avoid infinite loops
        result = await agent.run(max_steps=15)

        if result:
            data = result.final_result()
            parsed: Profiles = Profiles.model_validate_json(data)
        else:
            print('No result')
            return

        # Filter and deduplicate
        new_profiles = []
        for profile in parsed.profiles:
            # Normalize the profile URL
            clean_url = normalize_profile_url(profile.profile_url)
            # Detect potential infinite loop via repetitive action pattern
            detect_loop(clean_url)

            if clean_url not in visited_urls:
                #print(f"New profile: {profile.profile_name}")
                profile_dict = {
                    "profile_name": profile.profile_name,
                    "profile_url": profile.profile_url
                }
                update_cache(profile_dict, cache)
                visited_urls.add(clean_url)
                new_profiles.append(profile_dict)
            else:
                print(f"Skipping cached profile: {profile.profile_name}")
                

        # Save updated cache
        save_cache(cache)

        # Save only new profiles
        if new_profiles:
            with open("linkedin_profile_data.json", "w") as f:
                json.dump(new_profiles, f, indent=4)
            print("New profiles saved to linkedin_profile_data.json")
        else:
            print("No new profiles to save.")

    except RuntimeError as loop_error:
        print(f"Execution halted: {loop_error}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            await browser.close()
            print("Browser closed successfully.")
        except Exception as close_error:
            print(f"An error occurred while closing the browser: {close_error}")

# ------------ Entrypoint ------------
if __name__ == '__main__':
    asyncio.run(main())