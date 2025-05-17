import json
import requests
import time
import os
from tqdm import tqdm
from os import environ
sportsradar_api = environ.get('SPORTSRADAR_API')


def fetch_wnba_games(schedule_file='schedule_2024.json'):
    """
    Fetch WNBA game data for all games in the schedule file
    
    Args:
        schedule_file (str): Path to the schedule JSON file
        api_key (str): Sportradar API key
    """
    
    with open(schedule_file, 'r') as f:
        schedule_data = json.load(f)   
    game_ids = []

    for game in schedule_data['games']:
        if 'id' in game:
            game_ids.append(game['id'])

    print(f"Found {len(game_ids)} games in schedule.")

    
    # Create output directory if it doesn't exist
    output_dir = "game_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up the API request
    base_url = "https://api.sportradar.com/wnba/trial/v8/en/games/{}/summary.json"
    headers = {
    "accept": "application/json",
    "x-api-key": sportsradar_api
    }
    
    # Process each game ID
    success_count = 0
    for i, game_id in enumerate(game_ids):
        output_file = os.path.join(output_dir, f"2024_{game_id}.json")
        
        # Skip if file already exists
        if os.path.exists(output_file):
            print(f"Skipping game {game_id} - file already exists")
            success_count += 1
            continue
        
        # Construct URL
        url = base_url.format(game_id)
        
        try:
            print(f"Fetching game {i+1}/{len(game_ids)}: {game_id}")
            response = requests.get(url, headers=headers)
            
            # Check for successful response
            response.raise_for_status()
            
            # Save response to file
            with open(output_file, 'w') as f:
                json.dump(response.json(), f, indent=4)
            
            print(f"Saved data to {output_file}")
            success_count += 1
            
            time.sleep(1)
                
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for game {game_id}: {e}")
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting 60 seconds...")
                time.sleep(1)  # Wait longer for rate limit errors
            
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    
    print(f"Process completed: {success_count}/{len(game_ids)} games successfully processed")
    return success_count == len(game_ids)


fetch_wnba_games()