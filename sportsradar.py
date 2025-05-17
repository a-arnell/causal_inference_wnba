import requests
import json

url = "https://api.sportradar.com/wnba/trial/v8/en/games/127815af-ec83-4409-b0c3-4140a357a60c/summary.json"

headers = {
    "accept": "application/json",
    "x-api-key": "MJejeqoKn1x1FSYAeZxcPhkKXbb2EKO40xFZO9XI"
}

response = requests.get(url, headers=headers)

with open('game_summary.json', 'w') as f:
    json.dump(response.json(), f,indent=4)

