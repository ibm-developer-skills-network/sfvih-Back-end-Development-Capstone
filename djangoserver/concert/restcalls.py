import requests


def get(url):
    headers = {'Accept': 'application/json', "User-Agent": "XY"}
    response = requests.get(url, headers=headers)
    print(f"Response: {response.json()}")
    return response

def get_lyrics(url, song_id):
    lyric_field = "message"
    full_url = f"{url}{song_id}"
    print(full_url)
    response = get(full_url)
    return response.json()[lyric_field]
