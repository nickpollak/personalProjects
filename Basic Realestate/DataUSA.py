import json, requests

dataUSbaseURL = "https://api.datausa.io/tesseract/data.jsonrecords"

STATE_CODES = {
    "AL": "04000US01", "AK": "04000US02", "AZ": "04000US04", "AR": "04000US05", "CA": "04000US06",
    "CO": "04000US08", "CT": "04000US09", "DE": "04000US10", "DC": "04000US11", "FL": "04000US12",
    "GA": "04000US13", "HI": "04000US15", "ID": "04000US16", "IL": "04000US17", "IN": "04000US18",
    "IA": "04000US19", "KS": "04000US20", "KY": "04000US21", "LA": "04000US22", "ME": "04000US23",
    "MD": "04000US24", "MA": "04000US25", "MI": "04000US26", "MN": "04000US27", "MS": "04000US28",
    "MO": "04000US29", "MT": "04000US30", "NE": "04000US31", "NV": "04000US32", "NH": "04000US33",
    "NJ": "04000US34", "NM": "04000US35", "NY": "04000US36", "NC": "04000US37", "ND": "04000US38",
    "OH": "04000US39", "OK": "04000US40", "OR": "04000US41", "PA": "04000US42", "RI": "04000US44",
    "SC": "04000US45", "SD": "04000US46", "TN": "04000US47", "TX": "04000US48", "UT": "04000US49",
    "VT": "04000US50", "VA": "04000US51", "WA": "04000US53", "WV": "04000US54", "WI": "04000US55", "WY": "04000US56"
}

cube_config = {
    "total_population_state": {
        "cube": "acs_yg_total_population_1",
        "drilldowns": ["State", "Year"],
        "measures": ["Population"]
    },
    "total_population_county": {
        "cube": "acs_yg_total_population_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Population"]
    },
    "tenure_state": {
        "cube": "acs_ygo_tenure_1",
        "drilldowns": ["State", "Year"],
        "measures": ["Household Ownership"]
    },
    "tenure_county": {
        "cube": "acs_ygo_tenure_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Household Ownership"]
    },
    "median_household_income_state": {
    "cube": "acs_yg_household_income_1",
    "drilldowns": ["State", "Year"],
    "measures": ["Household Income"]
    },
    "median_household_income_county": {
        "cube": "acs_yg_household_income_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Household Income"]
    },
    "gini_state": {
        "cube": "acs_yg_gini_1",
        "drilldowns": ["State", "Year"],
        "measures": ["Wage GINI"] 
    },
    "gini_county": {
        "cube": "acs_yg_gini_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Wage GINI"]
    },
    "property_value_state": {
        "cube": "acs_yg_housing_median_value_1",
        "drilldowns": ["State", "Year"],
        "measures": ["Property Value"] 
    },
    "property_value_county": {
        "cube": "acs_yg_housing_median_value_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Property Value"]
    },
    "median_age_state": {
        "cube": "acs_ygs_median_age_total_1",
        "drilldowns": ["State", "Year"],
        "measures": ["Median Age"]
    },
    "median_age_county": {
        "cube": "acs_ygs_median_age_total_1",
        "drilldowns": ["County", "Year"],
        "measures": ["Median Age"]
    },
    "renters_by_income_state": {
    "cube": "acs_ygh_renters_by_income_percentage_1",
    "drilldowns": ["State", "Year", "Household Income", "Gross Rent Percent of Income"],
    "measures": ["Renters by Income Percentage"]
    },
    "renters_by_income_county": {
        "cube": "acs_ygh_renters_by_income_percentage_1",
        "drilldowns": ["County", "Year", "Household Income", "Gross Rent Percent of Income"],
        "measures": ["Renters by Income Percentage"]
    },
    "mortgage_costs_state": {
        "cube": "acs_ygh_homeowners_with_mortgage_spending_30_percent_on_costs_1",
        "drilldowns": ["State", "Year", "Mortgage Status"],
        "measures": ["Homeowners by Mortgage"]
    },
    "mortgage_costs_county": {
        "cube": "acs_ygh_homeowners_with_mortgage_spending_30_percent_on_costs_1",
        "drilldowns": ["County", "Year", "Mortgage Status"],
        "measures": ["Homeowners by Mortgage"]
    },
    "housing_value_bucket_state": {
        "cube": "acs_ygo_housing_value_bucket_1",
        "drilldowns": ["State", "Year", "Value Bucket"],
        "measures": ["Property Value by Bucket"]
    },
    "housing_value_bucket_county": {
        "cube": "acs_ygo_housing_value_bucket_1",
        "drilldowns": ["County", "Year", "Value Bucket"],
        "measures": ["Property Value by Bucket"]
    }
}

def fetchDataUSData(year="2016,2017,2018,2019,2020,2021,2022,2023,2024,2025"):
    results = {}
    for config_key, config in cube_config.items():
        cube = config.get("cube")
        params = {
            "cube": cube,
            "drilldowns": ",".join(config["drilldowns"]),
            "measures": ",".join(config["measures"]),
            "Year": year
        }
        try:
            response = requests.get(dataUSbaseURL, params=params)
            print(f"URL: {response.url}")
            if response.status_code != 200:
                print(f"Failed: {config_key} ({response.status_code})")
                continue
            data = response.json()
            # Warn if we got back no records
            if not data.get("data"):
                print(f"  ⚠️  No data returned for {config_key} — measure name is probably wrong")
            results[config_key] = data
        except Exception as e:
            print(f"Error with {config_key}: {e}")
    return results
