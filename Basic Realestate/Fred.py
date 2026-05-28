import json, requests
#I don't do this but for sake of proj
FRED_API_KEY = ""

real_estate_series = [
    "CPIAUCSL",
    "MORTGAGE30US",
    "MORTGAGE15US",
    "HOUST"
]

def fetch_fred_series_metadata(series_id):
    url = "https://api.stlouisfed.org/fred/series"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch metadata: {series_id} ({response.status_code})")
        return None
    data = response.json()
    series = data.get("seriess", [])
    if series:
        return series[0]
    return None

def fetch_fred_observations(series_id, observation_start="2016-01-01"):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": observation_start,
        "sort_order": "desc"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed: {series_id} ({response.status_code})")
        return None
    return response.json().get("observations", [])

def fetchFredData(states=None):
    results = {}
    if states:
        for state in states:
            real_estate_series.append(f"{state}UR")

    for series_id in real_estate_series:
        metadata = fetch_fred_series_metadata(series_id)
        obs = fetch_fred_observations(series_id)
        if obs and metadata:
            results[series_id] = {
                "units": metadata.get("units"),
                "title": metadata.get("title"),
                "observations": obs
            }
            print(f"{series_id}: {len(obs)} observations, units = {metadata.get('units')}, latest = {obs[0]['date']}: {obs[0]['value']}")
    return results

if __name__ == "__main__":
    data = fetchFredData()
    with open("fred_data.json", "w") as fred:
        json.dump(data, fred, indent=2)